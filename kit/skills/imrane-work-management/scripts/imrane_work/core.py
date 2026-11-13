"""Validation, lifecycle and scoped atomic storage."""
from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

STAGES = ("qualification", "research", "plan", "production", "review", "delivery", "follow-up")
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
RESERVED = {"schema_version", "project", "stage", "created_at", "updated_at", "history", "revision", "blocked_intervals"}
FIELDS = {"id", "title", "owner", "mode", "domain", "brief", "priority", "blocker", "next_action", "tasks", "evidence", "review", "delivery", "decisions", "lessons", "escaped_errors"}


class WorkError(ValueError):
    pass


def now():
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def timestamp(value, label):
    if not isinstance(value, str):
        raise WorkError(f"{label}: expected ISO 8601 timestamp with timezone")
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            raise ValueError()
        return dt
    except ValueError:
        raise WorkError(f"{label}: expected ISO 8601 timestamp with timezone") from None


def slug(value, label="id"):
    if not isinstance(value, str) or len(value) > 100 or not SLUG.fullmatch(value):
        raise WorkError(f"{label}: use a lowercase slug (letters, digits, single hyphens; max 100)")
    if value in {"con", "prn", "aux", "nul", *(f"com{i}" for i in range(1, 10)), *(f"lpt{i}" for i in range(1, 10))}:
        raise WorkError(f"{label}: reserved Windows filename")
    return value


def obj(value, keys, label, required=None):
    if not isinstance(value, dict):
        raise WorkError(f"{label}: expected object")
    extra = set(value) - set(keys)
    missing = set(keys if required is None else required) - set(value)
    if extra or missing:
        raise WorkError(f"{label}: unknown fields {sorted(extra)}; missing fields {sorted(missing)}")


def string(value, label, meaningful=False):
    if not isinstance(value, str) or (meaningful and not value.strip()):
        raise WorkError(f"{label}: expected {'nonempty ' if meaningful else ''}string")


def strings(value, label):
    if not isinstance(value, list) or any(not isinstance(x, str) or not x.strip() for x in value):
        raise WorkError(f"{label}: expected array of nonempty strings")
    if len(set(value)) != len(value):
        raise WorkError(f"{label}: duplicates are not allowed")


def enum(value, options, label):
    if value not in options:
        raise WorkError(f"{label}: expected one of {', '.join(options)}")


def is_blocked(record):
    return record["blocker"]["active"] or any(i["disposition"] == "blocking" for i in record["brief"]["missing_inputs"])


def read_json(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise WorkError(f"duplicate JSON key: {key}")
            result[key] = value
        return result
    try:
        return json.loads(Path(path).read_text(encoding="utf-8-sig"), object_pairs_hook=unique)
    except (OSError, ValueError) as exc:
        raise WorkError(f"Cannot read JSON {path}: {exc}") from None


def beneath(path, root):
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


class Scope:
    def __init__(self, workspace, project):
        self.workspace = Path(workspace).resolve(strict=True)
        slug(project, "project")
        registry = read_json(self.workspace / ".codex/projects.json")
        entries = registry.get("projects", [])
        if not isinstance(entries, list):
            raise WorkError("registry projects must be an array")
        self.lanes = []
        selected = None
        for entry in entries:
            root = (self.workspace / entry["path"]).resolve()
            if not beneath(root, self.workspace) or root == self.workspace:
                raise WorkError("registry project path must be beneath workspace")
            self.lanes.append((entry["id"], root))
            if entry["id"] == project:
                if entry.get("status", "active") != "active" or entry.get("active") is False or entry.get("retired"):
                    raise WorkError(f"project {project} is retired/inactive")
                selected = root
        if project == "governance":
            descriptor = read_json(self.workspace / ".codex/governance.json")
            if descriptor.get("id") != "governance" or descriptor.get("path") != ".":
                raise WorkError("invalid governance descriptor")
            selected = self.workspace
        if selected is None:
            raise WorkError(f"unknown or retired project: {project}")
        if not selected.is_dir():
            raise WorkError("selected lane does not exist")
        self.root, self.project = selected, project
        self.store = self.path(".imrane/work")

    def path(self, reference):
        if not isinstance(reference, (str, Path)) or not str(reference):
            raise WorkError("path reference must be nonempty")
        raw = Path(reference)
        if ".." in raw.parts:
            raise WorkError("parent traversal is not allowed")
        candidate = raw if raw.is_absolute() else self.root / raw
        resolved = candidate.resolve()
        if not beneath(resolved, self.root):
            raise WorkError("path escapes selected lane")
        # Resolve junctions as well as symlinks. Registered children always own their subtree.
        for other_id, other_root in self.lanes:
            if other_id != self.project and beneath(other_root, self.root) and beneath(resolved, other_root):
                raise WorkError(f"path belongs to nested lane {other_id}")
        relative = candidate.absolute().relative_to(self.root)
        if any(":" in name for name in relative.parts):
            raise WorkError("alternate streams/colon paths are not allowed")
        part = self.root
        for name in relative.parts:
            part = part / name
            if part.is_symlink():
                raise WorkError("symlink paths are not allowed")
        return resolved

    def source(self, value, label, require_exists=False):
        string(value, label)
        if not value:
            return
        parsed = urlsplit(value)
        if parsed.scheme in ("http", "https") and parsed.netloc:
            if require_exists:
                raise WorkError(f"{label}: delivery artifact must be a scoped local path")
            return
        if parsed.scheme and not Path(value).is_absolute():
            raise WorkError(f"{label}: expected HTTP(S) URL or scoped local path")
        path = self.path(value)
        if require_exists and not path.is_file():
            raise WorkError(f"{label}: local file does not exist")

    def initialize(self):
        # Never retrofit an existing unmanaged store or change project configuration.
        if self.store.exists():
            marker = self.store / ".gitignore"
            self.path(marker)
            if not marker.is_file() or marker.read_text(encoding="utf-8") != "# imrane-work private state v1\n*\n":
                raise WorkError("existing work store is not managed/private; refusing to modify it")
            return
        self.path(".imrane").mkdir(parents=True, exist_ok=True)
        try:
            self.store.mkdir()
        except FileExistsError:
            return self.initialize()
        (self.store / ".gitignore").write_text("# imrane-work private state v1\n*\n", encoding="utf-8")

    def item_path(self, item_id):
        return self.path(self.store / "items" / (slug(item_id) + ".json"))

    @contextmanager
    def lock(self):
        self.initialize()
        lock = self.path(self.store / ".lock")
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError:
            raise WorkError("work store is locked; retry after the active command finishes (stale locks require manual inspection)") from None
        try:
            os.close(fd)
            yield
        finally:
            lock.unlink()

    def load(self, item_id):
        path = self.item_path(item_id)
        try:
            raw = path.read_bytes()
        except OSError as exc:
            raise WorkError(f"cannot read item {item_id}: {exc}") from None
        record = read_json(path)
        validate(record, self)
        if record["id"] != item_id or record["project"] != self.project:
            raise WorkError("record identity does not match selected scope/file")
        return record, hashlib.sha256(raw).hexdigest()

    def save(self, record, expected=None):
        validate(record, self)
        path = self.item_path(record["id"])
        self.write(path, json.dumps(record, ensure_ascii=False, indent=2) + "\n", expected)

    def write(self, path, content, expected=None):
        path = self.path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, temp = tempfile.mkstemp(prefix=".imrane-work-", dir=path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(content)
                handle.flush()
                os.fsync(handle.fileno())
            self.path(path)
            if expected is None:
                # Windows rename refuses existing destinations; POSIX hard-link install
                # supplies the same atomic create-if-absent semantics.
                try:
                    if os.name == "nt":
                        os.rename(temp, path)
                    else:
                        os.link(temp, path)
                except FileExistsError:
                    raise WorkError("output already exists; refusing to overwrite") from None
            else:
                if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                    raise WorkError("concurrent change detected; owner edit preserved, reload and retry")
                os.replace(temp, path)
        finally:
            Path(temp).unlink(missing_ok=True)


def defaults(item_id, project):
    at = now()
    return {"schema_version": 1, "id": item_id, "project": project, "title": "", "owner": "", "mode": "standard", "domain": "general", "stage": "qualification",
            "brief": {"goal": "", "deliverable": "", "in_scope": [], "out_of_scope": [], "inputs": [], "missing_inputs": [], "acceptance": []},
            "priority": {"impact": 3, "urgency": 3, "effort": 3, "reason": ""}, "blocker": {"active": False, "reason": ""}, "next_action": "", "tasks": [], "evidence": [],
            "review": {"reviewer": "", "independent": False, "required": False, "verdict": "pending", "notes": ""},
            "delivery": {"summary": "", "artifact": "", "delivered_at": "", "channel": ""}, "decisions": [], "lessons": [], "escaped_errors": None,
            "created_at": at, "updated_at": at, "revision": 1, "history": [{"event": "created", "at": at, "to": "qualification"}], "blocked_intervals": []}


def validate(r, scope):
    obj(r, FIELDS | RESERVED, "record")
    if type(r["schema_version"]) is not int or r["schema_version"] != 1:
        raise WorkError("schema_version must be 1")
    slug(r["id"])
    if r["project"] != scope.project:
        raise WorkError("project does not match selected scope")
    for key in ("title", "owner", "next_action"):
        string(r[key], key)
    enum(r["mode"], ("light", "standard"), "mode")
    enum(r["domain"], ("website", "research", "financial", "advertising", "general"), "domain")
    enum(r["stage"], STAGES, "stage")
    b = r["brief"]
    obj(b, ("goal", "deliverable", "in_scope", "out_of_scope", "inputs", "missing_inputs", "acceptance"), "brief")
    for key in ("goal", "deliverable"):
        string(b[key], "brief." + key)
    for key in ("in_scope", "out_of_scope", "inputs", "acceptance"):
        strings(b[key], "brief." + key)
    if not isinstance(b["missing_inputs"], list):
        raise WorkError("missing_inputs must be an array")
    for value in b["missing_inputs"]:
        obj(value, ("description", "disposition", "reason"), "missing input")
        string(value["description"], "missing input.description", True)
        enum(value["disposition"], ("blocking", "nonblocking", "not-needed"), "missing input.disposition")
        string(value["reason"], "missing input.reason", value["disposition"] != "blocking")
    obj(r["priority"], ("impact", "urgency", "effort", "reason"), "priority")
    for key in ("impact", "urgency", "effort"):
        if type(r["priority"][key]) is not int or not 1 <= r["priority"][key] <= 5:
            raise WorkError(f"priority.{key} must be an integer 1..5")
    string(r["priority"]["reason"], "priority.reason")
    obj(r["blocker"], ("active", "reason"), "blocker")
    if type(r["blocker"]["active"]) is not bool:
        raise WorkError("blocker.active must be boolean")
    string(r["blocker"]["reason"], "blocker.reason", r["blocker"]["active"])
    schemas = {"tasks": ("id", "title", "owner", "status", "depends_on"), "evidence": ("id", "criterion", "kind", "source", "observed_at", "result", "notes"), "decisions": ("id", "prediction", "rationale", "test", "observation", "outcome", "decided_at"), "lessons": ("id", "summary", "context", "limitations", "status", "reviewer", "reviewed_at", "sanitized", "proposed_change"), "escaped_errors": ("id", "description", "source", "observed_at")}
    for collection, keys in schemas.items():
        values = r[collection]
        if collection == "escaped_errors" and values is None:
            continue
        if collection == "escaped_errors" and first_delivery(r) is None:
            raise WorkError("escaped errors require observation at/after first delivery")
        if not isinstance(values, list):
            raise WorkError(f"{collection}: expected array")
        seen = set()
        for value in values:
            obj(value, keys, collection)
            slug(value["id"], collection + ".id")
            if value["id"] in seen:
                raise WorkError(f"{collection}: duplicate id")
            seen.add(value["id"])
            for key in keys:
                if key not in ("depends_on", "sanitized"):
                    string(value[key], collection + "." + key)
            if collection == "tasks":
                string(value["title"], "task.title", True)
                enum(value["status"], ("todo", "doing", "done"), "task.status")
                strings(value["depends_on"], "task.depends_on")
            elif collection == "evidence":
                enum(value["kind"], ("measured", "observed", "reported", "hypothesis", "unknown"), "evidence.kind")
                enum(value["result"], ("pass", "fail", "pending"), "evidence.result")
                if value["kind"] in ("hypothesis", "unknown") and value["result"] == "pass":
                    raise WorkError("hypothesis/unknown evidence cannot be marked pass")
                scope.source(value["source"], "evidence.source")
                if value["observed_at"]:
                    if timestamp(value["observed_at"], "evidence.observed_at") > timestamp(now(), "now"):
                        raise WorkError("evidence.observed_at cannot be in the future")
                if value["result"] in ("pass", "fail"):
                    string(value["source"], "evidence.source", True)
                    timestamp(value["observed_at"], "evidence.observed_at")
            elif collection == "decisions":
                enum(value["outcome"], ("pending", "supported", "rejected", "inconclusive"), "decision.outcome")
                if value["decided_at"]:
                    if timestamp(value["decided_at"], "decision.decided_at") > timestamp(now(), "now"):
                        raise WorkError("decision.decided_at cannot be in the future")
                if value["outcome"] != "pending":
                    for key in ("prediction", "rationale", "test", "observation"):
                        string(value[key], "decision." + key, True)
                    timestamp(value["decided_at"], "decision.decided_at")
            elif collection == "lessons":
                enum(value["status"], ("draft", "approved", "rejected"), "lesson.status")
                if type(value["sanitized"]) is not bool:
                    raise WorkError("lesson.sanitized must be boolean")
                if value["reviewed_at"]:
                    if timestamp(value["reviewed_at"], "lesson.reviewed_at") > timestamp(now(), "now"):
                        raise WorkError("lesson.reviewed_at cannot be in the future")
                if value["status"] != "draft":
                    string(value["reviewer"], "lesson.reviewer", True)
                    timestamp(value["reviewed_at"], "lesson.reviewed_at")
            else:
                string(value["description"], "escaped_error.description", True)
                string(value["source"], "escaped_error.source", True)
                scope.source(value["source"], "escaped_error.source")
                when = timestamp(value["observed_at"], "escaped_error.observed_at")
                delivered = first_delivery(r)
                if delivered is None or when < delivered:
                    raise WorkError("escaped errors require observation at/after first delivery")
                if when > timestamp(now(), "now"):
                    raise WorkError("escaped_error.observed_at cannot be in the future")
    tasks = {v["id"]: v for v in r["tasks"]}
    visiting, done = set(), set()
    def visit(key):
        if key in visiting:
            raise WorkError("task dependency cycle")
        if key in done:
            return
        visiting.add(key)
        for dep in tasks[key]["depends_on"]:
            if dep not in tasks:
                raise WorkError(f"unknown task dependency: {dep}")
            visit(dep)
            if tasks[key]["status"] in ("doing", "done") and tasks[dep]["status"] != "done":
                raise WorkError("active/completed task depends on incomplete task")
        visiting.remove(key)
        done.add(key)
    for key in tasks:
        visit(key)
    review = r["review"]
    obj(review, ("reviewer", "independent", "required", "verdict", "notes"), "review")
    for key in ("reviewer", "notes"):
        string(review[key], "review." + key)
    if type(review["independent"]) is not bool or type(review["required"]) is not bool:
        raise WorkError("review independent/required must be boolean")
    enum(review["verdict"], ("pending", "pass", "fail"), "review.verdict")
    delivery = r["delivery"]
    obj(delivery, ("summary", "artifact", "delivered_at", "channel"), "delivery")
    for key, value in delivery.items():
        string(value, "delivery." + key)
    scope.source(delivery["artifact"], "delivery.artifact")
    if delivery["delivered_at"]:
        when = timestamp(delivery["delivered_at"], "delivery.delivered_at")
        if when > timestamp(now(), "now"):
            raise WorkError("delivery.delivered_at cannot be in the future")
    created = timestamp(r["created_at"], "created_at")
    updated = timestamp(r["updated_at"], "updated_at")
    if updated < created or type(r["revision"]) is not int or r["revision"] < 1:
        raise WorkError("invalid audit timestamp/revision")
    if not isinstance(r["history"], list) or not r["history"] or r["history"][0].get("event") != "created":
        raise WorkError("invalid audit history")
    last_time, last_stage = created, "qualification"
    for index, entry in enumerate(r["history"]):
        event = entry.get("event")
        keys = {"created": ("event", "at", "to"), "updated": ("event", "at", "fields"), "advanced": ("event", "at", "from", "to")}
        if event not in keys:
            raise WorkError("unknown history event")
        obj(entry, keys[event], "history event")
        when = timestamp(entry["at"], "history.at")
        if when < last_time or when > updated:
            raise WorkError("history timestamps are out of order")
        if event == "created" and (index != 0 or entry["to"] != "qualification" or when != created):
            raise WorkError("invalid creation history")
        if event == "advanced":
            if entry["from"] != last_stage or entry["to"] not in STAGES:
                raise WorkError("invalid transition history")
            allowed = [] if last_stage == "follow-up" else [STAGES[STAGES.index(last_stage) + 1]]
            if last_stage in ("qualification", "review"):
                allowed.append("production")
            if entry["to"] not in allowed:
                raise WorkError("invalid transition history")
            last_stage = entry["to"]
        if event == "updated":
            strings(entry["fields"], "history.fields")
        last_time = when
    if last_stage != r["stage"] or r["revision"] != len(r["history"]):
        raise WorkError("stage/revision does not match audit history")
    if not isinstance(r["blocked_intervals"], list):
        raise WorkError("invalid blocked intervals")
    for interval in r["blocked_intervals"]:
        obj(interval, ("started_at", "ended_at"), "blocked interval")
        start = timestamp(interval["started_at"], "blocked start")
        if interval["ended_at"] is not None and timestamp(interval["ended_at"], "blocked end") < start:
            raise WorkError("blocked interval ends before start")


def first_delivery(r):
    recorded = any(e.get("event") == "advanced" and e.get("to") == "follow-up" for e in r["history"])
    return timestamp(r["delivery"]["delivered_at"], "delivery.delivered_at") if recorded and r["delivery"]["delivered_at"] else None


def metrics(r, at=None):
    at = timestamp(at or now(), "metrics.at")
    delivered = first_delivery(r)
    blocked = 0.0
    for interval in r["blocked_intervals"]:
        start = timestamp(interval["started_at"], "blocked start")
        end = min(timestamp(interval["ended_at"], "blocked end"), at) if interval["ended_at"] else at
        blocked += max(0.0, (end - start).total_seconds())
    return {"time_to_first_delivery_seconds": (delivered - timestamp(r["created_at"], "created_at")).total_seconds() if delivered else None,
            "revision_cycles": sum(e.get("event") == "advanced" and e.get("from") == "review" and e.get("to") == "production" for e in r["history"]),
            "blocked_elapsed_seconds": blocked,
            "escaped_errors": len(r["escaped_errors"]) if r["escaped_errors"] is not None else None}


def targets(r):
    stage = r["stage"]
    if stage == "follow-up":
        return []
    result = [STAGES[STAGES.index(stage) + 1]]
    if stage == "qualification" and r["mode"] == "light":
        result.append("production")
    if stage == "review":
        result.append("production")
    return result


def gate(r, target, scope):
    errors = []
    if target not in targets(r):
        return [f"transition {r['stage']} -> {target} is not allowed"]
    if r["blocker"]["active"]:
        errors.append("active blocker must be resolved")
    if any(x["disposition"] == "blocking" for x in r["brief"]["missing_inputs"]):
        errors.append("material missing inputs are blocking")
    if not (r["stage"] == "review" and target == "production"):
        for name, value in (("title", r["title"]), ("owner", r["owner"]), ("next_action", r["next_action"]), ("brief.goal", r["brief"]["goal"]), ("brief.deliverable", r["brief"]["deliverable"]), ("brief.in_scope", r["brief"]["in_scope"]), ("brief.acceptance", r["brief"]["acceptance"])):
            if not value or isinstance(value, str) and not value.strip():
                errors.append(f"transition requires {name}")
    if r["stage"] == "research" and target == "plan":
        if not any(e["kind"] != "unknown" and e["source"] and e["observed_at"] and e["notes"].strip() for e in r["evidence"]):
            errors.append("research requires sourced, dated evidence with notes; hypotheses/reported findings must remain explicitly tagged")
    if r["stage"] == "plan" and target == "production":
        if not r["tasks"] or any(not t["owner"].strip() for t in r["tasks"]):
            errors.append("plan requires nonempty owned tasks with validated dependencies")
    if r["stage"] == "production" and target == "review":
        if any(x["status"] != "done" for x in r["tasks"]):
            errors.append("all tasks must be done")
        if not r["evidence"]:
            errors.append("production requires evidence")
    if r["stage"] == "review" and target == "delivery":
        if not r["brief"]["acceptance"]:
            errors.append("acceptance criteria are required")
        for criterion in r["brief"]["acceptance"]:
            if not any(e["criterion"] == criterion and e["result"] == "pass" and e["kind"] in ("observed", "measured") and e["source"] and e["observed_at"] for e in r["evidence"]):
                errors.append(f"criterion lacks passed observed/measured evidence: {criterion}")
            if any(e["criterion"] == criterion and e["result"] == "fail" for e in r["evidence"]):
                errors.append(f"criterion has unresolved failed evidence; replace corrected evidence explicitly: {criterion}")
        review = r["review"]
        if review["verdict"] != "pass" or not review["reviewer"].strip():
            errors.append("review requires pass verdict and named reviewer")
        if review["required"] and (not review["independent"] or review["reviewer"].strip().casefold() == r["owner"].strip().casefold()):
            errors.append("required independent reviewer must differ from owner")
        if any(x["status"] != "done" for x in r["tasks"]):
            errors.append("all tasks must still be done")
    if r["stage"] == "delivery" and target == "follow-up":
        for key in ("summary", "artifact", "delivered_at", "channel"):
            if not r["delivery"][key].strip():
                errors.append(f"delivery requires {key}")
        if not r["next_action"].strip():
            errors.append("follow-up requires next_action")
        if r["delivery"]["artifact"]:
            try:
                scope.source(r["delivery"]["artifact"], "delivery.artifact", True)
            except WorkError as exc:
                errors.append(str(exc))
        if r["delivery"]["delivered_at"] and timestamp(r["delivery"]["delivered_at"], "delivered_at") < timestamp(r["created_at"], "created_at"):
            errors.append("delivery date precedes record creation")
    return errors


def patch_record(r, patch, scope, create=False):
    obj(patch, FIELDS if create else FIELDS - {"id"}, "input", required={"id"} if create else set())
    result = copy.deepcopy(r)
    result.update(copy.deepcopy(patch))
    at = now()
    validate(result, scope)
    if create:
        if is_blocked(result):
            result["blocked_intervals"].append({"started_at": at, "ended_at": None})
    else:
        if r["stage"] in ("delivery", "follow-up") and any(key in patch for key in ("brief", "tasks", "evidence", "review", "owner", "mode")):
            raise WorkError("accepted delivery fields are frozen; create a new work item for changed scope")
        if r["stage"] == "follow-up" and "delivery" in patch:
            raise WorkError("recorded handoff is frozen; create a new work item for a new delivery")
        result["revision"] += 1
        result["history"].append({"event": "updated", "at": at, "fields": sorted(patch)})
        if is_blocked(r) != is_blocked(result):
            if is_blocked(result):
                result["blocked_intervals"].append({"started_at": at, "ended_at": None})
            else:
                result["blocked_intervals"][-1]["ended_at"] = at
    result["updated_at"] = at
    validate(result, scope)
    return result


def advance(r, target, scope):
    errors = gate(r, target, scope)
    if errors:
        raise WorkError("; ".join(errors))
    result = copy.deepcopy(r)
    at = now()
    result["history"].append({"event": "advanced", "at": at, "from": r["stage"], "to": target})
    result["stage"], result["updated_at"] = target, at
    result["revision"] += 1
    if r["stage"] == "review" and target == "production":
        result["review"]["verdict"] = "pending"
        for evidence in result["evidence"]:
            evidence["result"] = "pending"
    validate(result, scope)
    return result

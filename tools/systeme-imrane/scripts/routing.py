"""Deterministic complexity recommendations; never select an active host model."""
import re
import unicodedata


def strip_accents(text):
    return "".join(c for c in unicodedata.normalize("NFD", text)
                   if unicodedata.category(c) != "Mn")


def recommend(prompt, previous, policy):
    legacy = policy.get("version") != 2
    text = prompt if legacy else strip_accents(prompt).strip().lower()
    if legacy:
        explicit = re.search(r"\[route:([a-z_]+)\]", text, re.I)
    else:
        # An inline example, quote, or code block is part of the task text.
        explicit = re.match(r"^\[route:([^\]\r\n]+)\](?=\s|$)", text)
        if explicit:
            text = text[explicit.end():].lstrip()
    # Preserve regex operators (\\S, \\D, \\B) and literal whitespace.
    matches = lambda patterns: any(re.search(p if legacy else strip_accents(p), text, re.I) for p in patterns)
    if legacy:
        # Existing recipients keep their personal v1 policy on toolkit upgrade.
        # Preserve its bindings/effort until an explicit models.py migration.
        aliases = {"luna": "fast_safe", "terra": "standard_safe", "sol": "deep_safe"}
        signals = {"critical": False, "deep": matches(policy.get("deep_patterns", [])),
                   "simple": matches(policy.get("fast_patterns", []))}
        route = "deep_safe" if signals["deep"] else "fast_safe" if signals["simple"] else policy["default_route"]
        reason = "legacy personal policy; explicit migration available"
    else:
        aliases = policy["aliases"]
        signals = {key: matches(patterns) for key, patterns in policy["signals"].items()}
        route, reason = policy["default_route"], "uncertain scope; conservative default"
        if signals["critical"] or signals["deep"]:
            route, reason = "deep_safe", "critical risk or explicitly deep analysis"
        elif any(signals[k] for k in ("architecture", "broad", "uncertainty", "dependencies")):
            route, reason = "standard_safe", "architecture, broad scope, uncertainty or coupled dependencies"
        elif signals["mechanical"] and not signals["implementation"]:
            route, reason = "mechanical_safe", "mechanical action with directly checkable result"
        elif signals["simple"] and not signals["implementation"]:
            route, reason = "fast_safe", "local presentation or label correction"
        elif signals["bounded"] and (signals["implementation"] or re.search(r"\b(corrige|corriger|fix|debug)\b", text)):
            route, reason = "focused_safe", "bounded implementation or isolated function/component correction"
        elif signals["implementation"]:
            route, reason = "balanced_safe", "defined implementation without high-risk signals"
    classified = route
    failures = 0
    failed = matches(policy.get("failure_patterns", []))
    continued = (any(re.fullmatch(p, text.strip(), re.I) for p in policy.get("continuity_patterns", []))
                 if legacy else matches(policy.get("continuity_patterns", [])))
    selected = None
    unknown_tag = False
    if explicit:
        tag = explicit.group(1).lower()
        selected = tag if tag in policy["routes"] else aliases.get(tag)
        if not selected:
            unknown_tag = True
            if policy["routes"][classified].get("level", 0) < policy["routes"][policy["default_route"]].get("level", 0):
                classified = policy["default_route"]
            reason = "unknown route tag; at least the conservative default"
    if selected:
        route, reason = selected, "explicit user override (does not grant permissions)"
    elif previous.get("route") in policy["routes"] and (continued or failed):
        route = previous["route"]
        failures = max(0, int(previous.get("failures", 0)))
        reason = "continuation of the same task"
        if failed:
            failures += 1
            reason = f"reported failure {failures}/2 in the same task"
        if ((unknown_tag or any(signals.get(k) for k in ("critical", "deep", "architecture", "broad", "uncertainty", "dependencies")))
                and policy["routes"][classified].get("level", 0) > policy["routes"][route].get("level", 0)):
            route, reason = classified, "new evidence raises the active task complexity"
        if failures >= 2:
            route = policy.get("failure_escalation_route", "deep_safe")
            reason = "escalation after two reported failures in the same task"
    else:
        route = classified
        if failed:
            failures = 1
    spec = policy["routes"][route]
    effort = spec.get("reasoning_effort", policy.get("reasoning_effort", "high"))
    if effort not in ("low", "medium", "high", "xhigh"):
        raise ValueError("Unsupported automatic routing effort")
    return {"policy_version": policy.get("version", 1), "route": route,
            "level": spec.get("level"), "reasoning": effort, "reason": reason,
            "signals": signals, "failures": failures}

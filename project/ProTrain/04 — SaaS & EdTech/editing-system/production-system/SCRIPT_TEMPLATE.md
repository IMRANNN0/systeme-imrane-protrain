# ProTrain script input template

The only necessary new input for a known ProTrain brief is the exact spoken script/version and any changed constraints. Reuse known brand, product boundaries, audience and format; do not make the owner refill the whole brief.

## Minimal owner input

```text
Pilot / script ID:
Version:
Script state: approved wording / draft to discuss
Target duration: approximate, to confirm against recording

HOOK
Exact spoken text

PROBLEM
Exact spoken text

SOLUTION
Exact spoken text

PRODUCT VALUE / PROOF
Exact spoken text

CTA
Exact spoken text

Changes to known brief, if any:
Available genuine product recordings/report, if any:
Voice preference, if any:
```

Keep Darija in Arabic script as supplied. Preserve any approved Latin terms rather than silently rewriting them; propose pronunciation/display handling separately. A script may use another framework: retain its actual structure rather than force every video into this template.

## Defaults already known

- Product: ProTrain Match; student formation-choice problem for Campus France.
- Delivery: vertical1080×1920,9:16;30 fps proposed.
- Brand: local extracted identity, original logo and Arabic Cairo.
- Exact marketing message preserved; free profile distinct from paid report, no numeric price in video.
- Authentic product recordings for demonstrations; permitted generated imagery for explanatory/context scenes.
- Storyboard approval before asset generation, approval before paid services and publishing.

## Assistant production output

Produce one row per meaningful beat, not per arbitrary number of seconds:

| Field | Required content |
| --- | --- |
| Scene and script reference | Stable sceneID and exact script section/line; no invented spoken words. |
| Timing | Estimated until audio exists, then measured start/end and frame mapping. |
| Visual/action | Exact subject, information revealed and why it serves the beat. |
| On-screen wording | Separate editable headings/captions, with approved meaning preserved. |
| Assets | Specific file/provider, authentic/generated status, permission and availability. |
| Audio | VO cue, pauses, optional licensed music/SFX and pronunciation notes. |
| Transition | Cut/reveal/move with a purpose, not an effects quota. |
| Approval/check | Missing evidence, storyboard decision, paid-service scope and review state. |

Record a script hash before media production. Retain the submitted file unchanged; changes receive a new version and permission where required. Caption transcription corrections must represent the actual approved speech, not introduce a new marketing claim.

## Current intake

[Pilot 001 V3](pilots/PTM-P001/script-v3.txt) has already been received: five sections,77 orthographic whitespace-delimited words. That count is descriptive, not a reliable duration estimator for Darija. [Storyboard revision1](pilots/PTM-P001/STORYBOARD_V1.md) was subsequently approved; its immutable file preserves the proposed-state header and the live production plan holds approval status. No need to request this same script again.


## Reference-analysis setup — 13 November 2026

For a reference-driven pilot, add `approved_style_id`, `style_profile_path`, `style_approval_event`, `techniques_to_use`, `techniques_to_omit`, `original_asset_provenance` and `unknowns`. Use null/pending until actual evidence/approval exists. See [STYLE_PROFILE_TEMPLATE.json](STYLE_PROFILE_TEMPLATE.json); an analysis report is not an automatically approved production template.

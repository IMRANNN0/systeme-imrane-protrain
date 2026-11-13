# ProTrain video production error log

Opened13 November 2026. Append findings, correction events and verification evidence; do not delete errors, rewrite history as success, or silently replace a previous decision. A documented rule is not proof that an old export has been corrected.

Historical evidence remains in [the9.5 second review](../DARIJA_AD_REVIEW_20261113.md), [client profile](../PROTRAIN_EDITING_PROFILE.md), [V2 review](../REVISION_V2.md), [craft review](../CRAFT_STUDY_REVIEW_20261113.md) and existing runtime QA records. Those artifacts are preserved.

## Initial audit records

| ID | Observed issue and evidence | Root cause | Correction/status |
| --- | --- | --- | --- |
| E001 |2–5.4s of the prior ad asserts profile-based matching over blank notebooks | Context imagery substituted for mechanism/evidence | Open for next pilot: genuine demo or labelled explanatory relationship; no fake UI. |
| E002 | Two still photos, gentle zoom and decorative type provide limited information progression | Animation selected before establishing what each beat explains | Rule adopted; new execution must be reviewed. Stills are not inherently defective. |
| E003 | Opening identifies Campus France but omits the formation-choice problem | Audience naming treated as sufficient relevance | P001V3 now explicitly mentions confusion choosing formations; rendered opening not yet tested. |
| E004 | Detailed execution started without a separate key-frame/animatic test | Production moved faster than visual planning | Owner now requires storyboard approval before assets; pilot storyboard pending. |
| E005 | Reference study emphasized identity/stills; full audiovisual scope incomplete | Available access was narrower than intended craft comparison | Record actual source/viewing scope and break down explanation, timing and sound. No claim of full viewing. |
| E006 | Generic word formations dominates type over personalized-profile benefit | Hierarchy followed word size rather than differentiating meaning | Improve hierarchy in proposed pilot; owner creative judgement pending. |
| E007 | Prior CTA holds4.1s/9.5s, including~2.34s after speech | No explicit time budget for reading versus new information | Test scene lengths against real audio. This is a creative question, not proven viewer drop-off. |
| E008 | CTA lacks a visible destination/free-entry cue in isolated export | Platform button/journey not reviewed with video | P001V3 distinguishes free profile from paid report; actual destination and platform preview remain pending. |
| E009 | Model audio assessment used without human native Darija listening/full-speed verdict | Perceptual review access incomplete | Model and human checks separately recorded; accent/delivery approval pending. No proven current hiss/bad accent claimed. |
| E010 | Logo/CTA placement not tested with actual Reels overlay | Canvas/phone-size still inspection treated too broadly | Placement review pending; do not claim observed obstruction without preview. |
| E011 | Legacy verifier hardcodes a visual-review pass, resets independent review and rewrites a single report | Qualitative judgement mixed into technical automation | New artifact-bound checker introduced; legacy script preserved and excluded from production workflow. See correction event below. |
| E012 | Copy/timing/frame counts repeated across source files; audio prep and final copy manual | One test-specific composition treated as a reusable system | Production plan/version records introduced. General composition generation/audio prep not yet automated. Verify exact delivery bytes. |

## Additional technical findings

| ID | Finding | Status |
| --- | --- | --- |
| E013 | Initial downmixed peak1.19 falsely suggested clipping; actual stereo channel peaks~0.842753 | Corrected historically: use original per-channel sample peaks. Retain false-positive history. Sample peaks do not prove true-peak/loudness compliance. |
| E014 | Prior export reports full-range yuvj420p/bt470bg, without verified delivery color policy | Open: define/test source-to-delivery SDR color handling; do not relabel unknown material and call it corrected. |
| E015 | Caption utilities and helper packages could be mistaken for tested Darija ASR/provider integration | Inventory now distinguishes installed, configured and actually tested. Automatic Darija alignment remains unverified. |
| E016 | Restricted localhost connection and memory/cache settings caused render failures | Known workaround: separate bundle/render, localTEMP,concurrency1,256 MBmedia cache; allowed execution context for Chromium. New55 second render still untested. |
| E017 | First final-video embed was not usable for the owner | Delivery now requires opening/link verification for the exact artifact and a direct file link fallback. |

## Correction events

**13 November 2026 — E011/E012, technical QA separation implemented.** Added [check_export.py](scripts/check_export.py). It accepts an exact artifact path and expected dimensions/FPS/optional duration or frames; optionally verifies complete narration duration plus start/tail fits output. It performs full decode, hashing and per-channel sample measurements. Each run creates a new timestamp/UUID technical report; visual/listening/creative/owner states remain pending and platform unknown.

Seven contract tests passed, including report/history preservation, changed bytes with failed revalidation, dimensions/duration failures and narration/tail overflow. Actual existing9.5 second file passed with7.16 second voice and0.5 second requested tail; source/media and historical reports unchanged. This proves technical behavior, not correction of prior creative weaknesses, caption sync or human voice approval.

**13 November 2026 — P001V3 received.** Exact user copy saved with hash in [script record](pilots/PTM-P001/script-record.json). Storyboard, service use, assets and publication remain separately pending. No media generated as part of system setup.

## Append format

**13 November 2026 — workflow consistency correction.** Independent review caught key-frame/animatic preparation placed before the owner's storyboard gate. Revised workflow/checklist so preapproval planning is textual (existing unchanged references may be inspected); new media/keyframes/animatic are prepared only after storyboard approval and applicable service authorization. No asset was generated in the incorrect order. Owner subsequently approved P001storyboardV1 in chat; approval is recorded separately from the immutable proposed storyboard.

Record date, errorID, artifact/version/hash or scene/timecode, observed problem, root cause, proposed/applied correction, approval where relevant, evidence and unresolved checks. Add a later event when a fix is tested; preserve the original observation and previous exports. Treat a preference change as a superseding decision, not a fabricated technical failure.


**13 November 2026 — E018, UTF8 authorization-record read.** A default WindowsCP1252 JSON read failed after Arabic content entered the plan. The voice helper correctly refused an unrecorded approval and made no provider request. Corrected the record reader to explicitUTF8, then performed one authorizedTTS call. Four provider-free guard tests verify storyboard/service approval, script-hash preservation and request-limit checks.

**13 November 2026 — E019, perceptual input limitation.** Native audio forwarding returned that this controller cannot accept audio input. No listening verdict was fabricated and no extra paid multimodal analysis was called outside the approvedTTS scope. Owner has the WAV preview; narration/caption listening remains pending.

**13 November 2026 — approved pilot materials.** Two generated photographic context/metaphor assets saved with prompts/provenance, one35.84second narration saved with processing record, and a real public form screenshot captured without entering contacts, consenting to processing, submitting or purchasing. Owner approved explanatory report scenes; original approvedV3words retained. Actual export review follows separately.


**13 November 2026 — E020, observed pilot form layout defect.** Actual exported previewV1 phone frames around11.6–17.3seconds showed the two-line heading colliding with the free badge, and a whole-form view too small to read. Preserved V1 and its36-frame/technical evidence. Corrected heading/badge spacing and used a closer camera crop of the unchanged genuine bac-stream/average pixels. Rendering V2 as a new file; correction verification remains pending until V2 frames are inspected. No additional provider request or spoken-copy change.


## Pilot checkpoint — 13 November 2026

**E020 correction verified:** V2 actual frame review confirms heading/badge separation and enlarged genuine form details. Exact MP4 SHA256 `6f540262ea1d3e7e137c8b88d6a31c002c3e66c861752c0b77611fba7b897dcb`; all36 sampled frames reviewed independently with no blocking visual defect observed. V1 remains preserved. Listening, caption alignment, normal-speed motion, owner acceptance and platform checks remain pending. No extra provider request. E014 historical color issue is not retroactively erased; this V2 reports yuv420p/bt709 metadata, not perceptual certification.

Evidence: [V2 exact-export review](pilots/PTM-P001/REVIEW_PREVIEW_V2.md).


## Reference-analysis setup — 13 November 2026

**E021 — Windows model-loader Unicode path.** First rea-video run generated reports but OpenCV could not open the YuNet path under the em-dash workspace; its Haar fallback also failed. Source hash was valid. Copied the pinned MIT model to the selected client private ASCII runtime cache and updated only the adapter. Direct native model load and the second actual analysis passed without the warning; first run retained.

**E022 — machine classifications conflict with known source.** Own Pilot001V3 still-image push-in was labelled AI video; narration-only audio produced possible SFX/music candidates. Sampled-frame/source-provenance review was merged but native fusion retained the first label. Preserve machine estimates as uncertain and attach confirmed source facts; do not automate paid generation from them. This is not a measured failure rate on external ads.

**E023 — CRLF integrity false positive.** Official skill-installer Git checkout used Windows CRLF while the raw source snapshot used LF. Initial byte-only comparison failed. All10skill text files match after newline normalization; both byte hashes retained. Do not overwrite files merely to silence this expected representation difference.

Evidence: [integration report](REA_VIDEO_INTEGRATION.md) and [verification](rea-video-setup-verification.json).

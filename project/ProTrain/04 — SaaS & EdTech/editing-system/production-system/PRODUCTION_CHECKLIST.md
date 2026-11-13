# ProTrain production checklist

Apply at intake, before assets, before preview and before final handoff. Use [workflow](VIDEO_WORKFLOW.md) and [standing review notes](<{{IMRANE_WORKSPACE_ROOT}}/.agents/skills/performance-video-editing/references/production-review.md>). Each item is completed only when evidence exists for this version; this unchecked template grants no approval.

## Intake and plan

- [ ] Exact script/version/hash saved; spoken copy matches user input.
- [ ] Audience, problem, benefit and real next action clear.
- [ ] Company/Match distinction and supported feature/offer limits maintained.
- [ ] Every meaningful beat has a visual purpose, assets and caption/audio plan.
- [ ] Existing reference scope recorded; initial shot proposal is textual, with new media preparation reserved until approval.
- [ ] Estimated timing labelled; real voice later determines timing.
- [ ] Missing genuine product capture/report identified without fabricating UI.
- [ ] Owner approved this storyboard revision before asset preparation/generation.

## Services and assets

- [ ] After storyboard approval and any required service authorization, key frames/animatic prepared before full animation.
- [ ] Paid provider/model, inputs, scope/limit and attempts authorized before use.
- [ ] Any required Canva AI-limit confirmation obtained if that optional service is selected.
- [ ] Authentic UI/report permission and redaction checked before use/upload.
- [ ] Generated imagery inspected for anatomy, artificial detail and story relevance; provenance retained.
- [ ] Original logo and controlled Arabic text remain accurate; no fake testimonial or admission evidence.
- [ ] Music/footage/font/SFX rights and production-tool eligibility checked where applicable.

## Voice, captions and edit

- [ ] Actual recording preserves exact approved message and complete sentence tails.
- [ ] Darija pronunciation, brand names and delivery reviewed; reviewer/method recorded.
- [ ] Speech duration and pauses measured; complete narration fits video including intended tail.
- [ ] Captions match actual speech, use corrected phrase timings and natural Arabic breaks.
- [ ] Arabic joining, bidi punctuation, numerals and mixed-script terms checked in export.
- [ ] Every cut/reveal advances explanation, evidence or attention; no unnecessary template/AI scenes.
- [ ] Demonstrated product detail is authentic and readable; no hidden qualifier cropped out.
- [ ] CTA/hold suits this recording and actual destination; free profile is not confused with full report.
- [ ] Speech is intelligible with any music/SFX; actual channel peaks/loudness checked appropriately.

## Exact export and review

- [ ] Technical checker run on the exact candidate path/hash; fresh report retained.
- [ ] Dimensions1080×1920,9:16,FPS and approved duration checked.
- [ ] H264MP4/AAC output and intended color policy checked; do not infer these from dimensions alone.
- [ ] Full file decodes; complete narration/tail check performed with source audio.
- [ ] Actual first frame, boundaries, text-heavy scenes, product evidence, CTA and last frame inspected at phone size.
- [ ] Normal-speed playback/motion and listening reviewed, or explicitly recorded pending with draft status.
- [ ] Intended placement overlays checked; no claim of Meta-ready placement without evidence.
- [ ] Technical, human/model perceptual, creative and owner-review states separated and hash-bound.
- [ ] All observed blockers corrected; changed bytes receive affected rechecks, no inherited creative pass.
- [ ] Exact checked file opens from delivered preview/direct link; SRT/CaptionJSON/sourceplan preserved.
- [ ] Owner final feedback/approval recorded; publishing remains separately authorized.
- [ ] Errors/correction events and approved reusable lessons appended; prior records not overwritten.

## Technical automation boundary

`scripts/check_export.py` automates artifact identity, dimensions/FPS/optional duration/frames, full decode, per-channel sample peaks, observed color metadata and optional complete-voice fit. It does **not** approve captions, accent, motion, truth of claims, actual synchronization, licensing, owner taste or platform placement. Codec/color target validation and subjective checks still require explicit review of report/export. Technical reruns create new report directories and leave existing review history untouched.

Current technical setup evidence uses the previous9.5 second export only. P001V3 storyboardV1 was approved by the owner in chat after proposal; see the pilot production plan/approval log for current status. Subsequent owner-authorized preparation produced one narration take, two context images and an authentic public form capture; first preview is being assembled. Owner-approved explanatory visuals replace missing report capture. Final approval is still pending.


## Pilot checkpoint — 13 November 2026

P001 corrected V2: exact-artifact technical check and full decode passed (1080×1920,30fps,1140frames,38sec,H264/AAC). Source narration plus2sec tail fits. Controller contact sheets and independent36-frame review completed; original script/caption words and genuine-form/explanatory boundaries retained. Human listening/internal caption sync, full-speed motion, actual Meta overlays and owner acceptance remain unchecked. The generic checklist above is a template; see the per-export review for this candidate.

Evidence: [V2 exact-export review](pilots/PTM-P001/REVIEW_PREVIEW_V2.md).


## Reference-analysis setup — 13 November 2026

Before using a reference profile, verify permitted local source/provenance and source hash; preserve raw vs reviewed reports; check measured cuts separately from semantic beats; inspect frames and full motion; listen before confirming music/SFX/beat synchronization; verify text/font/RTL instead of trusting OCR. Keep disagreements and unknowns. Confirm style approval before adapting with original assets. The installed base test has no OCR/ASR/stem separation; HTML/VIDEO.md generation and schema validation are tested. See [actual setup verification](rea-video-setup-verification.json).

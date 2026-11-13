# ProTrain Match video workflow

Version 1,13 November 2026. The implemented baseline is a local Remotion/FFmpeg studio plus documentation and technical QA. A complete autonomous script-to-video engine is not yet implemented. Start with [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md), [CREATIVE_GUIDELINES.md](CREATIVE_GUIDELINES.md), [ERROR_LOG.md](ERROR_LOG.md) and [PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md).

## Actual capability inventory

Inspection separates local executable tests, retained historical evidence, tool exposure and unconfigured services. No fresh paid/provider request was made for this inventory.

| Capability | Available evidence | Automation status |
| --- | --- | --- |
| Local assembly/render | Node 24.14.0, Remotion 4.0.543, React 19.3.1, TS 7.0.2; existing editable compositions and successful exports; current typecheck passes | Repeatable local rendering from an authored composition and available assets. A new55 second composition is not yet built/tested. |
| Media processing/QA | Python 3.14.2,FFmpeg/ffprobe9.0.2,NumPy 2.5.4,Pillow 12.2.0; existing MP4 fully decodes | Local duration/probe/decode, frame extraction, audio measurements and artifact hashing can be automated. Creative/listening approval cannot be inferred. |
| Raster generation | Built-in ImageGen tool exposed; real generated PNGs retained | External AI generation, available on request after approved storyboard; outputs need visual review and provenance. |
| Darija TTS | Gemini genericKore takes and metadata retained from the9.5 second test | Historically working external API path. New access/quota/billing not checked. New paid use requires explicit approval. |
| ElevenLabs | No tested connector/credential integration in this lane | Optional external alternative; not configured/ready merely because an adapter package exists. |
| Local speech | Windows System.Speech exposes Zira en-US | English fixture voice only; no verified local Moroccan Darija voice. |
| Caption rendering | `@remotion/captions`, Caption fixtures and Arabic text rendering | Render/export corrected timed text locally. Full Darija transcription/alignment is not validated. |
| Local transcription | No active PythonWhisper/faster-whisper/torch or WhisperCLI; FFmpegwhisper filter exists | Filter present, model/config missing or unverified. Needs deliberate model setup/testing before being called usable ASR. |
| Transitions/motion | `@remotion/transitions` installed; basic interpolation/easing already used | Local capability, chosen by scene purpose; not a requirement to use every library. |
| Generated video | Canva `create_video` tool exposed, Seedance engine, output schema480p/720p | Untested external option, not the default1080p master pipeline. Tool-specific AI-limit confirmation and user approval required before any generation. Upscaling would not create native1080p detail. |
| Authentic product demos | No supplied Match screen recording/redacted report for P001 | Human/product-owner asset input or authorized capture is needed. Do not synthesize fake UI as a substitute. |
| Automation | Local Python/Node scripts, manifests and file-based versioning | Parameterized technical QA is implemented and tested; full storyboard-to-composition generation, validated ASR and provider orchestration remain staged development. |

Remotion's [caption guide](https://www.remotion.dev/docs/captions/) separates caption import/display/export; its [transcription guide](https://www.remotion.dev/docs/captions/transcribing) lists separate local/cloud engines. Installed caption utilities alone are not ASR. [Gemini TTS](https://aistudio.google.com/docs/speech-generation) and [ElevenLabs TTS](https://elevenlabs.io/docs/overview/capabilities/text-to-speech) are external services. Check [Remotion licensing](https://www.remotion.dev/docs/license) before commercial production where applicable; earlier `isProduction:false` tests do not establish eligibility.

## Who does what

| Category | Work |
| --- | --- |
| Can run locally after inputs are valid | Script/version hashing, asset validation, measured audio duration, assembly from approved plan, caption layout/export from reviewed timings, render, complete decode, metadata/audio checks, unique QA reports and delivery hashing. |
| Assistant prepares and creatively reviews | Scene analysis, proposed shot list, key frames/animatic, visual explanation, pronunciation/caption correction, purposeful cuts and iterative fixes. These are not unattended quality guarantees. |
| External AI services | Generated imagery/video, Gemini/ElevenLabs voice, optional cloudASR/multimodal review. Confirm provider, uploaded material, intended use, charge/AI-limit implications and allowed attempts before use. |
| Owner/manual approval or input | Exact marketing-message changes, storyboard before assets, paid service scope, authentic demo assets/permission, Darija voice/style feedback, preview/final approval and separate publication permission. |

## Pipeline and status

1. **Intake.** Save exact user script/version and approval state. Read existing context, approved rules and open errors. Reuse known information rather than request the same brief again. P001V3 has been received; new storyboard/service approvals remain pending.
2. **Analysis and proposed storyboard.** Prepare a text-only shot plan mapping every spoken beat to a visual purpose, caption plan, sound, transition and specific asset. List evidence and missing authentic captures; keep times estimated. Inspect already-existing unchanged references if useful. Prepare new media/keyframes/animatic only after storyboard approval and any required service authorization.
3. **Storyboard approval.** Present concrete scenes and ask the owner to approve or revise the plan. Do not prepare/generate new media before approval. A supplied script is not storyboard approval.
4. **Service authorization.** Before paid calls, identify the service/model, inputs leaving the environment, output, budget/approvedlimit and maximum attempts. Record the owner's explicit scope. Existing keys, earlier experiments, storyboard approval and free quotas do not themselves authorize spending. Canva video has its own mandatory AI-limit confirmation. If a step uses cleared local assets only, no paid-service request is needed for that step.
5. **Asset preparation.** After storyboard approval and applicable service authorization, prepare key visual frames and a low-cost animatic before polishing full animation. Generate only approved assets; retain prompt/provider/date and fictional/real status. Obtain genuine redacted Match form/report/offer recordings for demonstration. Check media/music rights. Do not invent unavailable UI/features/results. Preserve originals.
6. **Voice and alignment.** Preserve approved text; create permitted voice or use supplied recording. Review a sample before spending approved remaining attempts on fulltakes. Measure duration, mark actual phrases, correct caption text/timing and record voice review. Never force guessed timing or call estimates forced alignment.
7. **Rough cut and preview.** Build the local composition against the current plan/audio, using real asset references. Export a clearly labelled preview. Show the actual playback file and requested review points; retain missing/untested checks explicitly.
8. **Feedback and revision.** Record feedback verbatim with version/timecode. Classify observed error, preference or unverified hypothesis. Apply permitted corrections, preserve old exports and append correction events. Marketing-message changes still require approval.
9. **Technical and creative QA.** Run artifact-bound technical checks on the exact candidate; separately inspect real frames, playback/listening, captions, actual product truth and placement. Preserve review history and do not transfer a prior creative pass to new bytes. Resolve findings and rerun affected checks.
10. **Owner review and delivery.** Deliver same-hash preview/finalMP4, captions, source plan and review state. Owner taste approval is explicit. Publication remains a separate owner-authorized action; no automatic upload/campaign launch.
11. **Learning.** Append error/correction records and new approved decisions. Keep superseded decisions/history. Improve reusable code/rules from demonstrated issues without adding an effects quota or rewriting client identity.

## Production data and review records

Each pilot keeps exact script/version/hash, storyboard revision, asset/source list, proposed/measured timing, explicit approvals and provider scope in its production plan. User approval remains pending until an actual reply is recorded; file creation or time passing is not consent.

Technical runs write unique report directories and bind path/hash to the actual MP4. Human/model perceptual review, creative judgement, owner approval and placement validation are separate records referencing that hash. Technical reruns must not erase them. A new hash requires reviewing affected content; old reports stay historical.

New generic QA entry: `python scripts/check_export.py <exact-mp4> --output-root runs --expected-width 1080 --expected-height 1920 --expected-fps 30`, from this folder. Use the script's `--help` for narration/length checks. It performs technical inspection only. See [PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md) for the remaining reviews. The earlier fixed285 frame verifier is a legacy test and must not be used as the new55 second production checker.

## Runtime constraints and next engineering steps

Keep existing studio at `../video-studio`; do not scaffold another runtime. Windows path contains`&`: invoke Remotion's JS CLI throughNode. Use project-localTEMP/TMP, separate bundle/render processes, concurrency1 and the tested256 MBmedia cache where applicable. Elevation may be needed for local Chromium networking; retain normal approvals.

The existing renderer exports a9.5 second composition and is not a55 second template. Next production engineering after storyboard approval: derive a composition from the approved measured plan, reproducible audio preparation, reusable caption data and append-only review records. Darija ASR and AIvideo are optional later improvements, not claims of current automation. No new dependencies or provider calls are required just to plan P001.


## Pilot checkpoint — 13 November 2026

P001 now has a measured, data-driven38-second composition and version-preserving renderer at `../video-studio/src/Pilot001.tsx` and `../video-studio/scripts/pilot001-render.mjs`. Corrected V2 rendered successfully with the documented constrained runtime. Local assembly, caption display from supplied timings, export, hashing and technical QA are executable. Automatic script-to-storyboard judgement, natural Darija validation, internal caption alignment and creative/placement approval remain manual. Historical next-step paragraphs above describe the initial setup.

Evidence: [V2 exact-export review](pilots/PTM-P001/REVIEW_PREVIEW_V2.md).


## Reference-analysis setup — 13 November 2026

Reference analysis now has a tested local adapter: `python editing-system/production-system/scripts/run_rea_local.py <permitted-local-video>` from the SaaS component. The pinned tool has a private venv and fresh outputs; it does not expose generation. Read [integration details](REA_VIDEO_INTEGRATION.md) before use. Analyse reference -> review measurements/uncertain labels/audio -> proposed style profile -> owner style/storyboard approval -> original assets -> existing renderer. Native classification/review fusion may disagree with source facts. Never route generation directly from a machine label or use upstream assemble defaults to retain protected footage.

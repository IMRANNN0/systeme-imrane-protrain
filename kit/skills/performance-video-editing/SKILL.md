---
name: performance-video-editing
description: Turn advertising or trust video scripts into shot-by-shot editing plans, then execute and verify edits when source media and a supported editing environment are available. Use for reusable script-to-video workflows, edit briefs, footage assembly, captions and video revisions.
---

# Performance video editing

Convert the supplied script into concrete editing decisions with enough detail for execution. Reuse the selected client's local editing profile and approved script. Keep generic methods in this skill and client facts, assets, references and feedback inside that client's lane.

## Standing production review

For every video planning, editing, revision or quality-review task, read [Video editing review notes](references/production-review.md) before work and revisit them before handoff. Apply the checks relevant to the task. Keep technical measurements, perceptual assessment, creative judgement and owner approval distinct; record only completed checks for the exact export. Do not repeat the checklist to the user unless useful.


## Inputs and continuity

Read the script version, its approval state, objective, audience, CTA destination and relevant client profile. Consult existing references and assets before asking questions. Request only missing choices that change the work, such as the editing application or a reference that defines the desired look. Continue useful planning while those answers are pending.

Use an established client profile when present. Otherwise propose restrained defaults and explicitly label them provisional. A script alone supports a storyboard. Actual footage or voice-over is needed for source timecodes and synchronization. A render also needs a verified media tool or editing application. Do not make the user repeatedly supply a profile already available in the current lane.

Preserve the approved spoken script, offer and destination. Suggest copy revisions separately if a line cannot be executed or contains an unsupported claim. Any needed restructuring should preserve the customer's actual framework rather than force every video into the same formula.

## Choose the visual treatment

Decide from the content and evidence, not from the order in a template.

- Product demonstration. Bring the relevant real UI or deliverable on screen when its value is discussed. Choose one readable detail at a time. Use a clearly labeled illustrative frame if the real asset is unavailable, and retain the missing-real-asset status.
- Expert or authority. Prioritize the speaker's delivery and concrete explanation. Use supporting visuals for specific claims or comparisons. Preserve pauses that carry meaning.
- Testimonial or case study. Preserve the speaker's own meaning and the actual result. Attribute agency work, product use and documented outcomes accurately. Collect permission for intended use and redact private data in both picture and audio where needed.
- Narrated comparison or explainer. Use graphics that clarify relationships, conditions or sequence. Do not invent binary pass/fail results, customer comments, testimonials or product screens as evidence.

Begin with the visual that gives the opening line its meaning. Plan changes when the idea, proof or emphasis changes. Avoid arbitrary cut frequencies, ornamental motion and repeated sound effects. Explain what each insert helps the viewer understand.

## Output contract

For a supplied script, prepare the smallest useful execution package, normally these elements.

1. Brief. Script ID/version, objective, viewer, CTA, output format and profile/reference used. Mark inferred settings.
2. Editing timeline. One row per meaningful beat, with beat ID, script line or source line IDs, estimated output timing, picture/action, on-screen text, caption behavior, sound and transition, source asset and availability.
3. Asset list. Identify provided/inspected assets, requested assets and proposed illustrations. Reference files precisely. Each requested asset should identify what must be visible or audible. Group missing assets into one concise request.
4. Execution and QA status. State whether this is a storyboard, an actual project/timeline, a draft render or a verified export. Name the next action and any unresolved dependency.

Include exact on-screen wording where it is known. A direction such as 'add B-roll' is incomplete without the subject, purpose and source. Separate visual labels from spoken subtitles. Use estimated timing only as a planning aid and revise it against recorded speech or footage before claiming sync.

Keep output adapted to the user. For a request about one beat or one correction, return that scope rather than regenerating a full package.

## Captions, text and sound

Use the spoken language and the client's terminology. Preserve meaning, negation, qualifications and the CTA. Break captions into readable phrases instead of blindly splitting each word. Prefer short lines with a conservative two-line target where the composition permits. Check actual line breaks and reading time.

For Arabic, keep letters joined and paragraphs in the appropriate direction. Inspect Arabic shaping, numerals, punctuation and mixed Latin tokens in rendered frames. Transliterate brand names when that is the approved style. Verify exported captions or subtitle files, not only an editor preview.

Position text using the actual frame composition and the intended placement's current overlays. Do not treat a guessed safe-area margin as universally valid. Keep faces, proof and UI details readable on a phone. Retain essential qualifying text when cropping.

Prioritize clear speech. Use music and effects only where they support the content and their intended use is permitted. Check peaks, distortion, transitions and intelligibility in the actual export. Avoid claiming audio was heard when only metadata or waveforms were inspected.

## Execute when the inputs support it

Before editing, inspect available assets and tools. Verify the actual application, API, CLI or import support. Do not claim a native editable project exists unless it was created and its compatibility checked. Follow the computer-use skill if operating a GUI. Preserve original media and existing project edits.

Inspect clips and transcripts before selecting source ranges. Keep source in/out timecodes distinct from output timeline ranges. Use the source's actual frame rate or variable-frame-rate timing. Adapt output dimensions, duration and export settings to the user's requested placement and current media. State provisional settings when unknown.

Create or modify only the requested outputs. A script-only request does not authorize paid stock, cloud transcription, voice cloning, messages to people or publishing. If a media tool is unavailable, complete the storyboard and identify the execution dependency accurately.

For rendered work, verify duration, dimensions, frame rate, orientation, audio tracks and playback. Inspect the beginning, transitions, text-heavy frames, proof and CTA, plus the ending. Listen to speech and music when audio playback is available. Check caption timing, Arabic rendering, privacy redactions and the absence of accidental black/frozen frames. Record the scope and limits of actual checks. A render without a listening check remains audio-review-pending.

## Remotion backend

When Remotion is the selected backend, use the installed [Remotion best practices](../remotion-best-practices/SKILL.md) and load its relevant modules for markup, Arabic, captions, interactivity or export. Keep the client profile and media in the current lane. Verify the local package scripts, since Windows paths containing an ampersand can break npm executable shims. Preserve the requested output scope when choosing between a preview and an export.

## Improve from feedback

Apply corrections to the current video and update only approved recurring preferences in the client's profile. Keep taste choices provisional until confirmed through an example or explicit feedback. Separate observed campaign measurements from creative hypotheses. Never promise retention or conversion gains from an editing choice alone.

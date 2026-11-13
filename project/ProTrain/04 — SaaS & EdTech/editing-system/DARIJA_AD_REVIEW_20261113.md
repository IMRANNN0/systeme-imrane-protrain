# ProTrain Match narrated ad review

13 November 2026. Delivery: `video-studio/out/protrain-match-darija-final.mp4`.

9.5seconds,1080×1920,30fps,285frames,H264/AAC. Complete decode and TypeScript checks passed. Illustrative photo-led ad with a generic synthetic Moroccan Darija woman voice. No testimonial, real product demonstration or campaign launch.

## Script and edit

«كتوجد لكامبوس فرانس؟ بروترين ماتش كيقترح عليك تكوينات على حساب ملفك. عمّر ملفك دابا.»

-0–2s: fictional adult student photo and full Campus France question visible on frame0.
-2–5.4s: photographic notebook cutaway, product name and academic-profile benefit.
-5.4–9.5s: student photo and amber CTA on green. Last~2.34s allow reading after speech ends.

Exact website colors#0A6B43,#F2A541,#0F2A1F,#F6F4EE; original logo. Actual website Cairo Arabic variable font downloaded, upstream SIL OFL license retained. Text and logo remain separate from generated imagery. Asset prompts/provenance saved in `public/darija-ad/` and existing `public/craft/`.

## Critique and corrections

1. Audio take1 rushed the product name. Two further takes generated; take3 uses original Latin product spelling for clearer TTS articulation. All on-screen sentences stay Arabic. No voice cloning.
2. Take3 audio model review noted possible high-frequency buzz. Applied mild70Hz highpass/8kHz lowpass, loudness/peak control. Actual exported-MP4 model review reported clear Darija, intelligibility, sync and no audible noise/distortion.
3. Suspected hook/benefit wrapping checked in13 actual360×640 decoded frames; both remain single-line and contained. First frame, both sides of cuts and last frame reviewed.
4. Rejected model's optional tracking advice for «كتوجد»: the visible word is legible and Arabic joining must stay intact.
5. Initial QApeak1.19 investigated: FFmpeg's equal-power stereo→mono added~3dB. Actual each channel peak0.842753. Corrected QA to arithmetic averaging, source/output correlation0.9999787. No clipping found in actual channels.

Controller and native `/root/protrain_darija_ad_review` independently reviewed exported frames. Arabic, logo, face clearance, contrast and held CTA passed with no concrete visual blocker. Worker approves as a short production test.

Gemini3.1FlashLite assessed the actual MP4 picture/audio. This is model-based perceptual review, not a human listening or full-speed playback verdict. IAB preview timed out; local Studio stopped before export. No physical-phone or live Meta placement-overlay verification. Generated photos are stills with restrained reframing/type; blank notebooks convey study, not matching evidence. No measured ad performance, guaranteed acceptance, real UI or launch readiness claimed. User taste approval remains pending.

## Evidence and local reproduction

Editable source `src/DarijaAd.tsx`; speech provenance `public/darija-ad/voice-generation-take3.json`, `voice-review-take3.json`, `voice-processing.json`; actual QA `out/darija-ad-qa/{verification.json,export-review.json,overview.jpg,contact.jpg}`.

Reuse existing local assets: `npm run check`, separate `node --max-old-space-size=512 scripts/darija-ad-render.mjs bundle` and `... video`, then `python scripts/verify-darija-ad.py`. Copy verified MP4 to final delivery name. API regeneration is a separate deliberate action. Media renderer requires minimum240MB cache;256MB/concurrency1 used. Localhost Chromium needed elevated execution outside restricted shell. No packages installed; shared skills and prior practice outputs preserved.

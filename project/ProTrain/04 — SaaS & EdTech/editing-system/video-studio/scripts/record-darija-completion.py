"""Record this verified local production milestone in the selected client's memory."""
from pathlib import Path

memory=Path('{{PROTRAIN_PROJECT_ROOT}}/.codex/memory')
checkpoint='''## Narrated Darija ad completed — 13 November 2026

### Restart checkpoint
- Current stage: actual revised narrated9.5sec local ad exported, technically checked and reviewed; user taste feedback pending. Owner explicitly requested≤10sec real Darija voice/API generation, brand assets, self-critique and corrections before handoff.
- Delivery:04 — SaaS & EdTech/editing-system/video-studio/out/protrain-match-darija-final.mp4;6086343bytes;H2641080x1920/30fps285frames9.5secvideo/container9.515sec,AACstereo. SHA256d17efb2af8afaa2d96ca8184bee30d88c91f555ea4f71ef08c00211f4b79e7d0. Full decode/TypeScript passed. Prior practice videos preserved.
- Creative: generated fictional adult Moroccan student/desk photographs, actual green#0A6B43/amber#F2A541/forest#0F2A1F/ivory#F6F4EE, true logo, website CairoArabicfont/OFL saved. Read local brand reference rather than repeat extraction. Three beats:0–2hook,2–5.4profile-based recommendations,5.4–9.5heldCTA. All screen sentences Arabic, no price, fake report/UI, acceptance promise or testimonial.
- Speech: existing authorized Gemini API key read in memory only; no secret copied/logged. Gemini3.8FlashTTS/Kore generated3takes. Take3 uses Latin product spelling to improve articulation,7.16sec. Mild70Hzhighpass8kHzlowpass and loudness/peak control; no time stretch/voice cloning. Model actualMP4 review (Gemini3.1FlashLite) found clear Darija, sync and no audible noise/distortion. ElevenLabs not configured/used. No human listening or full-speed playback claim.
- QA: controller and native /root/protrain_darija_ad_review viewed13 actual360x640 decoded frames incl0/cutboundaries/end. Arabic joined/single-line, face/contrast/CTA clear; approved short production test with no concrete visual blocker. Model's tracking suggestion rejected to preserve Arabic joining. Initial false clipping test fixed: equal-powerstereo→mono adds3dB; actual per-channel peak.842753 and source/outputcorr.9999787. Final verification.json uses arithmetic average.
- Source/evidence:editing-system/DARIJA_AD_REVIEW_20261113.md;video-studio/src/DarijaAd.tsx; scripts/{gemini-ad-voice.py,darija-ad-render.mjs,verify-darija-ad.py};public/darija-ad assets/prompts/speechmetadata;out/darija-ad-qa/{verification.json,export-review.json,overview.jpg,contact.jpg}. Generated photo is illustrative, blank books convey study not product evidence. Style remains owner-review pending, not proven ad performance or live-placement-certified.
- Runtime: separate512MB Node bundle/render,concurrency1,256MBmedia cache (minimum240MB with @remotion/media). SandboxlocalhostChromium EACCES resolved elevated; no packages installed. IAB preview timed out, CUA completion summarized, own Studio stopped beforeexport. Transient Gemini503/timeouts and retired model404 resolved using available3.1FlashLite assessment. No NotebookLM, campaign, publication, external messages, payment setup or network indexing.
- Next action: user watches this exact short ad, then refine chosen style from concrete feedback before applying to approved01–09 scripts. Reuse assets/voice; do not present earlier rejected template edits as approved or re-search same setup.

Native dispatchf34c16bb869f40e2a51785fdbbaebff1 finished after source and actual-frame review. Graphify remains stale/unrefreshed; no new corpus sent.

'''
p=memory/'CURRENT.md'
text=p.read_text(encoding='utf-8-sig')
if '## Narrated Darija ad completed — 13 November 2026' not in text:p.write_text(checkpoint+text,encoding='utf-8')

updates={
'DECISIONS.md':'''\n\n## Short narrated ad and API generation — 13 November 2026

Owner explicitly authorizes an actual≤10second ProTrain ad with generated Moroccan Darija speech using existing ElevenLabs/Google AI Studio APIs, generated raster assets, real brand colors and self-critique/correction before delivery. Existing Gemini key used in memory only; genericKore voice, not cloned.3takes, corrected product articulation, filtered/normalized audio;9.5sec actual ad exported. Keep generated illustrations distinct from testimonials and real UI/proof. Model actualMP4 audio/visual review plus independent decoded-frame review are evidence, not human listening, owner taste approval, measured ad performance or launch authorization. No publishing/contact/campaign/billing changes. Preserve generated media outside git/corpus and generic methods in shared skill library.
''',
'CONTEXT_INDEX.md':'''\n\n## Narrated Darija ad — 13 November 2026

- `04 — SaaS & EdTech/editing-system/DARIJA_AD_REVIEW_20261113.md`: corrections, review scope,9.5sec output and reproduction.
- `04 — SaaS & EdTech/editing-system/video-studio/out/protrain-match-darija-final.mp4`: exact final local delivery; generated student imagery/voice.
- Studio `src/DarijaAd.tsx`, `public/darija-ad/`, `scripts/{gemini-ad-voice.py,darija-ad-render.mjs,verify-darija-ad.py}` and `out/darija-ad-qa/`: editable source/assets/voiceprovenance and actual export evidence. Source audio available locally, ignored by git. User style approval pending.
''',
'PROJECT_CONTEXT.md':'''\n\n## Current video capability — 13 November 2026

The local Remotion/FFmpeg editing backend now produced a real9.5second ProTrain Match ad with generated Moroccan Darija speech and photographic imagery using extracted brand tokens, original logo and Cairo Arabic. Existing authorized GeminiAPI used; no ElevenLabs integration installed. Product-name articulation corrected across3takes, actual export reviewed via model audio/vision and independent decoded frames. This updates earlier statements that no narrated Darija edit exists. It does not establish owner taste approval, measured advertising performance, real Hajj/student footage, productUI demonstrations, launch readiness or human listening verification. See component review report; do not reinitialize toolchain or regenerate assets unnecessarily.
'''
}
for name,addition in updates.items():
    p=memory/name
    old=p.read_text(encoding='utf-8-sig')
    if addition.strip().splitlines()[0] not in old:p.write_text(old+addition,encoding='utf-8')
print('Updated selected protrain checkpoint and four canonical memories')

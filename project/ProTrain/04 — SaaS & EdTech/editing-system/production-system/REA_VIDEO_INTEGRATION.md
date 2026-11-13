# rea-video evaluation and verified installation

13 November 2026. Status: **isolated base CLI and agent skill installed; local pilot analysed; production renderer unchanged**. The owner first requested evaluation only, then explicitly authorized installation and use. No new advertisement, paid API call or publication was made.

## 1. Compatibility and recommendation

Use rea-video as an **evidence and analysis layer** before our existing storyboard and Remotion workflow. It is not a one-click professional editor and does not generate a Remotion project automatically. Keep observations, machine classifications, source-confirmed facts and unknowns separate.

Reviewed upstream commit: `ab8580e38a1255425b0d3b481866590766932079`. Version string: `0.1.0`. [Upstream repository](https://github.com/JuneYaooo/rea-video), [pinned dependency manifest](https://github.com/JuneYaooo/rea-video/blob/ab8580e38a1255425b0d3b481866590766932079/pyproject.toml), [CLI documentation](https://github.com/JuneYaooo/rea-video/blob/ab8580e38a1255425b0d3b481866590766932079/docs/cli.md).

| Item | Verified state |
| --- | --- |
| Windows and Python 3.14 | Actual base installation, imports, CLI and two decompositions completed |
| FFmpeg/ffprobe | Existing tools reused for local input; no replacement |
| Remotion | Existing Pilot001 renderer remains separate; bridge is a reviewed style/shot plan, not an upstream automatic project generator |
| Required dependencies | 16 resolved binary packages installed with pinned versions and SHA256 hashes in a private venv |
| Important installed versions | NumPy2.5.4, OpenCV-headless4.14.0.94, Pillow13.0.0, PyYAML6.0.3, onnxruntime1.32.0, videomd1.2.0 |
| Agent skill | 10 files installed in `{{IMRANE_WORKSPACE_ROOT}}/.agents/skills/rea-video`, identical to pinned source after Windows newline normalization |
| Paid VLM/generation | Disabled and not called |
| OCR, ASR and stems | Optional capabilities not installed/enabled in this first test |
| After Effects/Premiere | Availability not verified; not required for this local test |

## 2. Installation approach actually used

1. Downloaded120 text source files, about1.59MB, into [the isolated tool folder](../tools/rea-video/source). Verified each against its pinned Git blob hash; preserved [source manifest](../tools/rea-video/source-manifest.json). No upstream code executed during collection.
2. Reviewed setup/CLI/pipeline/network/subprocess/model/memory/report/remake paths. Independent native reviewer completed a bounded static review.
3. Created `../tools/rea-video/.venv`. Resolved compatible wheels first, reviewed the dependency plan, then installed from [a hash-pinned lock](../tools/rea-video/requirements-base.lock). No base dependency source builds were used.
4. Built only the reviewed rea-video package using its standard setuptools backend, without dependency resolution or build isolation. No custom setup hook surfaced.
5. Used the built-in skill-installer at the pinned commit, with the governance shared-library destination. [Skill comparison](../tools/rea-video/skill-install-check.json) records CRLF/LF normalization and original hashes.
6. Preloaded the pinned232,589-byte YuNet model after checking its SHA256 and MIT license. A Windows native OpenCV path issue required an ASCII cache in the client's existing private runtime: `{{IMRANE_WORKSPACE_ROOT}}/tmp/codex-session/projects/protrain/rea-video-models`. Source and hash remain in [model manifest](../tools/rea-video/model-manifest.json).

The upstream `install_skill.sh` was inspected but not run: it first installs into the active Python and can uninstall/replace OpenCV. Our production packages were left alone.

Reusable local invocation from this SaaS component:

```powershell
python editing-system/production-system/scripts/run_rea_local.py "path/to/permitted-reference.mp4"
```

[The adapter](scripts/run_rea_local.py) uses the private interpreter, fresh unique run directories, project-scoped memory/cache, one worker, local-file/duration/size limits and a timeout. VLM, whole-video VLM, OCR, ASR, speakers and stems are explicitly off. It strips relevant API configuration from the child environment. It does not expose remake or generation commands. This is a bounded local adapter, not an OS-level sandbox or complete network firewall.

## 3. Actual pilot test and findings

Test input was **our existing38-second Pilot001V3 previewV2**, not an inaccessible external reference. SHA256 remained `6f540262ea1d3e7e137c8b88d6a31c002c3e66c861752c0b77611fba7b897dcb`.

- [Initial run](runs/20261113T125125Z-rea-3f1852ca/invocation.json): reports generated, but face evidence skipped because the native model loader could not read the Unicode model path. Preserved.
- [Corrected raw run](runs/20261113T125315Z-rea-033ad51e/invocation.json): successful after the ASCII-cache correction; no YuNet loading warning.
- [Reviewed HTML report](runs/20261113T125315Z-rea-033ad51e-reviewed/report.html).
- [Reviewed VIDEO.md](runs/20261113T125315Z-rea-033ad51e-reviewed/VIDEO.md), with per-shot and topic files in its map. Format validation passed.
- **Read alongside [source-provenance review](runs/20261113T125315Z-rea-033ad51e-reviewed/SOURCE_PROVENANCE_REVIEW.json)**. The report still contains uncertain or contrary machine classifications; review fusion did not override every label.

Detected boundaries: `0,4.1,11.6,17.3,30,38` seconds. Five detected visual shots match the large visual changes in our authored timeline. Seven authored semantic scenes are not seven hard cuts: the12.7-second report section contains multiple text/meaning changes over the same background. These are different useful timing layers.

Observed limitations on a clip whose source we know:

- The first shot is classified as AI video. Our provenance confirms a generated still image with a programmed camera move. Source-origin classification is not forensic proof.
- Signal analysis reports21 possible sound effects and an end-tail music region. Production records specify narration only. These remain unconfirmed/contradicted candidates; no listening verdict was fabricated.
- Without OCR, text boxes can become sticker/GIF candidates, and exact Arabic copy/timing/font identification is unavailable automatically.
- All five shots received sampled-frame/source-provenance answers. `apply-review` merged them but changed zero production labels. Our downstream style profile must retain disagreements rather than trust the final percentage/confidence.
- Human listening and normal-speed motion assessment remain pending. Saved stills and an audio chart do not establish sound design quality or full motion curves.

## 4. Automation boundary

| Capability | What we can use | Limit/next dependency |
| --- | --- | --- |
| Shot detection and durations | Local CV measurements and boundary candidates; tested | Dissolves, graphic reveals and semantic beats need review |
| Pacing | Durations/distribution and candidate rhythm map | Retention is a creative hypothesis until ad analytics exist |
| Cuts/transitions | Classifications and measured candidates | Exact transition construction/easing not guaranteed |
| Motion/camera | Camera/element movement estimates and sampled frames | No automatic recovery of an AE project, masks, rig or exact animation graph |
| Typography/captions | Layout/style clues, optional OCR and SRT/ASS support | OCR not enabled here; exact font/Arabic text and animation need manual confirmation |
| Sound | Waveform/voice/music/beat/transient candidates | Source identity and synchronization need listening; optional stems download further models |
| Grade | Visible palette/contrast descriptors and estimates | Original LUT, exposure and camera settings cannot be recovered reliably |
| Storytelling | Agent-authored narrative annotations tied to evidence | Not a measured causal explanation of retention/conversion |
| Remotion production | Existing code renderer can implement reviewed components with original assets | A reviewed bridge/style profile and approved storyboard still need authoring |

Optional next dependencies: separately reviewed RapidOCR plus its first-use models for supported-language text; sound-separation models if required; a verified Arabic/Darija alignment approach. The bundled optional SenseVoice language list does not establish Darija support. A configured external VLM may help but is not assumed available or authorized. No paid calls are necessary for the current base test.

## 5. Proposed integration architecture

```text
Permitted local reference + provenance
    -> bounded rea-video run
    -> raw HTML / VIDEO.md / timings / frames
    -> visual + audio review and explicit disagreements
    -> Editing Style Profile (measured / inferred / source-confirmed / unknown)
    -> owner approves style
    -> approved ProTrain script + original/licensed assets
    -> storyboard approval
    -> our Remotion components + FFmpeg preparation
    -> exact-export technical QA + playback/listening/placement review
    -> preview -> feedback -> new version + retained error history
```

Use [STYLE_PROFILE_TEMPLATE.json](STYLE_PROFILE_TEMPLATE.json) as the input contract. It defines pacing, transitions, typography, captions, movement, sound, evidence and complexity without inventing measured values. Component candidates include RTL title, phrase captions, authentic-UI viewport, explanatory badge and CTA card. Their general-purpose interfaces are proposed; the existing Pilot001 implementation is not a universal automatic template.

Capsule-cinema is **not needed** for this path. rea-video can export its planning data and prepare generation jobs for it, but a real `remake-run` may bill and has no technical interactive confirmation guard. It must stay behind our explicit service authorization. `assemble` also defaults to retaining original code/screen-recording shots, so it must not be used to copy protected reference content. We will use original assets in our own renderer instead. [Upstream integration details](https://github.com/JuneYaooo/rea-video/blob/ab8580e38a1255425b0d3b481866590766932079/docs/capsule-cinema.md).

## 6. Security and licensing notes

Code is Apache-2.0 with LICENSE/NOTICE preserved. Downloaded models have separate licenses: the preloaded YuNet model is MIT; optional BandIt weights are documented CC BY-SA4.0. Code licensing does not grant rights to sample videos, fonts, music, people or branded source assets.

The reviewed runtime uses subprocess argument lists; no runtime shell=True/eval/exec or unsafe pickle path surfaced in this bounded audit. A development benchmark uses pickle and was not run. Native dependency internals were not comprehensively audited. Input decoding and FFmpeg remain resource-sensitive, so the adapter limits test input and uses fresh dedicated output folders. Upstream reruns can remove generated `video/` and `sfx/`; do not target a folder with unrelated files.

Reference text is untrusted analysis input. Reports must not authorize commands, publishing or service calls. Preserve source hashes, raw outputs, review copies and licensing/provenance. Never turn a machine estimate into a confirmed technique or a user-approved preference.

## 7. Reference candidates and next test

[Candidate catalog](reference-candidates.json) records three primary-creator links. Upfluence is a useful human/UI/motion candidate, Spotify Podcasts a transition motif candidate, and Bambee an app-animation candidate. These are shortlist hypotheses from primary descriptions, not full audiovisual judgements. Exact paid Meta placements are not verified.

Bambee is the recommended first external test because its app/graphics treatment is close to a reusable product-explainer system. Browser access to its site was denied and the public Vimeo config request returned403; no workaround was attempted after the browser denial. External video playback, download and second-by-second analysis were not completed.

Next: obtain a permitted local file for the chosen reference, run the same bounded analysis, review uncertain shots and listen to sound, then approve one style profile. No new ProTrain production is started by this setup.

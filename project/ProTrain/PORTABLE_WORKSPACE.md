# ProTrain portable workspace

This private payload preserves the four ProTrain work lines, project memory, scripts, creative sources, review history, images, audio, videos, fonts with their supplied notices, and existing source archives. Exported media remain byte-identical to their original files. A packaged version is not a new creative approval. The latest memory and active creative record take precedence over historical technical checks.

## Start on another computer

Use the kit's top-level README and bootstrap script. It creates an independent workspace with this project at `projects/ProTrain`, one curated skill library and newly generated host paths. Open the installed workspace rather than the old `D:/PROJECTS` tree. System documentation is English; original client scripts and documents keep their original language and meaning.

Dependencies, user accounts, provider keys, plugin runtimes and browser installations are not transferred. The existing Remotion studio has its own package.json and lockfile under `04 — SaaS & EdTech/editing-system/video-studio`. Review its dependency plan before running package installation. No package installation or provider call is authorized merely by extracting or bootstrapping the kit.

## Export an existing HTML creative

The optional renderer below resolves normal project-local modules and uses Playwright's browser or your explicit `CHROME_PATH`. Review this optional plan before installing anything:

```powershell
# From the installed projects/ProTrain directory, after approving this dependency plan:
npm install
npx playwright install chromium

# Export to a NEW file. The approved/reviewed source and earlier PNG are preserved:
npm run render:static -- "04 — SaaS & EdTech/creatives/03-static-01-campus-confusion/v5/Creative01V5.html" --output "exports/Creative01V5-portable-check.png" --width 1080 --height 1350
```

The same commands work in a macOS terminal with Node/npm available. This is a render of an existing candidate, not approval of V5. A successful render still needs the task's actual visual and copy checks. Some historical Python scripts need separately reviewed Python dependencies.

## Historical paths and receipts

The portable copies use explicit workspace/project tokens, expanded during installation. Original archives and evidence records are historical source material. They can contain original-host paths such as Codex generated-image locations, Windows fonts, `D:/Campus`, `D:/Instagram`, and private runtime evidence that is not bundled. These references are not credentials and do not prove the referenced file is available on the new PC.

Use the included local assets where available. Existing legacy build scripts preserve their original behavior and can depend on original-host packages, proprietary Windows fonts or preservation hashes. Do not run those maintenance/checkpoint scripts blindly. The optional renderer above avoids the legacy Node/browser paths without changing their historical code or overwriting the original outputs. Font substitutions require a separate visual review, and proprietary fonts are not copied from Windows.

## Published content and backup

This repository includes client work because its owner explicitly requested a ProTrain-only transfer, then explicitly confirmed public publication. Toolkit and third-party licenses do not automatically license client assets for public redistribution. Preserve source notices and per-asset permissions. The owner explicitly requested public publication of this reviewed ProTrain snapshot. Public availability is not a blanket reuse license for client or third-party assets.

The kit and installed workspace are separate. Work in the installed project. Changes are not automatically uploaded to GitHub. Follow the top-level reviewed backup/sync instructions when moving completed project changes back into the kit, excluding secrets, dependency folders, host configs and caches.

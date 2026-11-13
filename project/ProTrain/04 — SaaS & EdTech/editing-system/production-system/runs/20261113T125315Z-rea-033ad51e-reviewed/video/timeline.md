---
videomd: 1
part: timeline
shots: 5
tokens: 551
---

# Timeline

One shot per line: `#<n> start-end (s) | key value | …`. A key ending in `~` is the tools' inference; keys without it are visible on screen or measured directly.
`story` job in the story and the point · `seen` what is on screen · `camera` camera move · `overlay` overlays · `made~` how it was made (inferred) · `material~` where the material came from (inferred) · `remake` remake route · `flag` needs a second look
Full detail for a shot is in `video/shots/<n>.md` (e.g. `video/shots/07.md`).

```videomd-timeline
#01 0.0-4.1 | story grab attention, Identify the formation-choice pr… | seen Fictional student photograph with a subtle whole-image push-… | camera static | overlay graphic, static sticker | made~ AI-generated video 38% · runner-up 3D render 34% | material~ AI-generated | remake AI generation · G1 | flag low confidence,to confirm
#02 4.1-11.6 | story set the scene, Explain why the academic profile … | seen Ivory explanatory graphic connects the academic profile with… | camera static | made~ code / template render 94% · runner-up 3D render 3% | material~ mixed (includes real material): logo / b… | remake code render · Part 1
#03 11.6-17.3 | story add information, Show the free academic-profile … | seen Green title and free-profile badge above a genuine cropped f… | camera static | transition jump cut | overlay animated sticker / GIF | made~ code / template render 93% · runner-up 3D render 3% | material~ mixed (includes real material): UI scree… | remake code render · Part 1
#04 17.3-30.0 | story add information, Explain the proposed report con… | seen Physical-folder still illustration with sequential report-va… | camera static | overlay animated sticker / GIF | made~ code / template render 89% · runner-up 3D render 3% | material~ rendered by the creator | remake code render · Part 1
#05 30.0-38.0 | story call to action, Invite the viewer to complete th… | seen Green end card separates free-profile entry, full-report off… | camera static | made~ code / template render 94% · runner-up 2D animation 2% | material~ mixed (includes real material): logo / b… | remake code render · Part 1
```

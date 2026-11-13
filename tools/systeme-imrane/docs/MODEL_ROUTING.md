# Six-level model routing

Routing selects a worker model and effort; it does not change the active controller model, host permissions or service tier. This owner-requested private kit configures:

| Level | Route | Model | Effort |
| --- | --- | --- | --- |
| 1 mechanical | mechanical_safe | gpt-6-luna | low |
| 2 simple | fast_safe | gpt-6-luna | medium |
| 3 bounded | focused_safe | gpt-6-luna | high |
| 4 intermediate | balanced_safe | gpt-6.1-sol | low |
| 5 complex | standard_safe | gpt-6.1-sol | medium |
| 6 critical | deep_safe | gpt-6.1-sol | high |

Assess actual uncertainty, dependencies, risk/reversibility and validation. An unknown task defaults to standard_safe. The deterministic classifier is a conservative recommendation, not proof of scope. Short continuations preserve the route; new risk can raise it; two reported failures in the same task escalate to deep_safe. Explicit leading route tags override the default within permission boundaries.

The controller calls tools/imrane-route.py with JSON stdin, a stable session id and an opaque task id. It starts one real native worker with the returned model/effort, records the actual started receipt, waits and verifies the result, then records finished/failed. Workers never delegate. A plan is not a launch receipt. Report missing model/delegation capabilities; never silently substitute. Automatic adapters permit only Luna/Sol and efforts no higher than high. No automatic Max/Ultra or service-tier changes.

Six Codex role files are generated at governance and in ProTrain. Actual support and account access require local verification. Claude bindings are unset and advisory. Hooks add scoped context and routing recommendations only; they do not launch workers or change the active model. Reload the local clients and observe real hooks/roles before claiming native support.

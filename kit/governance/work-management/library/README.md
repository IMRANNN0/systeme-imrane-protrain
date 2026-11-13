# Reviewed method library

This shared library contains reusable working methods and fully synthetic examples. Client records, source screenshots, customer data and private financial figures do not belong here.

Use the templates in `../templates` for a new assignment. [examples.json](examples.json) shows accepted and rejected reasoning from the installation pilot, with review, context and limitations. A rejected example is a learning example, not an instruction to perform the rejected action.

To add a real lesson:

1. Keep the original evidence in its source lane and draft the contextual lesson there.
2. Review the evidence and the proposed change; name the reviewer and actual date.
3. Sanitize the exact text and export only the selected reviewed lesson locally.
4. For a cross-lane promotion, obtain the handoff authorization required by `HANDOFF_POLICY.md`. Review what would be copied, not just a sanitization flag.
5. Add a reviewed generic example or deliberately update the relevant template/skill. Preserve provenance, limitations and rejected alternatives. Run checks appropriate to that actual change.

The CLI never performs step 4 or 5 automatically. There is no background ingestion of client results, autonomous skill rewrite or assumption that a successful case applies everywhere.

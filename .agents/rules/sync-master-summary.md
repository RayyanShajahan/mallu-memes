---
trigger: always_on
---

# Mandatory Project Master Summary Synchronization Rule

Whenever ANY change, file edit, addition, deletion, endpoint update, schema modification, dependency change, scoring heuristic update, or feature implementation is made to this codebase, the agent MUST automatically update `PROJECT_MASTER_SUMMARY.md` in the same turn before concluding its response.

### Strict Invariants:
1. **Never Forget**: `PROJECT_MASTER_SUMMARY.md` is the Single Source of Truth (SSOT) for all teammates. It must never fall out of sync with the actual state of the repository.
2. **Automatic Execution**: Do not wait for the user to ask to update the summary. Any code modification, configuration change, or new service requires updating `PROJECT_MASTER_SUMMARY.md`.
3. **Extreme Technical Detail**: Ensure all changes are documented in detail, including affected scripts, scoring algorithms, metric formulas, schemas, and execution runbooks.
4. **Changelog & Milestones**: Append or update the relevant milestone/changelog entry in `PROJECT_MASTER_SUMMARY.md` reflecting the exact changes made.

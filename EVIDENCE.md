# Acceptance evidence

## GitHub PR exercise

[PR #1](https://github.com/ai-platform-portfolio/engineering-acceptance/pull/1)
adds a raw Terraform resource, then replaces it with a commit-pinned module call.
Neither revision applies infrastructure.

| Revision | Quality result | Evidence |
|---|---|---|
| `9b79cac` | Rejected with `TF001` at `gate-example/terraform/rejected.tf:1` | [Failed job](https://github.com/ai-platform-portfolio/engineering-acceptance/actions/runs/36258706260/job/108450279832) |
| `71bb468` | Passed after switching to the approved identity module | [Corrected job](https://github.com/ai-platform-portfolio/engineering-acceptance/actions/runs/36258789065/job/108450503868) |

The first complete [acceptance run](https://github.com/ai-platform-portfolio/engineering-acceptance/actions/runs/36258689042)
passed all 28 original cases on Linux. The subsequent gitignore regression adds
a 29th case: tracked source remains checked even if the candidate ignores it.
CI artifacts contain each case's expected and actual findings.

The gitignore case initially failed because jscpd honoured the consumer ignore
file. The corrected policy supplies its own configuration and scans the explicit
source list. Ruff also ignores consumer gitignore exclusions. The local regression
passed after this correction.

## Merge enforcement

The original runs above occurred while this repository was private on GitHub
Free and its protection API returned HTTP 403. They prove detection and
correction, not blocked merging at that time. Current visibility and merge
controls are tracked separately in the audited
[portfolio governance status](https://github.com/ai-platform-portfolio/engineering-standards#ci-and-enforcement-status).

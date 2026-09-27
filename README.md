# Engineering acceptance

Whole-change acceptance tests for `engineering-standards`. Each case applies a
patch to the clean reference tree and runs the actual pinned quality tools.

With a sibling standards checkout, run `make -C ../engineering-standards tools`,
then `make test`. Results are written to `reports/acceptance.json`.

Each `cases/<name>/expected.json` specifies the required exit code, report status
and findings. Every expected finding must appear, and unexpected findings fail
the case. A checker crash cannot satisfy a case expecting a duplicate-code failure.
Fixtures use temporary Git tree objects; the runner does not sign commits or
manage signing keys.

The reference Terraform source is a static policy fixture. Acceptance does not
initialise or apply its resources. Actual module configuration validation and
mocked provider tests run in `terraform-modules`.

The suite checks duplication against unchanged source, correct reuse, dependency
boundaries, type errors, comment budgets, approved Terraform sources and tool
failures. It does not claim to recognise all semantic duplication.

The `gate-example` directory is a standalone consumer for the GitHub PR exercise.
Its check uses a pinned standards action and the base revision's policy.
Protected files can change only after a base CODEOWNER approves the exact PR
head. The review workflow reruns the original quality job, preserving one check.
The checker verifies that approval before adopting the proposed policy.
See [evidence](EVIDENCE.md) for the failed and corrected job links.

Repository visibility and merge controls are recorded in the automatically
checked [portfolio governance status](https://github.com/ai-platform-portfolio/engineering-standards#ci-and-enforcement-status).
That read-only audit detects drift between the documented expectations and live
GitHub settings. Acceptance runs demonstrate the checker behaviour; repository
rules provide the separate merge gate. No cloud credentials are used by this suite.

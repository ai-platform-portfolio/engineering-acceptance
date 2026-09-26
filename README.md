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

GitHub Free currently prevents branch protection on these private repos. Workflow
results can demonstrate detection, but blocked merging cannot be demonstrated
until the organisation enables that capability. No cloud credentials are used.

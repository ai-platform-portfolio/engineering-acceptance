import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


def run(*command, cwd):
    return subprocess.run(command, cwd=cwd, check=True, capture_output=True, text=True)


def matches(expected, actual):
    return all(actual.get(key) == value for key, value in expected.items())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checker", required=True)
    parser.add_argument("--tools", required=True)
    parser.add_argument("--report", default="reports/acceptance.json")
    parser.add_argument(
        "--case", action="append", help="Run only the named acceptance case (repeatable)"
    )
    args = parser.parse_args()
    repository = Path(__file__).resolve().parent.parent
    results = []
    cases = sorted((repository / "cases").iterdir())
    if args.case:
        unknown = set(args.case) - {case.name for case in cases}
        if unknown:
            parser.error("Unknown cases: " + ", ".join(sorted(unknown)))
        cases = [case for case in cases if case.name in args.case]
    for case in cases:
        expected = json.loads((case / "expected.json").read_text())
        with tempfile.TemporaryDirectory(prefix="engineering-acceptance-") as directory:
            root = Path(directory)
            shutil.copytree(repository / "reference", root, dirs_exist_ok=True)
            if (case / "baseline").exists():
                shutil.copytree(case / "baseline", root, dirs_exist_ok=True)
            run("git", "init", "-q", cwd=root)
            run("git", "add", ".", cwd=root)
            # A tree object supplies a baseline without creating or signing a commit.
            tree = run("git", "write-tree", cwd=root).stdout.strip()
            patch = case / "change.patch"
            if patch.exists():
                run("git", "apply", "--index", str(patch), cwd=root)
            report = root / "findings.json"
            command = [
                args.checker,
                "--root",
                str(root),
                "--base",
                tree,
                "--tools",
                args.tools,
                "--report",
                str(report),
            ]
            if expected.get("tool_failure"):
                command[command.index("--tools") + 1] = str(root / "missing-tools")
            completed = subprocess.run(command, text=True, capture_output=True)
            actual = (
                json.loads(report.read_text()) if report.exists() else {"status": "missing-report"}
            )
            findings = actual.get("findings", [])
            required = expected.get("findings", [])
            passed = (
                completed.returncode == expected["exit"]
                and actual["status"] == expected["status"]
                and all(any(matches(item, found) for found in findings) for item in required)
                and all(any(matches(item, found) for item in required) for found in findings)
            )
            results.append(
                {"case": case.name, "passed": passed, "expected": expected, "actual": actual}
            )
            print(f"{'PASS' if passed else 'FAIL'} {case.name}")
            if not passed:
                print(completed.stdout + completed.stderr)
    output = repository / args.report
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(results, indent=2) + "\n")
    return int(any(not result["passed"] for result in results))


if __name__ == "__main__":
    raise SystemExit(main())

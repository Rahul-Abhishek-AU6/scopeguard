import argparse
from .policy import load
from .git import changed_paths
from .evaluate import evaluate
from .render import write

def main():
    parser = argparse.ArgumentParser(prog="scopeguard")
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check"); check.add_argument("--policy", required=True); check.add_argument("--output-dir", default="evidence"); check.add_argument("--staged", action="store_true")
    args = parser.parse_args()
    try:
        policy = load(args.policy); paths = changed_paths(args.staged)
        changed, violations, warnings = evaluate(paths, policy)
        result = write(args.output_dir, "staged" if args.staged else "working-tree", changed, violations, warnings, policy["required_tests"])
        print(f"Scopeguard: {result['status']} ({len(changed)} path(s), {len(violations)} violation(s))")
        return 0 if result["status"] == "pass" else 1
    except ValueError as exc:
        parser.error(str(exc))
if __name__ == "__main__": raise SystemExit(main())

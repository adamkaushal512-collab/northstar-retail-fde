import argparse
import json
from pathlib import Path

from .red_team import run_red_team


def main() -> None:
    parser = argparse.ArgumentParser(description="Run NorthStar Phase 12 red-team scenarios")
    parser.add_argument("--repo-root", default="../..")
    args = parser.parse_args()

    root = Path(args.repo_root).resolve()
    report = run_red_team(
        root / "data/red-team/red-team-cases.json",
        base_payload_path=root / "data/examples/bopis-inventory-discrepancy.json",
        approved_policy_path=root / "data/policies/bopis-inventory-investigation.md",
        repo_root=root,
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

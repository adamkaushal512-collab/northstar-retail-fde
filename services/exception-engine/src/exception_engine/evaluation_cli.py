import argparse
import json

from .evaluation import run_evaluation


def main() -> None:
    parser = argparse.ArgumentParser(description="Run NorthStar investigation evaluations")
    parser.add_argument("--cases", required=True)
    parser.add_argument("--payload", required=True)
    parser.add_argument("--policy", required=True)
    args = parser.parse_args()
    report = run_evaluation(
        args.cases,
        base_payload_path=args.payload,
        policy_path=args.policy,
    )
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["pass_rate"] == 1.0 else 1)


if __name__ == "__main__":
    main()

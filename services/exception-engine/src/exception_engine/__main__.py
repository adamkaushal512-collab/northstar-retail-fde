import argparse
import json

from .prototype import PrototypeInputError, process_file


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the NorthStar BOPIS exception-engine prototype."
    )
    parser.add_argument("input_file", help="Path to a canonical JSON input file")
    args = parser.parse_args()

    try:
        result = process_file(args.input_file)
    except (OSError, json.JSONDecodeError, PrototypeInputError) as exc:
        parser.error(str(exc))

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

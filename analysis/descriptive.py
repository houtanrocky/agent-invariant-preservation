"""Print descriptive summaries only for explicitly supplied, validated data."""

import sys

from researchctl.cli import main

if __name__ == "__main__":
    raise SystemExit(main(["summarize", *sys.argv[1:]]))

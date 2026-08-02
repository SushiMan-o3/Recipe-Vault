"""Run the whole backend test suite.

    python tests/run_tests.py           # everything
    python tests/run_tests.py -k login  # pass any extra pytest flags through

No database is required - conftest.py swaps the Postgres layer for an in-memory fake.
"""

import subprocess
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
TESTS_DIR = BACKEND_DIR / "tests"


def main(argv=None):
    args = list(argv if argv is not None else sys.argv[1:])
    command = [sys.executable, "-m", "pytest", str(TESTS_DIR), "-v"] + args
    return subprocess.call(command, cwd=str(BACKEND_DIR))


if __name__ == "__main__":
    raise SystemExit(main())

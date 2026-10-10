"""
Compare CLI startup with lazy imports on and forced off.

Usage:
    uv run python scripts/bench_imports.py
    uv run python scripts/bench_imports.py --runs 30

The eager baseline relies on `sys.set_lazy_imports_filter`, which is still
young; if the API changes, only this script needs updating, not the tests.
"""

import argparse
import re
import statistics
import subprocess
import sys
import time

FORCE_EAGER = "import sys\nsys.set_lazy_imports_filter(lambda *_: False)\n"
MODES = {"lazy": "", "eager": FORCE_EAGER}

HELP = """\
import sys
sys.argv = ["page-refresher", "--help"]
from page_refresher.main import app
app()
"""


def run(code: str, *flags: str) -> subprocess.CompletedProcess[str]:
    """
    Run `code` in a fresh interpreter with extra interpreter `flags`.

    Returns:
        The finished process, with its output captured.
    """
    return subprocess.run(
        [sys.executable, *flags, "-c", code],
        capture_output=True,
        text=True,
        check=False,
    )


def module_count(prelude: str) -> int:
    """
    Count modules loaded by importing the CLI.

    Returns:
        The size of `sys.modules` after `import page_refresher.main`.
    """
    code = f"{prelude}import page_refresher.main, sys\nprint(len(sys.modules))"
    return int(run(code).stdout)


def import_time_ms(prelude: str) -> float:
    """
    Measure how long importing the CLI takes.

    Returns:
        The cumulative `-X importtime` figure for `page_refresher.main`.

    Raises:
        RuntimeError: The module is missing from the `-X importtime` output.
    """
    stderr = run(f"{prelude}import page_refresher.main", "-X", "importtime").stderr
    match = re.search(r"\|\s*(\d+) \|\s*page_refresher\.main$", stderr, re.MULTILINE)
    if match is None:
        msg = "page_refresher.main missing from -X importtime output"
        raise RuntimeError(msg)
    return int(match.group(1)) / 1000


def help_time_ms(prelude: str, runs: int) -> float:
    """
    Time `page-refresher --help` end to end.

    Returns:
        The median wall time over `runs` runs.
    """
    times = []
    for _ in range(runs):
        start = time.perf_counter()
        run(prelude + HELP)
        times.append(time.perf_counter() - start)
    return statistics.median(times) * 1000


def main() -> None:
    """Print module count, import time and `--help` time for each mode."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("--runs", type=int, default=15, help="--help runs per mode")
    args = parser.parse_args()

    if not hasattr(sys, "set_lazy_imports_filter"):
        sys.exit("needs Python 3.15+ with sys.set_lazy_imports_filter")

    print(f"{'mode':<6} {'modules':>8} {'import (ms)':>12} {'--help (ms)':>12}")
    for name, prelude in MODES.items():
        print(
            f"{name:<6} {module_count(prelude):>8} {import_time_ms(prelude):>12.1f}"
            f" {help_time_ms(prelude, args.runs):>12.0f}"
        )


if __name__ == "__main__":
    main()

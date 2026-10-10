"""
Guard the startup savings from lazy imports (PEP 810).

Nothing breaks when a lazy import turns eager, the CLI just gets slower, so
these tests check which heavy modules end up in `sys.modules`. Each probe runs
in a fresh interpreter, since the test process may already have imported them.
"""

import json
import subprocess
import sys

import pytest

SELENIUM = ("selenium", "webdriver_manager")
ADAPTERS = {"flet": "flet", "nicegui": "nicegui", "tkinter": "customtkinter"}
HEAVY = (*SELENIUM, *ADAPTERS.values())

# Rejecting every lazy import makes the process behave as if `lazy` were absent.
FORCE_EAGER = "import sys\nsys.set_lazy_imports_filter(lambda *_: False)\n"

HELP = """\
from page_refresher.main import app
try:
    app({args!r}, prog_name="page-refresher")
except SystemExit:
    pass
"""


def loaded_heavy_modules(code: str) -> list[str]:
    """
    Run `code` in a fresh interpreter.

    Returns:
        The modules from `HEAVY` it left in `sys.modules`.
    """
    report = f"print(json.dumps([m for m in {HEAVY!r} if m in sys.modules]))"
    probe = f"{code}\nimport json, sys\n{report}\n"
    result = subprocess.run(
        [sys.executable, "-c", probe], capture_output=True, text=True, check=True
    )
    return json.loads(result.stdout.splitlines()[-1])


@pytest.mark.parametrize(
    "code",
    [
        pytest.param("import page_refresher", id="import-package"),
        pytest.param("import page_refresher.main", id="import-cli"),
        pytest.param(HELP.format(args=["--help"]), id="help"),
        pytest.param(HELP.format(args=["refresh", "--help"]), id="refresh-help"),
        pytest.param(HELP.format(args=["run", "--help"]), id="run-help"),
    ],
)
def test_startup_loads_no_heavy_modules(code: str) -> None:
    assert loaded_heavy_modules(code) == []


@pytest.mark.parametrize("adapter", ADAPTERS)
def test_loading_an_adapter_loads_only_its_toolkit(adapter: str) -> None:
    code = (
        "from page_refresher.main import Adapter, _load_adapter\n"
        f"_load_adapter(Adapter({adapter!r}))\n"
    )
    loaded = set(loaded_heavy_modules(code))
    assert ADAPTERS[adapter] in loaded
    assert loaded.isdisjoint(set(ADAPTERS.values()) - {ADAPTERS[adapter]})


@pytest.mark.skipif(
    not hasattr(sys, "set_lazy_imports_filter"),
    reason="needs sys.set_lazy_imports_filter to force eager imports",
)
def test_probe_detects_eager_imports() -> None:
    """Without this, an always-empty probe would make the tests above pass."""
    assert set(loaded_heavy_modules(FORCE_EAGER + "import page_refresher.main")) == set(
        HEAVY
    )

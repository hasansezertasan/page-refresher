"""Typer CLI for Page Refresher."""

from enum import StrEnum
from typing import Annotated
lazy from collections.abc import Callable

import typer

# Lazy: Selenium and the driver manager are heavy, and only some commands need them.
lazy from selenium import webdriver
lazy from selenium.webdriver.chrome.service import Service
lazy from webdriver_manager.chrome import ChromeDriverManager

from page_refresher import SeleniumRefresher

# Lazy: each adapter's GUI dependency is optional, so only the chosen one loads.
lazy from page_refresher.adapters.flet import main as run_flet
lazy from page_refresher.adapters.nicegui import main as run_nicegui
lazy from page_refresher.adapters.tkinter import main as run_tkinter


class Adapter(StrEnum):
    """GUI frontends that can be launched with the `run` command."""

    FLET = "flet"
    NICEGUI = "nicegui"
    TKINTER = "tkinter"


app = typer.Typer(name="Page Refresher Toolbox", add_completion=True)


@app.command(
    help="Install Chrome Driver",
    short_help="Install Chrome Driver for current Chrome version",
    hidden=False,
    add_help_option=True,
)
def install_chrome_driver() -> None:
    """
    Install Chrome Driver.

    Usage:
        page-refresher install-chrome-driver
    """
    typer.echo(ChromeDriverManager().install())


@app.command(
    help="Page Refresher CLI",
    short_help="Page Refresher CLI",
    hidden=False,
    add_help_option=True,
)
def refresh(
    url: str = typer.Option(
        ..., "-u", "--url", help="URL to refresh", prompt="URL to refresh"
    ),
    delay: int = typer.Option(
        ...,
        "-d",
        "--delay",
        help="Delay between refreshes",
        prompt="Delay between refreshes",
    ),
    refresh_count: int = typer.Option(
        ...,
        "-r",
        "--refresh-count",
        help="Number of refreshes",
        prompt="Number of refreshes",
    ),
) -> None:
    """
    Page Refresher CLI.

    Usage:
        page-refresher refresh
        page-refresher refresh --url https://example.com --delay 5 --refresh-count 10
    """
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    refresher = SeleniumRefresher(driver, url, delay, refresh_count)
    refresher.refresh()


def _load_adapter(adapter: Adapter) -> Callable[[], None]:
    """
    Import the adapter by touching its lazy name.

    Returns:
        The adapter's `main` entry point.
    """
    match adapter:
        case Adapter.FLET:
            return run_flet
        case Adapter.NICEGUI:
            return run_nicegui
        case Adapter.TKINTER:
            return run_tkinter


@app.command(
    help="Run a GUI adapter",
    short_help="Launch the given GUI frontend",
    hidden=False,
    add_help_option=True,
)
def run(
    adapter: Annotated[Adapter, typer.Argument(help="GUI adapter to launch")],
) -> None:
    """
    Run a GUI adapter.

    Usage:
        page-refresher run tkinter
        page-refresher run flet
        page-refresher run nicegui

    Raises:
        BadParameter: The adapter's optional extra is not installed.
    """
    try:
        launch = _load_adapter(adapter)
    except ModuleNotFoundError as exc:
        msg = f"missing module {exc.name!r}; install it with: uv sync --extra {adapter}"
        raise typer.BadParameter(msg, param_hint="adapter") from exc
    launch()

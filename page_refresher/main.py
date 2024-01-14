import typer
from webdriver_manager.chrome import ChromeDriverManager

from page_refresher import SeleniumRefresher


app = typer.Typer(
    name="Page Refresher Toolbox",
    add_completion=True,
)


@app.command(
    help="Install Chrome Driver",
    short_help="Install Chrome Driver for current Chrome version",
    hidden=False,
    add_help_option=True,
)
def install_chrome_driver():
    """
    Install Chrome Driver

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
        ...,
        "-u",
        "--url",
        help="URL to refresh",
        prompt="URL to refresh",
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
):
    """
    Page Refresher CLI

    Usage:
        page-refresher refresh
        page-refresher refresh --url https://example.com --delay 5 --refresh-count 10
    """
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    refresher = SeleniumRefresher(driver, url, delay, refresh_count)
    refresher.refresh()

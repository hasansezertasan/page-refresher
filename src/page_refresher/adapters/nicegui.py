from nicegui import run, ui
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from page_refresher.core.refresher import SeleniumRefresher

refresher: SeleniumRefresher | None = None
driver: webdriver.Chrome | None = None


def _do_refresh(r: SeleniumRefresher) -> None:
    r.refresh()


async def start_click() -> None:
    global driver, refresher  # noqa: PLW0603
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    refresher = SeleniumRefresher(
        driver,
        url_input.value or "",
        int(delay_input.value or 5),
        int(count_input.value or 1),
    )
    status.set_text("Running...")
    await run.io_bound(_do_refresh, refresher)
    status.set_text("Done.")


def stop_click() -> None:
    if refresher is not None:
        refresher.stop()
    status.set_text("Stopped.")


url_input = ui.input("Target URL").classes("w-full")
with ui.row():
    delay_input = ui.number("Refresh Delay (seconds)", value=5)
    count_input = ui.number("Refresh Count", value=1)
with ui.row():
    ui.button("Start", on_click=start_click)
    ui.button("Stop", on_click=stop_click)
status = ui.label("")


def main() -> None:
    ui.run(title="Page Refresher")

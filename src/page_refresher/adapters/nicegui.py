from nicegui import run, ui

from page_refresher.core.refresher import SeleniumRefresher


def root() -> None:
    """Build the page; NiceGUI calls this once per client, so state stays per client."""
    refresher: SeleniumRefresher | None = None

    async def start_click() -> None:
        nonlocal refresher
        if refresher is not None:
            refresher.stop()
        refresher = current = SeleniumRefresher(
            url_input.value or "",
            int(delay_input.value or 5),
            int(count_input.value or 1),
        )
        status.set_text("Running...")
        # Chrome startup and the refresh loop both run off the event loop.
        await run.io_bound(current.refresh)
        if current is refresher and not current.stopped:
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
    # No auto-reload: it re-runs the CLI entry script, which never calls ui.run().
    ui.run(root, title="Page Refresher", reload=False)

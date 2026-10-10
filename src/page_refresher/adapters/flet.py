import flet as ft

from page_refresher.core.refresher import SeleniumRefresher


def main() -> None:
    def app(page: ft.Page) -> None:
        page.title = "Page Refresher"
        page.window.width = 600
        page.window.height = 400

        refresher: SeleniumRefresher | None = None

        url_field = ft.TextField(label="Target URL", expand=True)
        delay_field = ft.TextField(label="Refresh Delay (seconds)", width=200)
        count_field = ft.TextField(label="Refresh Count", width=200)
        status = ft.Text(value="", color=ft.Colors.GREY)

        def run_refresh(run: SeleniumRefresher) -> None:
            # Runs on a worker thread, so Chrome startup doesn't block the page.
            run.refresh()
            if run is refresher and not run.stopped:
                status.value = "Done."
                page.update()

        def start_click(e: ft.ControlEvent) -> None:
            nonlocal refresher
            if refresher is not None:
                refresher.stop()
            refresher = SeleniumRefresher(
                url_field.value or "",
                int(delay_field.value or "5"),
                int(count_field.value or "1"),
            )
            status.value = "Running..."
            page.update()
            page.run_thread(run_refresh, refresher)

        def stop_click(e: ft.ControlEvent) -> None:
            if refresher is not None:
                refresher.stop()
            status.value = "Stopped."
            page.update()

        page.add(
            url_field,
            ft.Row([delay_field, count_field]),
            ft.Row([
                ft.Button("Start", on_click=start_click),
                ft.Button("Stop", on_click=stop_click),
            ]),
            status,
        )

    ft.run(app)

import threading

import flet as ft
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from page_refresher.core.refresher import SeleniumRefresher


def main() -> None:
    def app(page: ft.Page) -> None:
        page.title = "Page Refresher"
        page.window.width = 600
        page.window.height = 400

        refresher: SeleniumRefresher | None = None
        driver: webdriver.Chrome | None = None

        url_field = ft.TextField(label="Target URL", expand=True)
        delay_field = ft.TextField(label="Refresh Delay (seconds)", width=200)
        count_field = ft.TextField(label="Refresh Count", width=200)
        status = ft.Text(value="", color=ft.Colors.GREY)

        def run_refresh() -> None:
            nonlocal refresher
            if refresher is None:
                return
            refresher.refresh()
            status.value = "Done."
            page.update()

        def start_click(e: ft.ControlEvent) -> None:
            nonlocal driver, refresher
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            refresher = SeleniumRefresher(
                driver,
                url_field.value or "",
                int(delay_field.value or "5"),
                int(count_field.value or "1"),
            )
            status.value = "Running..."
            page.update()
            threading.Thread(target=run_refresh, daemon=True).start()

        def stop_click(e: ft.ControlEvent) -> None:
            nonlocal refresher
            if refresher is not None:
                refresher.stop()
            status.value = "Stopped."
            page.update()

        page.add(
            url_field,
            ft.Row([delay_field, count_field]),
            ft.Row([
                ft.ElevatedButton("Start", on_click=start_click),
                ft.ElevatedButton("Stop", on_click=stop_click),
            ]),
            status,
        )

    ft.app(target=app)

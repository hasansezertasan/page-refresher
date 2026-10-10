import threading

import customtkinter as ctk

from page_refresher.core.refresher import SeleniumRefresher


class Main(ctk.CTk):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title("Page Refresher")
        self.geometry("600x300")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.resizable(width=False, height=False)

        self.refresher: SeleniumRefresher | None = None
        self.thread: threading.Thread | None = None

        self.interface()

    def interface(self) -> None:
        self.grid_columnconfigure(1, weight=1)
        label_font = ctk.CTkFont(size=14, weight="bold")

        ctk.CTkLabel(self, text="Target URL:", font=label_font).grid(
            row=1, column=0, padx=10, pady=10, sticky="w"
        )
        ctk.CTkLabel(self, text="Refresh Delay:", font=label_font).grid(
            row=2, column=0, padx=10, pady=10, sticky="w"
        )
        ctk.CTkLabel(self, text="Refresh Count:", font=label_font).grid(
            row=3, column=0, padx=10, pady=10, sticky="w"
        )

        self.link_input = ctk.CTkEntry(self, placeholder_text="https://example.com")
        self.link_input.grid(
            row=1, column=1, columnspan=2, padx=10, pady=10, sticky="ew"
        )

        self.delay_input = ctk.CTkEntry(self, placeholder_text="Seconds")
        self.delay_input.grid(
            row=2, column=1, columnspan=2, padx=10, pady=10, sticky="ew"
        )

        self.view_count_input = ctk.CTkEntry(self, placeholder_text="Times")
        self.view_count_input.grid(
            row=3, column=1, columnspan=2, padx=10, pady=10, sticky="ew"
        )

        ctk.CTkButton(self, text="Start", command=self.start).grid(
            row=4, column=0, padx=10, pady=10, sticky="w"
        )
        ctk.CTkButton(self, text="Stop", command=self.stop).grid(
            row=4, column=2, padx=10, pady=10, sticky="e"
        )

        self.status_label = ctk.CTkLabel(self, text="", text_color="gray")
        self.status_label.grid(row=5, column=0, columnspan=3, padx=10, sticky="w")

    def start(self) -> None:
        url = self.link_input.get().strip()
        delay = int(self.delay_input.get())
        refresh_count = int(self.view_count_input.get())

        if self.refresher is not None:
            self.refresher.stop()
        self.refresher = SeleniumRefresher(url, delay, refresh_count)
        self.status_label.configure(text="Running...")

        self.thread = threading.Thread(
            target=self._run_refresh, args=(self.refresher,), daemon=True
        )
        self.thread.start()

    def _run_refresh(self, run: SeleniumRefresher) -> None:
        # Runs on a worker thread, so Chrome startup doesn't freeze the window.
        run.refresh()
        self.after(0, self._on_finished, run)

    def _on_finished(self, run: SeleniumRefresher) -> None:
        if run is self.refresher and not run.stopped:
            self.status_label.configure(text="Done.")

    def stop(self) -> None:
        if self.refresher is not None:
            self.refresher.stop()
        self.status_label.configure(text="Stopped.")

    def on_closing(self) -> None:
        if self.refresher is not None:
            self.refresher.stop()
        self.destroy()


def main() -> None:
    app = Main()
    app.mainloop()

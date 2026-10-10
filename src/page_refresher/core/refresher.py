import time


class SeleniumRefresher:
    def __init__(self, driver, url: str, delay: int, refresh_count: int) -> None:
        self.driver = driver
        """Driver instance"""
        self.url = url
        """URL to refresh"""
        self.delay = delay
        """Delay between refreshes"""
        self.refresh_count = refresh_count
        """Number of refreshes"""
        self._running = False

    def refresh(self) -> None:
        self._running = True
        self.driver.get(self.url)
        for _ in range(int(self.refresh_count)):
            if not self._running:
                break
            time.sleep(int(self.delay))
            if not self._running:
                break
            self.driver.refresh()
        self._running = False

    def stop(self) -> None:
        self._running = False

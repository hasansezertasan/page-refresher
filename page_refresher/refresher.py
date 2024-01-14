import time


class SeleniumRefresher:
    def __init__(
        self,
        driver,
        url: str,
        delay: int,
        refresh_count: int,
    ):
        self.driver = driver
        """Driver instance"""
        self.url = url
        """URL to refresh"""
        self.delay = delay
        """Delay between refreshes"""
        self.refresh_count = refresh_count
        """Number of refreshes"""

    def refresh(self):
        self.driver.get(self.url)
        for i in range(int(self.refresh_count)):
            time.sleep(int(self.delay))
            self.driver.refresh()

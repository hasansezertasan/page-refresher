import threading
lazy from collections.abc import Callable

lazy from selenium import webdriver
lazy from selenium.webdriver.chrome.service import Service
lazy from webdriver_manager.chrome import ChromeDriverManager


def chrome_driver() -> webdriver.Chrome:
    """
    Install a matching ChromeDriver and start Chrome.

    Returns:
        A new Chrome driver.
    """
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()))


class SeleniumRefresher:
    def __init__(
        self,
        url: str,
        delay: int,
        refresh_count: int,
        driver_factory: Callable[[], webdriver.Chrome] = chrome_driver,
    ) -> None:
        self.url = url
        """URL to refresh"""
        self.delay = delay
        """Delay between refreshes"""
        self.refresh_count = refresh_count
        """Number of refreshes"""
        self.driver_factory = driver_factory
        """Creates the driver; called on the thread that runs `refresh()`"""
        self._stopped = threading.Event()

    @property
    def stopped(self) -> bool:
        """Whether `stop()` has been called."""
        return self._stopped.is_set()

    def refresh(self) -> None:
        """Open the URL and refresh it until done or stopped, then quit the driver."""
        if self.stopped:
            return
        driver = self.driver_factory()
        try:
            driver.get(self.url)
            for _ in range(int(self.refresh_count)):
                # Event.wait returns early, and True, once stop() is called.
                if self._stopped.wait(int(self.delay)):
                    break
                driver.refresh()
        finally:
            driver.quit()

    def stop(self) -> None:
        self._stopped.set()

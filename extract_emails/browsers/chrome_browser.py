from os import PathLike
from typing import Iterable
from typing import Optional

from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from extract_emails.browsers.page_source_getter import PageSourceGetter


class ChromeBrowser(PageSourceGetter):
    """Getting page sources with selenium and chromedriver

    Examples:
        >>> from extract_emails.browsers import ChromeBrowser
        >>> browser = ChromeBrowser()
        >>> browser.open()
        >>> # do something
        >>> browser.close()

    """

    default_options = {
        "--disable-gpu",
        "--disable-software-rasterizer",
        "--disable-dev-shm-usage",
        "--window-size=1920x1080",
        "--disable-setuid-sandbox",
        "--no-sandbox",
    }

    def __init__(
        self,
        executable_path: PathLike = "/usr/bin/chromedriver",
        headless_mode: bool = True,
        options: Iterable[str] = None,
    ) -> None:
        """ChromeBrowser initialization

        Args:
            executable_path: path to chromedriver, use `which chromedriver` to get the path.
                Default: /usr/bin/chromedriver
            headless_mode: run browser with headless mode or not. Default: True
            options: arguments for chrome.Options().
                Default: set("--disable-gpu", "--disable-software-rasterizer", "--disable-dev-shm-usage",
                    "--window-size=1920x1080", "--disable-setuid-sandbox", "--no-sandbox", )
        """
        self.executable_path = executable_path
        self.headless_mode = headless_mode
        self.options = options if options is not None else self.default_options
        self.driver: Optional[webdriver.Chrome] = None

    def open(self):
        """Add arguments to chrome.Options() and run the browser"""
        options = Options()
        for option in self.options:
            options.add_argument(option)

        if self.headless_mode:
            options.add_argument("--headless")

        self.driver = webdriver.Chrome(
            options=options, executable_path=self.executable_path
        )

    def close(self):
        """Close the browser"""
        self.driver.close()
        self.driver.quit()

    def get_page_source(self, url: str) -> str:
        """Get page source text from URL

        Args:
            url: URL

        Returns:
            page source as text
        """
        try:
            self.driver.get(url)
            page_source = self.driver.page_source
        except Exception as e:
            logger.error(f"Could not get page source from {url}")
            return ""
        else:
            return page_source

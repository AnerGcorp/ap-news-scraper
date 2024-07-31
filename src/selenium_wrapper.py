from RPA.Browser.Selenium import Selenium
from RPA.Browser.Selenium import (
    ElementNotFound, 
    ElementClickInterceptedException, 
    BrowserNotFoundError, 
    WebDriverException
    )
from urllib3.exceptions import NewConnectionError
import logging
import time

class SeleniumWrapper:
    def __init__(self, headless=True):
        # Initialize Selenium browser
        self.browser = Selenium(
            timeout=15,
            language="en"
        )

        # Configure browser options
        options = {}
        if not headless:
            options["headless"] = False
        try:
            # Open available browser with configured options
            self.browser.open_available_browser(options=options)
        except BrowserNotFoundError as e:
            self.logger.error(f"Browser not found: {e}")
        except WebDriverException as e:
            self.logger.error(f"Webdriver exception: {e}")

        # Setting logger
        self.logger = logging.getLogger(__name__)

    def handle_errors(func):
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except NewConnectionError as e:
                self.logger.error(f"`{func.__name__}` - New connection error, whether the url not exist or server is not responding: {e}")
            except ElementNotFound as e:
                if str(func.__name__) == "check_donation_and_close":
                    self.logger.info(f"`{func.__name__}` - Donation alert is not appear yet!")
                    return
                self.logger.error(f"`{func.__name__}` - Element not found: {e}")
            except ElementClickInterceptedException as e:
                self.logger.error(f"`{func.__name__}` - Element click intercepted: {e}")
            except TimeoutError as e:
                self.logger.error(f"`{func.__name__}` - Timeout error: {e}")
            except Exception as e:
                self.logger.error(f"Error in {func.__name__}: {e}")
        return wrapper

    @handle_errors
    def open_page(self, url):
        self.logger.info(f"Opening page: {url}")
        self.browser.go_to(url)

    @handle_errors
    def accept_cookies(self):
        self.logger.info("Accepting cookies...")
        try:
            self.browser.click_element_if_visible('id:onetrust-accept-btn-handler')
            self.logger.info("Cookies accepted!")
        except Exception as e:
            self.logger.error(f"Error accepting cookies: {e}")

    @handle_errors
    def search(self, query):
        self.logger.info("Looking for search box...")
        time.sleep(3)

        self.browser.click_element_if_visible("xpath://button[@class='SearchOverlay-search-button']")

        self.logger.info(f"Searching for: {query}")
        search_input = self.browser.find_element("name:q")
        self.browser.input_text(search_input, query)

        self.browser.wait_and_click_button("xpath://button[@class='SearchOverlay-search-submit']")


    @handle_errors
    def sort(self, sort_by="Newest"):
        self.logger.info(f"Sorting by: {sort_by}")
        options = {
            "Newest": "3",
            "Oldest": "2",
            "Relevance": "0"
        }

        select_element = self.browser.find_element("xpath://select[@class='Select-input']")
        self.browser.select_from_list_by_value(select_element, options[sort_by])
        time.sleep(4)

    def get_news_articles(self):
        self.logger.info("Getting news articles...")
        try:
            self.browser.wait_until_page_contains_element("class:PageList-items-item")
            container = self.browser.find_element("xpath://div[@class='SearchResultsModule-results']")
            articles = self.browser.find_elements("class:PageList-items-item", parent=container)
            return articles
        except ElementNotFound as e:
            self.logger.info(f"Element with CLASS_NAME='PageList-items' not found on page, which is expected! Broken URL found.")
        except Exception as e:
            self.logger.error(f"Error getting news articles: {e}")
            return None

    @handle_errors
    def next_page(self):
        self.logger.info("Clicking next page...")
        try:
            next_page_button = self.browser.find_element("class:Pagination-nextPage")
            self.browser.click_element(next_page_button)
            time.sleep(4)
            return 1
        except Exception as e:
            self.logger.error(f"Error clicking next page: {e}")
            return None
        
    @handle_errors
    def check_donation_and_close(self):
        self.logger.info("Checking donation alert...")
        donation = self.browser.find_element("css:.fancybox-item.fancybox-close")        
        self.browser.click_element(donation)

    def close(self):
        self.browser.close_browser()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import logging
import time


class SeleniumWrapper:
    def __init__(self, headless=False):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('headless')
        # Add preferences to bypass the "choose default search engine" prompt
        prefs = {
            "profile.default_content_setting_values.geolocation": 2,  # Disable geolocation prompts
            "profile.default_content_setting_values.notifications": 2,  # Disable notification prompts
            "profile.default_content_setting_values.automatic_downloads": 1,  # Allow automatic downloads
            "profile.default_content_setting_values.cookies": 1,  # Allow cookies
            "profile.password_manager_enabled": False,  # Disable password manager
            "credentials_enable_service": False,  # Disable password manager
        }
        options.add_experimental_option("prefs", prefs)
        options.add_argument('disable-blink-features=AutomationControlled')
        options.add_argument("--disable-search-engine-choice-screen")
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.wait = WebDriverWait(self.driver, 15)

        # setting logger
        self.logger = logging.getLogger(__name__)

    def open_page(self, url):
        self.logger.info(f"Opening page: {url}")
        self.driver.get(url)

    def accept_cookies(self): 
        self.logger.info("Accepting cookies...")
        try:
            # Assuming you have a WebDriverWait object called wait with a reasonable timeout
            accept_button = self.wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
            accept_button.click()
            self.logger.info("Cookies accepted!")
            
        except TimeoutException as e:
            self.logger.error(f"Failed to find 'Accept Cookies' button within timeout: {e}")
        except Exception as e:
            self.logger.error(f"Error accepting cookies: {e}")
        

    def search(self, query):
        self.logger.info("Looking for search box...")
        search_icon = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@class='SearchOverlay-search-button']")))
        search_icon.click()

        self.logger.info(f"Searching for: {query}")
        search_input = self.wait.until(EC.presence_of_element_located((By.NAME, 'q')))
        search_input.send_keys(query + Keys.RETURN)

    def sort(self, sort_by="Newest"):
        self.logger.info(f"Sorting by: {sort_by}")
        options = {
            "Newest": "3",
            "Oldest": "2",
            "Relevance": "0"
        }

        # Locate the select element
        select_element = self.wait.until(EC.presence_of_element_located((By.NAME, "s")))

        # Create a Select object
        select = Select(select_element)

        # Select the option by value
        select.select_by_value(options[sort_by])  # To select "Newest"
        time.sleep(4)


    def get_news_articles(self):
        self.logger.info("Getting news articles...")
        try:
            self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'PageList-items-item')))
            container = self.wait.until(EC.presence_of_element_located((By.XPATH, ".//div[@class='SearchResultsModule-results']")))
            articles = container.find_elements(By.CLASS_NAME, 'PageList-items-item')
            return articles
        except TimeoutException:
            self.logger.error(f"Element with CLASS_NAME='PageList-items' not found on page")
            return None
        except Exception as e:
            self.logger.error(f"Error getting news articles: {e}")
            return None
        
    def next_page(self):
        self.logger.info("Clicking next page...")
        try:
            next_page_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "Pagination-nextPage")))
            next_page_button.click()
            time.sleep(4)
            return 1
        except TimeoutException:
            self.logger.error(f"Element with CLASS_NAME='Pagination-nextPage' not found on page: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error clicking next page: {e}")
            return None
        
    def check_donation_and_close(self):
        self.logger.info("Checking donation alert...")
        # At certain time the page shows a donation alert, this method will close it
        try:
            donation = self.driver.find_element(By.CSS_SELECTOR, ".fancybox-item.fancybox-close")         
            donation.click()
            return 1
        except NoSuchElementException as e:
            self.logger.info(f"Donate alert did not appear yet!!!")
        except Exception as e:
            self.logger.error(f"Error clicking donation: {e}")
        return 0

    def close(self):
        self.driver.quit()
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


def check_compatibility():
    try:
        # Create Chrome options object
        options = Options()

        # Define your desired options here (examples)
        options.add_argument("--headless")  # Run Chrome in headless mode (no UI)
        options.add_argument("--disable-gpu")  # Disable GPU acceleration   

        # Create the webdriver instance with options
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        driver.get("https://www.google.com")
        print("Chrome and Selenium seem compatible.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if driver:
            driver.quit()

check_compatibility()
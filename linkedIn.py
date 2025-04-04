from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import time
import parameters
import os



class Linkedin:
    def __init__(self):
        self.username = parameters.linkedin_username
        self.password = parameters.linkedin_password
        self.keywords = parameters.keywords
        self.start_page = parameters.start_page
        self.till_page = parameters.till_page
        self.geo = parameters.geoUrn

        # Configure Remote WebDriver
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        # chrome_options.add_argument("--headless")  # Run headless in Docker
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

        # Connect to remote Selenium
        SELENIUM_URL = os.getenv("SELENIUM_URL", "http://selenium:4444/wd/hub")

        self.driver = webdriver.Remote(
            command_executor=SELENIUM_URL,
            options=chrome_options
        )
        self.wait = WebDriverWait(self.driver, 20)

    def login(self):
        """Logs into LinkedIn using the provided credentials."""
        self.driver.get('https://www.linkedin.com/login')
        self.wait.until(EC.presence_of_element_located((By.ID, 'username'))).send_keys(self.username)
        self.driver.find_element(By.ID, 'password').send_keys(self.password)
        self.driver.find_element(By.XPATH, '//*[@type="submit"]').click()
        time.sleep(5)

    def search_and_send_request(self):
        """Searches for profiles and sends connection requests."""
        for page in range(self.start_page, self.till_page + 1):
            print(f'\nINFO: Checking page {page}')
            query_url = (
                f'https://www.linkedin.com/search/results/people/?geoUrn={self.geo}'
                f'&keywords={self.keywords}&origin=FACETED_SEARCH&profileLanguage="en"&page={page}'
            )
            self.driver.get(query_url)
            time.sleep(5)

            # Scroll to load all dynamic content
            self.scroll_page()

            try:
                # Find all "Connect" buttons
                connect_buttons = self.wait.until(
                    EC.presence_of_all_elements_located((By.XPATH, "//button[.//span[text()='Connect']]"))
                )
                print(f"INFO: Found {len(connect_buttons)} 'Connect' buttons on page {page}")
            except TimeoutException:
                print(f"ERROR: No 'Connect' buttons found on page {page}")
                continue

            for index, button in enumerate(connect_buttons, start=1):
                self.process_connection(button, index)

            time.sleep(3)

        self.close_driver()

    def process_connection(self, button, index):
        """Processes individual connection requests."""
        name = "Unknown"
        try:
            # Extract name from aria-label
            name = button.get_attribute("aria-label").replace("Invite ", "").replace(" to connect", "").strip()
            print(f"INFO: Attempting to connect with {name}")

            # Scroll into view and ensure the button is clickable
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            time.sleep(1)  # Allow time for adjustments

            # Attempt to click
            try:
                button.click()
            except WebDriverException:
                print(f"ERROR: Click intercepted, trying JavaScript click for {name}")
                self.driver.execute_script("arguments[0].click();", button)

            time.sleep(2)  # Wait for any modals

            # Handle modal if present
            self.handle_modal(index, name)
        except Exception as e:
            print(f"ERROR: Failed to connect with {name} - {e}")
            self.save_debug_info()
        finally:
            print(f"INFO: Finished processing index {index}")

    def handle_modal(self, index, name):
        """Handles the confirmation modal for connection requests."""
        try:
            send_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'artdeco-button--primary')]")
            ))
            send_button.click()
            print(f"INFO: Connection request sent to {name}")
        except TimeoutException:
            print(f"INFO: No confirmation modal for {name}")
        finally:
            time.sleep(2)

    def scroll_page(self):
        """Scrolls the page to load dynamic content."""
        scroll_height = self.driver.execute_script("return document.body.scrollHeight")
        for i in range(0, scroll_height, 1000):
            self.driver.execute_script(f"window.scrollTo(0, {i});")
            time.sleep(1)

    def save_debug_info(self):
        """Saves the page source for debugging."""
        pass
        # with open("debug_page_source.html", "w", encoding="utf-8") as file:
        #     file.write(self.driver.page_source)
        # print("DEBUG: Page source saved for analysis.")

    def close_driver(self):
        """Closes the Selenium WebDriver."""
        self.driver.quit()
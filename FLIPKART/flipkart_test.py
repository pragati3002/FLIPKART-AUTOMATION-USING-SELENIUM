import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Function to initialize the browser
def get_browser():
    """Set up the browser instance."""
    options = Options()
    options.add_argument("--start-maximized")  # Start browser maximized
    options.add_argument("--disable-extensions")  # Disable extensions to avoid interference
    # You can add more options as needed
    
    # Initialize Chrome WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# Function to close the browser
def close_browser(driver):
    """Close the browser instance."""
    driver.quit()

class TestFlipkart(unittest.TestCase):

    def setUp(self):
        """Set up the browser instance before each test."""
        self.driver = get_browser()
        self.driver.get("https://www.flipkart.com")
        self.wait = WebDriverWait(self.driver, 5)  # Increased timeout to 60 seconds
        self.close_login_popup()

    def tearDown(self):
        """Close the browser instance after each test."""
        close_browser(self.driver)

    def close_login_popup(self):
        """Close the login popup if it appears."""
        try:
            close_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "_2KpZ6l _2doB4z")]'))
            )
            close_button.click()
        except Exception as e:
            print("No login popup or error:", e)

    def test_login_and_search_add_to_cart(self):
        """Log in to Flipkart, perform a search, and add an item to the cart."""
        driver = self.driver

        # Perform a search
        search_box = self.wait.until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.send_keys("laptop")
        search_box.send_keys(Keys.RETURN)

        # Wait for search results to load
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div/div/a/div[1]/div[1]/div/div'))
        )

        # Select the first item from the search results
        first_item = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div/div/a/div[1]/div[1]/div/div'))
        )
        first_item.click()

        # Switch to the product details page
        driver.switch_to.window(driver.window_handles[1])

        # Wait for the "Add to Cart" button to be clickable
        add_to_cart_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="container"]/div/div[3]/div[1]/div[1]/div[2]/div/ul/li[1]/button'))
        )
        add_to_cart_button.click()

        # Wait for cart confirmation popup or notification
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "added to cart")]'))
        )

    def test_add_to_cart_without_login(self):
        """Test adding an item to the cart without logging in."""
        driver = self.driver

        # Perform a search
        search_box = self.wait.until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.send_keys("smartphone")
        search_box.send_keys(Keys.RETURN)

        # Wait for search results to load
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div/div/a/div[1]/div[1]/div/div'))
        )

        # Select the first item from the search results
        first_item = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div/div/a/div[1]/div[1]/div/div'))
        )
        first_item.click()

        # Wait for the "Add to Cart" button to be clickable
        add_to_cart_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="container"]/div/div[3]/div[1]/div[1]/div[2]/div/ul/li[1]/button'))
        )
        add_to_cart_button.click()

        # Wait for cart confirmation popup or notification
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "added to cart")]'))
        )

if __name__ == "__main__":
    unittest.main()

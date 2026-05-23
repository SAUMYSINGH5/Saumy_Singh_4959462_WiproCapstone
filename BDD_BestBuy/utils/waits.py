from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Waits:

    def __init__(self, driver, timeout=20):
        self.driver  = driver
        self.timeout = timeout
        self.wait    = WebDriverWait(driver, timeout)

    def wait_for_element_to_be_visible(self, by, locator):
        return self.wait.until(
            EC.visibility_of_element_located((by, locator)),
            message=f"Element not visible: {locator}"
        )

    def wait_for_element_to_be_clickable(self, by, locator):
        return self.wait.until(
            EC.element_to_be_clickable((by, locator)),
            message=f"Element not clickable: {locator}"
        )

    def wait_for_element_to_be_present(self, by, locator):
        return self.wait.until(
            EC.presence_of_element_located((by, locator)),
            message=f"Element not present in DOM: {locator}"
        )

    def wait_for_url_contains(self, url_fragment):
        return self.wait.until(
            EC.url_contains(url_fragment),
            message=f"URL does not contain: {url_fragment}"
        )

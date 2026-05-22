from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import time

from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil

logger = LogGen.loggen(__name__)


class BasePage:

    BASE_URL = "https://www.bestbuy.com"
    DEFAULT_TIMEOUT = 30

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.DEFAULT_TIMEOUT)
        self.actions = ActionChains(driver)

    def find_element(self, locator):
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            logger.error(f"Element not found — {locator}")
            ScreenshotUtil.capture_screenshot(self.driver, "element_not_found")
            raise

    def click(self, locator):
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            self.driver.execute_script("arguments[0].click();", element)
        except TimeoutException:
            logger.error(f"Element not clickable — {locator}")
            ScreenshotUtil.capture_screenshot(self.driver, "element_not_clickable")
            raise

    def js_click(self, element):
        self.driver.execute_script("arguments[0].click();", element)

    def scroll_to(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)

    def is_element_visible(self, locator, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def dismiss_popup(self, locator, timeout=5):
        try:
            btn = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
            self.driver.execute_script("arguments[0].click();", btn)
            time.sleep(0.5)
            logger.info("Popup dismissed")
        except TimeoutException:
            pass
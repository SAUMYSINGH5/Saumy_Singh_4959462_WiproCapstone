from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil

logger = LogGen.loggen(__name__)


class ProductPage:

    ADD_TO_CART = (
        By.XPATH,
        "//button[contains(@data-button-state,'ADD_TO_CART')]"
    )

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

    def add_to_cart(self):
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        self.driver.execute_script("window.scrollBy(0, 600);")

        try:
            btn = self.wait.until(EC.element_to_be_clickable(self.ADD_TO_CART))
        except TimeoutException:
            logger.error("Add to Cart button not clickable")
            ScreenshotUtil.capture_screenshot(self.driver, "add_to_cart_not_clickable")
            raise

        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
        self.driver.execute_script("arguments[0].click();", btn)
        logger.info("Product added to cart")
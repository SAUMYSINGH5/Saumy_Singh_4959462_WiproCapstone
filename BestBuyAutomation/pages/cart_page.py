import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

from pages.base_page import BasePage
from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil

logger = LogGen.loggen(__name__)


class CartPage(BasePage):

    FLYOUT_GO_TO_CART       = (By.CSS_SELECTOR, "a.go-to-cart-button")
    FLYOUT_GO_TO_CART_XPATH = (By.XPATH,
        "//a[normalize-space()='Go to Cart'] | "
        "//button[normalize-space()='Go to Cart']")

    CART_ICON = (By.CSS_SELECTOR,
        "header a[href*='/cart'], "
        ".site-header a[href*='/cart'], "
        "#headerCart a, "
        "[data-testid='header-cart-icon-link']")

    CHECKOUT_BUTTON = (By.XPATH,
        "//button[normalize-space()='Checkout'] | "
        "//a[normalize-space()='Checkout']")

    EMPTY_CART_MSG = (By.XPATH,
        "//*[contains(text(),'Your cart is empty')]")

    CART_ITEM = (By.CSS_SELECTOR,
        ".cart-item, "
        "[data-testid='cart-item'], "
        ".fluid-large-view__column")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(
            driver, 40,
            ignored_exceptions=[StaleElementReferenceException]
        )

    def open_cart(self):
        time.sleep(2)

        # Option 1: flyout button
        for locator in [self.FLYOUT_GO_TO_CART, self.FLYOUT_GO_TO_CART_XPATH]:
            try:
                btn = WebDriverWait(self.driver, 6).until(
                    EC.element_to_be_clickable(locator)
                )
                self.driver.execute_script("arguments[0].click();", btn)
                self._wait_for_cart_page_load()
                logger.info("Cart opened via flyout")
                return
            except TimeoutException:
                continue

        # Option 2: header cart icon
        try:
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            icon = WebDriverWait(self.driver, 8).until(
                EC.element_to_be_clickable(self.CART_ICON)
            )
            self.driver.execute_script("arguments[0].click();", icon)
            self._wait_for_cart_page_load()
            logger.info("Cart opened via header icon")
            return
        except TimeoutException:
            pass

        # Option 3: direct navigation
        self.driver.get("https://www.bestbuy.com/cart")
        self._wait_for_cart_page_load()
        logger.info("Cart opened via direct navigation")

    def _wait_for_cart_page_load(self):
        self.wait.until(lambda d: "cart" in d.current_url.lower())
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        time.sleep(2)

    def proceed_checkout(self):
        self.wait.until(EC.element_to_be_clickable(self.CHECKOUT_BUTTON))
        self.click(self.CHECKOUT_BUTTON)
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        time.sleep(2)
        logger.info("Checkout clicked")

    def is_cart_empty(self):
        return self.is_element_visible(self.EMPTY_CART_MSG, timeout=10)

    def is_cart_not_empty(self):
        return not self.is_element_visible(self.EMPTY_CART_MSG, timeout=10)
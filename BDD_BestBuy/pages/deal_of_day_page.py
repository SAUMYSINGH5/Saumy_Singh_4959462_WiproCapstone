import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException
)

from pages.base_page import BasePage
from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil

logger = LogGen.loggen(__name__)


class DealOfDayPage(BasePage):

    ADD_TO_CART_SELECTORS = [
        (By.CSS_SELECTOR, "button[data-button-state='ADD_TO_CART']"),
        (By.CSS_SELECTOR, "button.add-to-cart-button"),
        (By.XPATH, "//button[normalize-space()='Add to Cart']"),
        (By.XPATH, "//button[contains(@class,'add-to-cart-button')]"),
    ]

    SURVEY_CLOSE = (
        By.CSS_SELECTOR,
        "#survey_window .survey-close, "
        "#survey_window [aria-label='Close'], "
        "#survey_window .close"
    )

    GO_TO_CART_LINK   = (By.XPATH, "//a[contains(@href,'/cart')]")
    GO_TO_CART_BUTTON = (By.XPATH, "//button[normalize-space()='Go to Cart']")

    DEAL_PAGE_INDICATOR = (
        By.CSS_SELECTOR,
        ".shop-deals-card, .v-fw-hard, .daily-deals"
    )

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(
            driver,
            30,
            ignored_exceptions=[StaleElementReferenceException]
        )

    # ---------- Helpers ----------

    def _wait_for_page_ready(self):
        self.wait.until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def _find_button(self, selectors, timeout=8):
        for selector in selectors:
            try:
                btn = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located(selector)
                )

                if btn.is_displayed():
                    return btn

            except TimeoutException:
                continue

        return None

    # ---------- Assertions ----------

    def is_deal_page_displayed(self):
        current_url = self.driver.current_url

        if "deal-of-the-day" in current_url or "pcmcat248000050016" in current_url:
            return True

        try:
            WebDriverWait(self.driver, 8).until(
                EC.presence_of_element_located(self.DEAL_PAGE_INDICATOR)
            )

            return True

        except TimeoutException:
            return False

    def is_product_details_displayed(self):
        current_url = self.driver.current_url

        btn = self._find_button(self.ADD_TO_CART_SELECTORS, timeout=6)

        if btn:
            return True

        return "/skuId=" in current_url or "/p/" in current_url

    # ---------- Page Actions ----------

    def wait_and_add_to_cart(self):
        self._wait_for_page_ready()

        self.dismiss_popup(self.SURVEY_CLOSE)

        time.sleep(2)

        self.driver.execute_script("window.scrollBy(0, 700);")

        btn = self._find_button(self.ADD_TO_CART_SELECTORS)

        if btn is None:
            self.driver.execute_script("window.scrollBy(0, 700);")
            time.sleep(1)

            btn = self._find_button(self.ADD_TO_CART_SELECTORS)

        if btn is None:
            logger.error("Add to cart button not found")

            ScreenshotUtil.capture_screenshot(
                self.driver,
                "add_to_cart_not_found"
            )

            raise Exception("Add to Cart button not found")

        self.scroll_to(btn)

        self.driver.execute_script("arguments[0].click();", btn)

        time.sleep(2)

        logger.info("Added to cart")

    def select_first_product(self):
        pass

    def add_to_cart(self):
        self.wait_and_add_to_cart()

    def go_to_cart(self):
        if "/cart" in self.driver.current_url:
            return

        for locator in [self.GO_TO_CART_LINK, self.GO_TO_CART_BUTTON]:
            try:
                element = WebDriverWait(self.driver, 8).until(
                    EC.element_to_be_clickable(locator)
                )

                element.click()

                logger.info("Went to cart")

                return

            except TimeoutException:
                continue

        logger.error("Could not go to cart")

        ScreenshotUtil.capture_screenshot(
            self.driver,
            "go_to_cart_failed"
        )

        raise TimeoutException("Could not navigate to cart")
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    TimeoutException, StaleElementReferenceException, ElementNotInteractableException
)

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

    # Banner shown after a blocked Checkout click
    DELIVERY_UNAVAILABLE_BANNER = (By.XPATH,
        "//*[contains(text(),'no longer available for the delivery method')] | "
        "//*[contains(text(),'choose a different way to get your order')]")

    # ALL Pickup radios on the page (one per cart item)
    ALL_PICKUP_RADIOS = (By.XPATH,
        "//input[@type='radio' and contains(@id,'fulfillment-ispu')]")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(
            driver, 40,
            ignored_exceptions=[StaleElementReferenceException]
        )

    # ──────────────────────────────────────────────────────────────────
    # open_cart
    # ──────────────────────────────────────────────────────────────────

    def open_cart(self):
        time.sleep(2)

        for locator in [self.FLYOUT_GO_TO_CART, self.FLYOUT_GO_TO_CART_XPATH]:
            try:
                btn = WebDriverWait(self.driver, 6).until(
                    EC.element_to_be_clickable(locator))
                self.driver.execute_script("arguments[0].click();", btn)
                self._wait_for_cart_page_load()
                logger.info("Cart opened via flyout")
                return
            except TimeoutException:
                continue

        try:
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            icon = WebDriverWait(self.driver, 8).until(
                EC.element_to_be_clickable(self.CART_ICON))
            self.driver.execute_script("arguments[0].click();", icon)
            self._wait_for_cart_page_load()
            logger.info("Cart opened via header icon")
            return
        except TimeoutException:
            pass

        self.driver.get("https://www.bestbuy.com/cart")
        self._wait_for_cart_page_load()
        logger.info("Cart opened via direct navigation")

    def _wait_for_cart_page_load(self):
        self.wait.until(lambda d: "cart" in d.current_url.lower())
        self.wait.until(
            lambda d: d.execute_script("return document.readyState") == "complete")
        time.sleep(2)

    # ──────────────────────────────────────────────────────────────────
    # _is_delivery_banner_visible
    # ──────────────────────────────────────────────────────────────────

    def _is_delivery_banner_visible(self) -> bool:
        try:
            elements = self.driver.find_elements(*self.DELIVERY_UNAVAILABLE_BANNER)
            return any(el.is_displayed() for el in elements)
        except Exception:
            return False

    # ──────────────────────────────────────────────────────────────────
    # _react_click
    # ──────────────────────────────────────────────────────────────────

    def _react_click(self, element) -> None:
        """
        Real ActionChains click that fires mousedown/mouseup/click
        so React's synthetic event system registers the state change.
        """
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center', inline:'center'});",
            element
        )
        time.sleep(0.5)
        ActionChains(self.driver).move_to_element(element).click(element).perform()

    # ──────────────────────────────────────────────────────────────────
    # _select_all_pickups  ← KEY FIX: clicks EVERY pickup radio
    # ──────────────────────────────────────────────────────────────────

    def _select_all_pickups(self) -> int:
        """
        Finds ALL 'Pickup at Aiea' radio buttons on the page
        (one per cart item) and clicks each unselected one.

        Returns the count of radios successfully clicked.
        Multiple items in cart each have their own fulfillment row,
        so ALL must be switched to Pickup or Checkout stays blocked.
        """
        radios = self.driver.find_elements(*self.ALL_PICKUP_RADIOS)
        logger.info(f"Found {len(radios)} Pickup radio(s) on page.")

        clicked = 0
        for idx, radio in enumerate(radios):
            try:
                # Skip if already selected
                if radio.get_attribute("checked") or \
                   radio.get_attribute("aria-checked") == "true":
                    logger.info(f"Pickup radio [{idx}] already selected — skipping.")
                    continue

                if radio.is_displayed():
                    self._react_click(radio)
                    logger.info(
                        f"Pickup radio [{idx}] clicked "
                        f"(id='{radio.get_attribute('id')}')."
                    )
                    clicked += 1
                    time.sleep(2)   # let this item's row recalculate before next
            except (StaleElementReferenceException,
                    ElementNotInteractableException) as e:
                logger.warning(f"Pickup radio [{idx}] not interactable: {e}")
                continue
            except Exception as e:
                logger.warning(f"Pickup radio [{idx}] error: {e}")
                continue

        logger.info(f"Switched {clicked} item(s) to Pickup.")

        # Wait for banner to disappear confirming all items are resolved
        if clicked > 0:
            try:
                WebDriverWait(self.driver, 8).until_not(
                    lambda d: self._is_delivery_banner_visible()
                )
                logger.info("Delivery banner gone — all items set to Pickup.")
            except TimeoutException:
                logger.warning(
                    "Delivery banner still visible after switching all radios. "
                    "There may be an item that cannot be picked up."
                )

        return clicked

    # ──────────────────────────────────────────────────────────────────
    # proceed_checkout
    # ──────────────────────────────────────────────────────────────────

    def proceed_checkout(self):
        """
        1. Click Checkout (attempt 1).
        2. If delivery banner appears → switch ALL items to Pickup.
        3. Wait for banner to clear.
        4. Click Checkout again (attempt 2).
        """
        # ── Attempt 1 ─────────────────────────────────────────────────
        self.wait.until(EC.element_to_be_clickable(self.CHECKOUT_BUTTON))
        self.click(self.CHECKOUT_BUTTON)
        logger.info("Checkout clicked (attempt 1)")

        time.sleep(4)
        self.wait.until(
            lambda d: d.execute_script("return document.readyState") == "complete")

        # ── Check for delivery block ───────────────────────────────────
        if "cart" in self.driver.current_url.lower() and \
                self._is_delivery_banner_visible():

            logger.warning(
                "Delivery unavailable banner detected. "
                "Switching ALL cart items to Pickup at Aiea."
            )

            count = self._select_all_pickups()

            if count > 0:
                time.sleep(2)
                # ── Attempt 2 ─────────────────────────────────────────
                self.wait.until(EC.element_to_be_clickable(self.CHECKOUT_BUTTON))
                self.click(self.CHECKOUT_BUTTON)
                logger.info(
                    f"Checkout clicked (attempt 2 — after switching "
                    f"{count} item(s) to Pickup)"
                )
                time.sleep(4)
                self.wait.until(
                    lambda d: d.execute_script(
                        "return document.readyState") == "complete")
            else:
                logger.error(
                    "No Pickup radios could be clicked — Checkout will fail.")
        else:
            logger.info("No delivery banner — checkout proceeded normally.")

        logger.info(f"Post-checkout URL: {self.driver.current_url}")

    # ──────────────────────────────────────────────────────────────────
    # Cart state helpers
    # ──────────────────────────────────────────────────────────────────

    def is_cart_empty(self):
        return self.is_element_visible(self.EMPTY_CART_MSG, timeout=10)

    def is_cart_not_empty(self):
        return not self.is_element_visible(self.EMPTY_CART_MSG, timeout=10)

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from pages.base_page import BasePage
from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil

logger = LogGen.loggen(__name__)


class CheckoutPage(BasePage):

    EMAIL_FIELD     = (By.ID, "fld-e")
    CONTINUE_BUTTON = (By.XPATH, "//button[contains(text(),'Continue')]")

    EMAIL_ERROR_LOCATORS = [
        (By.XPATH, "//*[contains("
                   "translate(text(),"
                   "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
                   "'abcdefghijklmnopqrstuvwxyz'),"
                   "'valid email')]"),
        (By.XPATH, "//*[contains(@class,'error') and contains(text(),'email')]"),
        (By.XPATH, "//*[contains(@class,'invalid') and contains(text(),'email')]"),
        (By.CSS_SELECTOR, "#fld-e[aria-invalid='true']"),
        (By.CSS_SELECTOR, ".error-message"),
        (By.CSS_SELECTOR, ".field-error"),
        (By.CSS_SELECTOR, ".inline-error"),
        (By.CSS_SELECTOR, ".validation-error"),
    ]

    CHECKOUT_PAGE_INDICATORS = [
        "identity/signin",
        "checkout",
        "bestbuy.com/checkout",
    ]

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 30)

    # -- Assertion ---------------------------------------------------------

    def is_checkout_page_displayed(self):
        current_url = self.driver.current_url
        for indicator in self.CHECKOUT_PAGE_INDICATORS:
            if indicator in current_url:
                return True
        logger.error("Checkout page not detected")
        return False

    # -- Actions -----------------------------------------------------------

    def enter_email(self, email):
        email_field = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        self.scroll_to(email_field)
        time.sleep(1)
        email_field.clear()
        email_field.send_keys(email)
        time.sleep(1)
        logger.info(f"Email entered: {email}")

    def click_continue(self):
        self.wait.until(EC.element_to_be_clickable(self.CONTINUE_BUTTON))
        self.click(self.CONTINUE_BUTTON)
        time.sleep(2)
        logger.info("Continue clicked")

    def invalid_email_error(self):
        for locator in self.EMAIL_ERROR_LOCATORS:
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(locator)
                )
                logger.info("Email error found")
                return True
            except TimeoutException:
                continue
        logger.error("Email error not found")
        ScreenshotUtil.capture_screenshot(self.driver, "invalid_email_error_not_found")
        return False

    def debug_page_errors(self):
        candidates = self.driver.find_elements(
            By.XPATH,
            "//*[contains(@class,'error') or contains(@class,'invalid') "
            "or contains(@class,'validation')]"
        )
        if not candidates:
            logger.warning("No error elements found on page")
        for el in candidates:
            logger.info(
                f"tag={el.tag_name} | class={el.get_attribute('class')!r} | "
                f"aria-invalid={el.get_attribute('aria-invalid')!r} | text={el.text.strip()!r}"
            )
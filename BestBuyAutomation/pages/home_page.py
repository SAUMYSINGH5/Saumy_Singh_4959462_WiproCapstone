import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from pages.base_page import BasePage
from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil

logger = LogGen.loggen(__name__)


class HomePage(BasePage):

    COUNTRY_US = (
        By.XPATH,
        "//img[@alt='United States']"
    )

    DEAL_OF_DAY = (
        By.XPATH,
        "//span[@data-testid='utility-nav-link-text' "
        "and normalize-space()='Deal of the Day']"
    )

    EMAIL_INPUT = (
        By.ID,
        "footer-email-signup"
    )

    EMAIL_SIGNUP = (
        By.XPATH,
        "//button[normalize-space()='Sign Up']"
    )

    SURVEY_CLOSE = (
        By.CSS_SELECTOR,
        "#survey_window .survey-close, "
        "#survey_window [aria-label='Close'], "
        "#survey_window .close"
    )

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 30)

    # ---------- Helper ----------

    def _capture(self, name):
        ScreenshotUtil.capture_screenshot(self.driver, name)

    # ---------- Actions ----------

    def select_country(self):
        try:
            country = self.wait.until(EC.element_to_be_clickable(self.COUNTRY_US))
            self.driver.execute_script("arguments[0].click();", country)
            time.sleep(3)
            logger.info("Country selected")
        except TimeoutException:
            logger.error("Country selector not found")
            self._capture("country_selector_not_found")
            raise

    def open_deal_of_day(self):
        self.dismiss_popup(self.SURVEY_CLOSE)
        self.driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(1)
        try:
            deal = self.wait.until(EC.element_to_be_clickable(self.DEAL_OF_DAY))
            self.scroll_to(deal)
            self.driver.execute_script("arguments[0].click();", deal)
            time.sleep(3)
            logger.info("Deal of the Day opened")
        except TimeoutException:
            logger.error("Deal of the Day link not found")
            self._capture("deal_of_day_not_found")
            raise

    def enter_email(self, email):
        try:
            email_box = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
            self.scroll_to(email_box)
            email_box.clear()
            email_box.send_keys(email)
            logger.info(f"Email entered: {email}")
        except TimeoutException:
            logger.error("Email input not found")
            self._capture("email_input_not_found")
            raise

    def click_signup_button(self):
        try:
            signup = self.wait.until(EC.element_to_be_clickable(self.EMAIL_SIGNUP))
            self.scroll_to(signup)
            signup.click()
            time.sleep(2)
            logger.info("Sign Up clicked")
        except TimeoutException:
            logger.error("Sign Up button not found")
            self._capture("signup_button_not_found")
            raise
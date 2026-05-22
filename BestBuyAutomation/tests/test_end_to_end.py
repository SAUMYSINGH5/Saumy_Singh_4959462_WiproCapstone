import allure
from pages.home_page import HomePage
from pages.deal_of_day_page import DealOfDayPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.csv_reader import CSVReader
from utils.logger import LogGen

logger = LogGen.loggen(__name__)


@allure.title("End to End - Add Product and Proceed to Checkout")
@allure.description("Selects a Deal of the Day product, adds to cart, proceeds to checkout, and enters email.")
def test_end_to_end(driver):

    home     = HomePage(driver)
    deal     = DealOfDayPage(driver)
    cart     = CartPage(driver)
    checkout = CheckoutPage(driver)

    with allure.step("Step 1: Open home page and select country"):
        home.select_country()

    with allure.step("Step 2: Open Deal of the Day page"):
        home.open_deal_of_day()

    with allure.step("Step 3: Select first product"):
        deal.select_first_product()

    with allure.step("Step 4: Add product to cart"):
        deal.add_to_cart()

    with allure.step("Step 5: Navigate to cart"):
        deal.go_to_cart()
        assert "cart" in driver.current_url.lower(), "Cart page not opened"

    with allure.step("Step 6: Proceed to checkout"):
        cart.proceed_checkout()

    with allure.step("Step 7: Read email from CSV"):
        data  = CSVReader.read_csv("test_data.csv")
        email = data[0]["email"]
        logger.info(f"Email loaded: {email}")

    with allure.step(f"Step 8: Enter email and click continue"):
        checkout.enter_email(email)
        checkout.click_continue()

    with allure.step("Step 9: Validate checkout or sign-in page reached"):
        current_url = driver.current_url.lower()
        assert "checkout" in current_url or "identity" in current_url or "signin" in current_url, \
            f"Expected checkout or sign-in page, got: {driver.current_url}"
        logger.info("E2E test passed")
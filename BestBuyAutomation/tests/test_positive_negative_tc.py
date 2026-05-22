import allure
from pages.home_page import HomePage
from pages.deal_of_day_page import DealOfDayPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.csv_reader import CSVReader
from utils.logger import LogGen

logger = LogGen.loggen(__name__)


@allure.title("Positive - Open Deal of the Day")
@allure.description("Verifies that Deal of the Day page opens successfully.")
def test_01_open_deal_of_day(driver):
    home = HomePage(driver)
    deal = DealOfDayPage(driver)
    with allure.step("Step 1: Select country on home page"):
        home.select_country()
    with allure.step("Step 2: Open Deal of the Day"):
        home.open_deal_of_day()
    with allure.step("Step 3: Verify Deal page is displayed"):
        assert deal.is_deal_page_displayed(), "Deal of the Day page did not open"


@allure.title("Positive - Select Product from Deal List")
@allure.description("Verifies that a product can be selected from Deal of the Day list.")
def test_02_select_product_from_deal_list(driver):
    home = HomePage(driver)
    deal = DealOfDayPage(driver)
    with allure.step("Step 1: Select country on home page"):
        home.select_country()
    with allure.step("Step 2: Open Deal of the Day"):
        home.open_deal_of_day()
    with allure.step("Step 3: Select first product"):
        deal.select_first_product()
    with allure.step("Step 4: Verify product details page is displayed"):
        assert deal.is_product_details_displayed(), "Product details page did not open"


@allure.title("Positive - Add Product Successfully")
@allure.description("Verifies a product can be added to cart from Deal of the Day.")
def test_03_add_product_to_cart(driver):
    home = HomePage(driver)
    deal = DealOfDayPage(driver)
    cart = CartPage(driver)
    with allure.step("Step 1: Select country on home page"):
        home.select_country()
    with allure.step("Step 2: Open Deal of the Day"):
        home.open_deal_of_day()
    with allure.step("Step 3: Select first product"):
        deal.select_first_product()
    with allure.step("Step 4: Add product to cart"):
        deal.add_to_cart()
    with allure.step("Step 5: Open cart"):
        cart.open_cart()
    with allure.step("Step 6: Verify cart is not empty"):
        assert cart.is_cart_not_empty(), "Cart is empty after adding product"


@allure.title("Positive - Proceed to Checkout")
@allure.description("Verifies that checkout page opens after adding product to cart.")
def test_04_proceed_to_checkout(driver):
    home = HomePage(driver)
    deal = DealOfDayPage(driver)
    cart = CartPage(driver)
    checkout = CheckoutPage(driver)
    with allure.step("Step 1: Select country on home page"):
        home.select_country()
    with allure.step("Step 2: Open Deal of the Day"):
        home.open_deal_of_day()
    with allure.step("Step 3: Select first product"):
        deal.select_first_product()
    with allure.step("Step 4: Add product to cart"):
        deal.add_to_cart()
    with allure.step("Step 5: Open cart"):
        cart.open_cart()
    with allure.step("Step 6: Proceed to checkout"):
        cart.proceed_checkout()
    with allure.step("Step 7: Verify checkout page is displayed"):
        assert checkout.is_checkout_page_displayed(), "Checkout page did not open"


@allure.title("Negative - Invalid Email at Checkout")
@allure.description("Verifies that an invalid email shows a validation error at checkout.")
def test_05_invalid_email(driver):
    home     = HomePage(driver)
    deal     = DealOfDayPage(driver)
    cart     = CartPage(driver)
    checkout = CheckoutPage(driver)
    with allure.step("Step 1: Select country on home page"):
        home.select_country()
    with allure.step("Step 2: Open Deal of the Day"):
        home.open_deal_of_day()
    with allure.step("Step 3: Select first product"):
        deal.select_first_product()
    with allure.step("Step 4: Add product to cart"):
        deal.add_to_cart()
    with allure.step("Step 5: Open cart and proceed to checkout"):
        cart.open_cart()
        cart.proceed_checkout()
    with allure.step("Step 6: Read invalid email from CSV"):
        data = CSVReader.read_csv("test_data.csv")
        invalid_email = next(
            item["email"] for item in data if "invalid" in item["type"].lower()
        )
        logger.info(f"Invalid email loaded: {invalid_email}")
    with allure.step("Step 7: Enter invalid email and click continue"):
        checkout.enter_email(invalid_email)
        checkout.click_continue()
    with allure.step("Step 8: Verify invalid email error is shown"):
        assert checkout.invalid_email_error() is True, "Invalid email error not shown"


@allure.title("Negative - Checkout Without Product")
@allure.description("Verifies that an empty cart is correctly detected at checkout.")
def test_06_checkout_without_product(driver):
    home = HomePage(driver)
    cart = CartPage(driver)
    with allure.step("Step 1: Select country on home page"):
        home.select_country()
    with allure.step("Step 2: Open cart directly without adding product"):
        cart.open_cart()
    with allure.step("Step 3: Verify cart is empty"):
        assert cart.is_cart_empty(), "Cart is NOT empty but expected empty"
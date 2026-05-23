import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from behave import given, when, then
import allure

from pages.home_page import HomePage
from pages.deal_of_day_page import DealOfDayPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.logger import LogGen

logger = LogGen.loggen()


# helper: attach a screenshot mid-step if needed
def _attach_screenshot(context, name: str):
    try:
        allure.attach(
            context.driver.get_screenshot_as_png(),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )
    except Exception as e:
        logger.warning(f"Could not attach screenshot '{name}': {e}")


# BACKGROUND

@given('User launches Best Buy application')
@allure.step("Launch Best Buy application")
def step_launch_bestbuy(context):
    context.home_page     = HomePage(context.driver)
    context.deal_page     = DealOfDayPage(context.driver)
    context.cart_page     = CartPage(context.driver)
    context.checkout_page = CheckoutPage(context.driver)
    context.driver.get("https://www.bestbuy.com")
    logger.info("Opened Best Buy")


@given('User selects their country')
@allure.step("Select country")
def step_select_country(context):
    context.home_page.select_country()
    logger.info("Country selected")


@when('User clicks on Deal of the Day menu')
@allure.step("Click Deal of the Day menu")
def step_navigate_deal_of_day(context):
    context.home_page.open_deal_of_day()
    logger.info("Navigated to Deal of the Day")


@then('User should see the Deal of the Day page')
@allure.step("Verify Deal of the Day page is displayed")
def step_verify_deal_page(context):
    assert context.deal_page.is_deal_page_displayed(), \
        "Deal of the Day page not displayed"
    _attach_screenshot(context, "Deal of the Day Page")
    logger.info("Deal of the Day page verified")


# PRODUCT

@when('User selects the first product from the deal list')
@allure.step("Select first product from deal list")
def step_select_first_product(context):
    context.deal_page.select_first_product()
    logger.info("First product selected")


@then('User should see the product details page')
@allure.step("Verify product details page is displayed")
def step_verify_product_details(context):
    assert context.deal_page.is_product_details_displayed(), \
        "Product details page not displayed"
    _attach_screenshot(context, "Product Details Page")
    logger.info("Product details page verified")


# CART

@when('User clicks on Add to Cart button')
@allure.step("Add product to cart")
def step_add_to_cart(context):
    context.deal_page.add_to_cart()
    logger.info("Added to cart")


@when('User clicks on Cart icon')
@allure.step("Open cart")
def step_click_cart(context):
    context.cart_page.open_cart()
    logger.info("Cart opened")


@then('User should see the cart is not empty')
@allure.step("Verify cart is not empty")
def step_verify_cart_not_empty(context):
    assert context.cart_page.is_cart_not_empty(), \
        "Cart is empty after adding product"
    _attach_screenshot(context, "Cart — Not Empty")
    logger.info("Cart has items")


@when('User opens the cart directly without adding a product')
@allure.step("Open cart directly without adding a product")
def step_open_cart_directly(context):
    context.cart_page.open_cart()
    logger.info("Opened cart directly")


@then('User should see the cart is empty')
@allure.step("Verify cart is empty")
def step_verify_cart_empty(context):
    assert context.cart_page.is_cart_empty(), \
        "Cart is NOT empty but expected to be empty"
    _attach_screenshot(context, "Cart — Empty")
    logger.info("Cart is empty")


# CHECKOUT

@when('User clicks on Checkout button')
@allure.step("Click Checkout button")
def step_click_checkout(context):
    context.cart_page.proceed_checkout()
    logger.info("Checkout clicked")


@then('User should see the checkout page')
@allure.step("Verify checkout page is displayed")
def step_verify_checkout(context):
    assert context.checkout_page.is_checkout_page_displayed(), \
        "Checkout page not displayed"
    _attach_screenshot(context, "Checkout Page")
    logger.info("On checkout page")


@when('User clicks on Continue button')
@allure.step("Click Continue button")
def step_click_continue(context):
    context.checkout_page.click_continue()
    logger.info("Continue clicked")


# EMAIL
@when('User enters an invalid email "{email}"')
@allure.step("Enter invalid email: {email}")
def step_enter_invalid_email(context, email):
    context.checkout_page.enter_email(email)
    logger.info(f"Invalid email entered: {email}")


@then('User should see an invalid email error message')
@allure.step("Verify invalid email error message is shown")
def step_verify_email_error(context):
    assert context.checkout_page.invalid_email_error() is True, \
        "Invalid email error not shown"
    _attach_screenshot(context, "Invalid Email Error")
    logger.info("Email error displayed")


@when('User enters email address "{email}"')
@allure.step("Enter email address: {email}")
def step_enter_email(context, email):
    context.checkout_page.enter_email(email)
    logger.info(f"Email entered: {email}")


@then('User should proceed to the next checkout step')
@allure.step("Verify user proceeds to next checkout step")
def step_verify_next_step(context):
    current_url = context.driver.current_url
    assert any(x in current_url for x in
               ["checkout", "payment", "shipping", "signin"]), \
        f"Did not proceed to next checkout step. URL: {current_url}"
    _attach_screenshot(context, "Next Checkout Step")
    logger.info(f"Next step loaded: {current_url}")
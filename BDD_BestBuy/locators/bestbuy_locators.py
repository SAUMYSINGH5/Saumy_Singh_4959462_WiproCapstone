"""
Locators for Best Buy Deal of the Day, Cart, and Checkout pages
"""


class HomePageLocators:
    DEAL_OF_DAY_LINK = "//a[contains(text(),'Deal of the Day') or contains(@href,'deal-of-the-day')]"
    DEAL_OF_DAY_NAV  = "//nav//a[contains(text(),'Deals')]"


class DealOfDayLocators:
    PAGE_HEADING         = "//h1[contains(text(),'Deal of the Day')]"
    FIRST_PRODUCT        = "(//div[contains(@class,'sku-item')])[1]"
    ADD_TO_CART_BUTTON   = "(//button[contains(@class,'add-to-cart') or contains(text(),'Add to Cart')])[1]"
    PRODUCT_TITLE        = "(//h4[contains(@class,'sku-title')]//a)[1]"
    DEAL_TIMER           = "//div[contains(@class,'deal-timer') or contains(@class,'countdown')]"


class CartLocators:
    CART_ICON            = "//a[@class='header-cart-icon' or contains(@aria-label,'Cart')]"
    CART_COUNT_BADGE     = "//span[contains(@class,'cart-count')]"
    CHECKOUT_BUTTON      = "//button[contains(text(),'Checkout') or @data-track='checkout']"
    CART_ITEM_TITLE      = "//div[contains(@class,'item-info')]//a"
    CART_ITEM_PRICE      = "//div[contains(@class,'item-price')]"
    EMPTY_CART_MESSAGE   = "//h1[contains(text(),'Your cart is empty')]"
    CONTINUE_SHOPPING    = "//a[contains(text(),'Continue Shopping')]"


class CheckoutLocators:
    CHECKOUT_PAGE_HEADING = "//h1[contains(text(),'Checkout') or contains(text(),'Sign In')]"
    EMAIL_INPUT           = "//input[@type='email' or @id='fld-e']"
    CONTINUE_BUTTON       = "//button[@type='submit' or contains(text(),'Continue')]"
    GUEST_CHECKOUT_BUTTON = "//button[contains(text(),'Continue as Guest')]"
    ORDER_SUMMARY_HEADING = "//h2[contains(text(),'Order Summary')]"
    SIGN_IN_BUTTON        = "//button[contains(text(),'Sign In')]"

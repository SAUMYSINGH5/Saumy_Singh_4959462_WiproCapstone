Feature: Best Buy Deal of the Day - Functional Tests (Positive & Negative)

  Background:
    Given User launches Best Buy application
    And User selects their country

  # POSITIVE SCENARIOS

  @positive @smoke
  Scenario: TC01 - Open Deal of the Day
    When User clicks on Deal of the Day menu
    Then User should see the Deal of the Day page

  @positive
  Scenario: TC02 - Select Product from Deal List
    When User clicks on Deal of the Day menu
    And User selects the first product from the deal list
    Then User should see the product details page

  @positive
  Scenario: TC03 - Add Product to Cart
    When User clicks on Deal of the Day menu
    And User selects the first product from the deal list
    And User clicks on Add to Cart button
    And User clicks on Cart icon
    Then User should see the cart is not empty

  @positive
  Scenario: TC04 - Proceed to Checkout
    When User clicks on Deal of the Day menu
    And User selects the first product from the deal list
    And User clicks on Add to Cart button
    And User clicks on Cart icon
    And User clicks on Checkout button
    Then User should see the checkout page

  # NEGATIVE SCENARIOS
  @negative
  Scenario: TC05 - Invalid Email at Checkout
    When User clicks on Deal of the Day menu
    And User selects the first product from the deal list
    And User clicks on Add to Cart button
    And User clicks on Cart icon
    And User clicks on Checkout button
    Then User should see the checkout page
    When User enters an invalid email "invalidemail@@@.com"
    And User clicks on Continue button
    Then User should see an invalid email error message

  @negative
  Scenario: TC06 - Checkout Without Product
    When User opens the cart directly without adding a product
    Then User should see the cart is empty

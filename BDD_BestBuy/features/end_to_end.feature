Feature: Best Buy Deal of the Day - End to End Tests

  Background:
    Given User launches Best Buy application
    And User selects their country

  # END-TO-END SCENARIOS

  @e2e
  Scenario: TC07 - End to End - Deal of Day to Checkout with Email
    When User clicks on Deal of the Day menu
    And User selects the first product from the deal list
    And User clicks on Add to Cart button
    And User clicks on Cart icon
    And User clicks on Checkout button
    Then User should see the checkout page
    When User enters email address "testuser@example.com"
    And User clicks on Continue button
    Then User should proceed to the next checkout step

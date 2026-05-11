# Gherkin Scenarios

These scenarios describe the implemented Customer Ordering System only. They align with the FastAPI endpoints, React pages, pytest coverage, and Playwright browser tests currently present in the project.

## Authentication

```gherkin
Feature: User registration
  Covers: FR-01, NFR-02

  Scenario: Register a new customer successfully
    Given no user exists with email "mina@example.com"
    When the user registers with name "Mina", email "mina@example.com", password "password123", and role "customer"
    Then the API should return status 201
    And the response should include id, name, email, and role
    And the response should not include the password

  Scenario: Register a kitchen staff account successfully
    Given no user exists with email "salma.kitchen@example.com"
    When the user registers with name "Salma", email "salma.kitchen@example.com", password "kitchen123", and role "kitchen"
    Then the API should return status 201
    And the response role should be "kitchen"

  Scenario: Reject duplicate email registration
    Given a user already exists with email "mina@example.com"
    When another registration is submitted with email "mina@example.com"
    Then the API should return status 400
    And the response detail should be "Email already registered"

  Scenario Outline: Reject weak registration passwords
    Given no user exists with email "weak-password@example.com"
    When the user registers with password "<password>"
    Then the registration should be rejected
    And no account should be created

    Examples:
      | password |
      | short    |
      | 1234567  |
```

```gherkin
Feature: User login
  Covers: FR-02, FR-03

  Background:
    Given a registered customer exists with email "mina@example.com" and password "password123"

  Scenario: Login succeeds with valid credentials
    When the customer logs in with email "mina@example.com" and password "password123"
    Then the API should return status 200
    And the response should include an access token
    And the token type should be "bearer"
    And the response role should be "customer"

  Scenario: Login rejects an incorrect password
    When the customer logs in with email "mina@example.com" and password "wrong-password"
    Then the API should return status 401
    And the response detail should be "Invalid credentials"
    And no access token should be returned
```

## Menu And Cart

```gherkin
Feature: Menu retrieval and cart building
  Covers: FR-04, FR-05, NFR-01

  Background:
    Given the SQLite database contains the seeded menu items

  Scenario: Retrieve menu items successfully
    When the user requests the menu
    Then the API should return status 200
    And the response should include at least three menu items
    And each item should include id, name, price, and availability

  Scenario Outline: Reject invalid cart quantities at order validation
    Given a customer is logged in
    And the cart contains menu item 1 with quantity <quantity>
    When the customer places the order
    Then the API should return status 400
    And the response detail should mention "quantity"

    Examples:
      | quantity |
      | 0        |
      | -1       |
      | 11       |
```

## Order Placement

```gherkin
Feature: Customer order placement
  Covers: FR-06, FR-07, FR-08, FR-13

  Background:
    Given a customer is registered and logged in
    And the menu contains item 1

  Scenario: Place an order from a non-empty cart
    Given the cart contains menu item 1 with quantity 2
    And the client order key is new
    When the customer places the order
    Then the API should return status 201
    And the order status should be "pending"
    And the response should include the ordered item and total

  Scenario: Reject an empty cart
    Given the cart contains no items
    When the customer places the order
    Then the API should return status 400
    And the response detail should be "Order must contain at least one item"
    And no order should be created

  Scenario: Reject duplicate client order key
    Given an order already exists with client order key "client-order-key-duplicate"
    And the cart contains menu item 1 with quantity 1
    When the customer places another order with client order key "client-order-key-duplicate"
    Then the API should return status 400
    And the response detail should mention "duplicate"
    And no duplicate order should be created
```

```gherkin
Feature: Protected order actions
  Covers: FR-13

  Scenario: Reject order placement with an invalid token
    Given the request uses access token "expired-or-invalid-token"
    And the request contains menu item 1 with quantity 1
    When the user places an order
    Then the API should return status 401
    And the response detail should be "Unauthorized access"
    And no order should be created
```

## Kitchen Dashboard

```gherkin
Feature: Kitchen dashboard
  Covers: FR-09, FR-11, FR-13, NFR-01

  Background:
    Given at least one order exists with status "pending"

  Scenario: Kitchen staff views active orders
    Given a kitchen staff user is logged in
    When the kitchen staff requests the kitchen dashboard
    Then the API should return status 200
    And the response should include active orders
    And each order should include id, customer email, status, total, and items

  Scenario: Reject customer access to kitchen dashboard
    Given a customer is logged in
    When the customer requests the kitchen dashboard
    Then the API should return status 403
    And the response detail should be "Kitchen role required"

  Scenario: Reject kitchen dashboard access with an invalid token
    Given the request uses access token "expired-or-invalid-token"
    When the user requests the kitchen dashboard
    Then the API should return status 401
    And the response detail should be "Unauthorized access"
```

## Order Status Updates

```gherkin
Feature: Kitchen order status update
  Covers: FR-10, FR-11, FR-12, FR-13

  Background:
    Given an order exists with status "pending"

  Scenario: Kitchen staff updates an order status successfully
    Given a kitchen staff user is logged in
    When the kitchen staff updates the order status to "preparing"
    Then the API should return status 200
    And the response should include the order id
    And the order status should be "preparing"

  Scenario: Reject invalid order status
    Given a kitchen staff user is logged in
    When the kitchen staff updates the order status to "archived"
    Then the API should return status 400
    And the response detail should be "Invalid order status"
    And the stored order status should remain "pending"

  Scenario: Reject customer status update
    Given a customer is logged in
    When the customer updates the order status to "preparing"
    Then the API should return status 403
    And the response detail should be "Kitchen role required"
    And the stored order status should remain unchanged

  Scenario: Reject status update with an invalid token
    Given the request uses access token "expired-or-invalid-token"
    When the user updates the order status to "preparing"
    Then the API should return status 401
    And the response detail should be "Unauthorized access"
    And the stored order status should remain unchanged
```

## Browser-Level Scenarios Covered By Playwright

```gherkin
Feature: Frontend smoke workflows

  Scenario: Homepage loads
    Given the Vite frontend is running
    When the browser opens "http://127.0.0.1:5173"
    Then the page should display the login workflow

  Scenario: Register, login, and view seeded menu
    Given the FastAPI backend is running
    And the Vite frontend is running
    When a new user registers through the browser
    And the same user logs in through the browser
    Then the menu page should display "Chicken Sandwich"
    And the menu page should display "Pasta Bowl"
    And the menu page should display "Fresh Juice"
```


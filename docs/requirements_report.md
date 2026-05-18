# Requirements Report

## Source Summary

This report is based on:

- `CSE323_Project_Overview.pdf`
- `CSE323_Project_Guidelines.pdf`

The selected subsystem is a small Customer Ordering System. The grading goal is not maximum features; it is complete engineering evidence across requirements discovery, traceability, design, TDD, testing, and validation.

## Actor Classification

### Primary Actors

| Actor | Rationale | Main Goals |
| --- | --- | --- |
| Customer | Initiates registration, login, menu browsing, cart actions, order placement, and order tracking. | Create account, log in, view menu, add items, submit order, track current order status. |
| Kitchen Staff | Initiates order status changes after receiving customer orders. | View pending orders, update order status accurately. |

### Supporting Actors

| Actor | Rationale | Main Responsibilities |
| --- | --- | --- |
| Authentication Service | Supports identity checks for protected actions. | Validate credentials, issue simple access token, reject invalid access. |
| Menu Data Store | Supplies item names, prices, and availability. | Provide menu list to customers and tests. |
| Order Data Store | Persists cart-derived orders, mock payment fields, and status changes. | Store orders, items, quantities, payment status, statuses, timestamps. |

### Offstage Actors

| Actor | Rationale | Interest |
| --- | --- | --- |
| Course Evaluator | Does not use the app directly as a business actor, but evaluates engineering evidence. | Traceability, TDD evidence, validation reports, runnable demo. |
| Restaurant Owner | Benefits from reduced order handling mistakes but is not part of the implemented workflow. | Clear, minimal ordering flow and kitchen visibility. |
| System Maintainer | Maintains code after submission. | Simple architecture, clear tests, no unnecessary infrastructure. |

## Personas

### Persona 1: Frustrated Customer

Name: Mina

Behavior: Repeatedly clicks "Place Order", enters unusual quantities, and expects clear feedback when the cart is empty or login fails.

Need: The system must reject invalid orders without corrupting data or creating duplicates.

### Persona 2: Busy Kitchen Staff

Name: Salma

Behavior: Opens the kitchen dashboard during a rush, updates order statuses quickly, and may act on stale information.

Need: The system must show only authorized kitchen actions and keep order status transitions predictable.

### Persona 3: Malicious Student Tester

Name: Kareem

Behavior: Calls protected APIs without a token, tries invalid quantities, and attempts unsupported status updates.

Need: The system must enforce boundaries at API level, not only in the UI.

## Core Requirements

| ID | Requirement | Source/Rationale | Priority | Acceptance Metric |
| --- | --- | --- | --- | --- |
| FR-01 | A customer can register with name, email, and password. | Required feature: Register/Login. | Must | Valid registration returns HTTP 201 and creates one user. |
| FR-02 | A customer can log in with valid credentials. | Required feature: Register/Login. | Must | Valid login returns HTTP 200 and an access token. |
| FR-03 | Invalid login attempts are rejected. | Persona edge case. | Must | Invalid login returns HTTP 401 with no token. |
| FR-04 | A customer can view menu items. | Required feature: View Menu. | Must | Menu endpoint returns at least 3 seeded items in under 2 seconds. |
| FR-05 | A customer can add menu items to a cart in the UI. | Required feature: Add To Cart. | Must | Quantity must be an integer from 1 to 10 per item. |
| FR-06 | A customer can place an order from a non-empty cart. | Required feature: Place Order. | Must | Valid order returns HTTP 201 and status `pending`. |
| FR-07 | Empty cart orders are rejected. | Persona edge case. | Must | Empty order returns HTTP 400 and creates no order. |
| FR-08 | Duplicate rapid order submissions are controlled. | Persona edge case. | Should | Same client order key cannot create more than one order. |
| FR-09 | Kitchen staff can view submitted orders. | Required feature: Kitchen Dashboard. | Must | Dashboard returns pending/preparing/ready orders in under 2 seconds. |
| FR-10 | Kitchen staff can update order status. | Required feature: Update Order Status. | Must | Valid status update is reflected by API within 1 second. |
| FR-11 | Unauthorized users cannot access kitchen actions. | Persona edge case. | Must | Missing or customer token returns HTTP 401 or 403. |
| FR-12 | Invalid order status transitions are rejected. | Edge case and race prevention. | Should | Unsupported status returns HTTP 400 and original status remains unchanged. |
| FR-13 | Expired or invalid access tokens are rejected before protected actions are executed. | Authentication edge case. | Must | Protected routes return HTTP 401 and perform no data read/write action. |
| FR-14 | Kitchen staff registration and access require an email ending with `@ejust.edu.eg`. | Domain restriction for staff workflow. | Must | Non-EJUST kitchen registration returns HTTP 400 and kitchen access requires the EJUST staff domain. |
| FR-15 | A lightweight mock payment status is captured with each order. | Demo-friendly payment simulation. | Should | Order responses and kitchen dashboard show payment method and `paid`/`unpaid` status without real payment processing. |
| FR-16 | A customer can view the latest status, payment status, and summary for their own orders. | Customer order tracking enhancement. | Should | Customer order tracking returns only the logged-in customer's orders and reflects kitchen status updates after refresh. |
| NFR-01 | API response time for normal demo data is under 2 seconds. | QA refinement metric. | Must | Verified by integration/E2E tests or documented manual timing. |
| NFR-02 | Password length must be at least 8 characters. | Measurable security boundary. | Must | Registration with fewer than 8 chars returns HTTP 422 or 400. |
| NFR-03 | The implementation remains small and maintainable. | Project instruction and rubric fit. | Must | No Docker, Redis, PostgreSQL, Redux, real payment integration, analytics, or cloud code. |

## Hidden Requirements and Edge Cases

| Edge Case ID | Case | Requirement Impact | Expected Handling |
| --- | --- | --- | --- |
| EC-01 | Duplicate order caused by double-clicking submit. | FR-08 | Use a client order key or server-side duplicate guard in service tests. |
| EC-02 | Invalid quantity such as 0, -1, 11, or text. | FR-05 | Reject outside integer range 1 to 10. |
| EC-03 | Empty cart submission. | FR-07 | Return validation error and create no order. |
| EC-04 | Unauthorized kitchen access. | FR-11 | Reject missing/customer token before reading or updating kitchen data. |
| EC-05 | Network interruption during order placement. | FR-08, validation | UI keeps cart state until order success is confirmed. |
| EC-06 | Invalid login credentials. | FR-03 | Return a generic failed-login response without issuing a token. |
| EC-07 | Order update race condition or stale status. | FR-12 | Reject unsupported transitions and verify unchanged persisted status. |
| EC-08 | Expired or invalid access token on protected action. | FR-13 | Return 401 before protected order or kitchen logic executes. |
| EC-09 | Non-EJUST email attempts kitchen staff registration. | FR-14 | Return 400 with a staff-domain validation message. |
| EC-10 | Customer marks mock payment as unpaid. | FR-15 | Store and display `unpaid` status for kitchen visibility. |
| EC-11 | Kitchen updates an order after customer placed it. | FR-16 | Customer tracking refresh shows the updated status. |

## Requirement Quality Rules

- Every feature must map to at least one requirement ID.
- Every test must cite one or more requirement IDs.
- Every API endpoint must cite one or more requirement IDs.
- No implementation feature should exist unless it supports the required small subsystem.

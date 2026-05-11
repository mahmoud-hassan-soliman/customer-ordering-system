# Verification vs Validation

## Verification

Verification asks: did we build the software correctly according to its specification?

For this project, verification evidence comes from executable tests and contract checks:

- Pytest unit tests verify service-level rules for registration, login, token rejection, quantity limits, empty cart rejection, duplicate order keys, kitchen dashboard listing, and invalid status rejection.
- Pytest integration tests verify the FastAPI contracts for `/auth/register`, `/auth/login`, `/menu`, `/orders`, `/orders/kitchen`, and `/orders/{order_id}/status`.
- Playwright tests verify that the React frontend loads in a browser and that a user can register, log in, and see seeded menu items.
- Frontend build verification confirms that the React/Vite project compiles successfully.

Examples of verified behavior:

- Valid registration returns HTTP 201.
- Duplicate registration returns HTTP 400 with `Email already registered`.
- Valid login returns a bearer token.
- Empty cart order placement returns HTTP 400.
- Invalid token access returns HTTP 401.
- Customer access to kitchen routes returns HTTP 403.
- Kitchen status update returns HTTP 200 for a valid status.
- Invalid status `archived` returns HTTP 400 and keeps the original status.

## Validation

Validation asks: did we build the right system for the intended customer ordering problem?

The validated problem is a small, demo-friendly Customer Ordering System, not a large restaurant platform. The implemented system supports the intended end-to-end workflow:

- A customer can register and log in.
- A customer can view the seeded menu.
- A customer can add menu items to a cart and place an order.
- The order is created with status `pending`.
- Kitchen staff can log in and view active orders.
- Kitchen staff can update order status to a supported value.

This solves the selected subsystem because it closes the core customer-to-kitchen loop without adding unrelated features such as payments, notifications, analytics, cloud deployment, Redis, Docker, or advanced administration.

## Evidence Mapping

| Evidence | Verification Value | Validation Value |
| --- | --- | --- |
| Pytest unit tests | Prove individual business rules and edge-case boundaries. | Show that the minimal domain rules match the customer ordering workflow. |
| Pytest integration tests | Prove API status codes and response bodies match the contracts. | Show that frontend and backend can rely on stable interfaces. |
| Playwright tests | Prove browser workflows render and interact with the backend. | Show that a user can perform the main demo path through the UI. |
| Real ordering workflow | Confirms order creation and status update operate together. | Demonstrates the system solves the intended ordering-to-kitchen handoff. |
| Kitchen workflow | Confirms role-protected dashboard and status update behavior. | Demonstrates kitchen staff can act on submitted orders. |

## Final Distinction

Verified means the implemented code behaves correctly against the documented requirements and tests.

Validated means the implemented behavior is the right behavior for a small academic Customer Ordering System focused on ordering and kitchen status management.


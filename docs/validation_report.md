# Validation Report

## Validation Question

Does the Customer Ordering System solve the right problem for a small demo-friendly ordering workflow?

Yes. The implemented system supports the required customer-to-kitchen workflow without adding unrelated restaurant-platform features.

## Validated Workflow

The implemented vertical slice validates that:

- A customer can register and log in.
- A customer can view the seeded menu.
- A customer can add menu items to a cart.
- A customer can place a non-empty order.
- Kitchen staff can log in.
- Kitchen staff can view submitted active orders.
- Kitchen staff can update order status.
- Kitchen staff accounts are restricted to `@ejust.edu.eg` emails.
- Mock payment method and paid/unpaid status are visible to staff.
- Customer order tracking shows current status, payment status, and order summary after refresh.

## Validation Evidence

| Evidence | Result | Related Requirements |
| --- | --- | --- |
| Backend pytest suite | 43 tests pass. | FR-01 through FR-16, NFR-02 |
| Frontend production build | `npm run build` succeeds. | NFR-03 |
| Playwright browser tests | 2 tests pass. | FR-01, FR-02, FR-04 |
| API contract tests | Auth, menu, order, and kitchen endpoints return expected status codes and payloads. | FR-01 through FR-13 |
| Edge-case tests | Duplicate email, invalid login, invalid quantity, empty cart, duplicate order key, invalid token, unauthorized kitchen access, invalid staff email domain, invalid status, mock payment visibility, and customer status refresh are covered. | FR-03, FR-05, FR-07, FR-08, FR-11, FR-12, FR-13, FR-14, FR-15, FR-16 |

## Testing Pyramid Summary

| Layer | Count | Evidence |
| --- | ---: | --- |
| Unit | 20 | Service-level business rule and boundary tests. |
| Integration | 23 | FastAPI `TestClient` API contract tests. |
| E2E | 2 | Playwright browser smoke workflows. |

Detailed testing evidence is documented in `docs/testing_pyramid_report.md`.

## Verification vs Validation Statement

Verification proves the software works according to the documented requirements and API contracts. Validation proves that the implemented behavior solves the intended small Customer Ordering System problem.

This project is validated because the real workflow closes the order loop from customer login and order placement to kitchen viewing and status update. The implementation avoids real payment gateways, notifications, analytics, cloud deployment, and advanced administration because those are outside the selected subsystem.

## Residual Manual Evidence

The `screenshots/` folder is available for final demo screenshots. Screenshots are optional supporting evidence; the primary validation evidence is the passing automated test suite and runnable demo workflow.

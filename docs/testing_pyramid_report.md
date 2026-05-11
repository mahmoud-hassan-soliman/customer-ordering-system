# Testing Pyramid Report

## Purpose

The project uses a small testing pyramid to provide rubric evidence without overbuilding the system. The intended structure is:

- 70 percent unit tests for business rules and edge-case boundaries.
- 20 percent integration tests for API contracts and persistence behavior.
- 10 percent E2E tests for browser-level validation of the main demo flow.

## Actual Current Distribution

Current automated tests:

| Layer | Location | Count | Evidence |
| --- | --- | ---: | --- |
| Unit | `tests/unit/` | 16 | Service-level tests for auth, menu retrieval, quantity validation, order creation, duplicate order keys, status updates, and token rejection. |
| Integration | `tests/integration/` | 17 | FastAPI `TestClient` tests for `/auth/register`, `/auth/login`, `/menu`, `/orders`, `/orders/kitchen`, and `/orders/{id}/status`. |
| E2E | `frontend/tests/e2e/` | 2 | Playwright browser tests for homepage loading and register-login-menu workflow. |

Total automated scenarios: 35.

Actual ratio by collected tests:

- Unit: 16 of 35, about 46 percent.
- Integration: 17 of 35, about 49 percent.
- E2E: 2 of 35, about 6 percent.

The suite is intentionally integration-heavy because the rubric emphasizes API contracts, traceability, and verification of observable system behavior. The E2E layer remains small, which preserves the pyramid principle that browser tests should validate critical workflows rather than duplicate every backend edge case.

## Unit Test Evidence

Unit tests focus on business rules and edge-case padlocks:

- `tests/unit/test_auth_service.py`
  - FR-01 registration success and duplicate email rejection.
  - FR-02 login success.
  - FR-03 invalid login rejection.
  - FR-13 invalid token rejection.
  - NFR-02 password length boundary.
- `tests/unit/test_menu_service.py`
  - FR-04 seeded menu retrieval.
- `tests/unit/test_order_service.py`
  - FR-05 quantity boundaries: 0, -1, and 11.
  - FR-06 valid order placement.
  - FR-07 empty cart rejection.
  - FR-08 duplicate `client_order_key` rejection.
  - FR-09 kitchen dashboard order listing.
  - FR-10 status update success.
  - FR-12 invalid status rejection.

## Integration Test Evidence

Integration tests verify the documented API contracts:

- `tests/integration/test_auth_api.py`
  - Registration returns 201.
  - Duplicate registration returns 400 with `Email already registered`.
  - Login returns bearer token.
  - Invalid login returns 401.
- `tests/integration/test_menu_orders_api.py`
  - Menu returns at least three items.
  - Invalid quantities return 400.
  - Valid order returns 201 and status `pending`.
  - Empty cart returns 400.
  - Duplicate order key returns 400.
  - Invalid token returns 401.
- `tests/integration/test_kitchen_api.py`
  - Kitchen dashboard returns submitted orders.
  - Kitchen status update returns 200.
  - Customer access returns 403.
  - Invalid status `archived` returns 400 and preserves the old status.
  - Invalid kitchen token returns 401.

## Playwright E2E Evidence

Playwright tests are stored in `frontend/tests/e2e/`:

- `login.spec.js`: verifies a user can register, log in, and see the seeded menu items in the browser.
- `menu.spec.js`: verifies the homepage loads and displays the login workflow.

These tests connect the React UI to the running FastAPI backend and validate that the main browser workflow is demo-ready.

## Screenshots Evidence

The `screenshots/` folder is reserved for manual or Playwright-generated demo screenshots. Suggested screenshot placeholders:

- `screenshots/login-page.png`
- `screenshots/menu-page.png`
- `screenshots/cart-page.png`
- `screenshots/kitchen-dashboard.png`
- `screenshots/playwright-run.png`

Screenshots are supporting validation evidence; they do not replace automated tests.

## Commands

Backend tests:

```bash
cd "/Volumes/My Macbook/Study/Semester 8/Software Engineering/Projects/FinalProject"
/Users/mahmoudhasssan/anaconda3/bin/pytest
```

Frontend build:

```bash
cd "/Volumes/My Macbook/Study/Semester 8/Software Engineering/Projects/FinalProject/frontend"
npm run build
```

Playwright E2E tests:

```bash
cd "/Volumes/My Macbook/Study/Semester 8/Software Engineering/Projects/FinalProject/frontend"
npx playwright test tests/e2e
```


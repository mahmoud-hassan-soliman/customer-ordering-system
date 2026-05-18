# Test-Driven Prompting Iteration Evidence

## Purpose

This document records the TDP workflow used in Phase 3. The project was intentionally implemented from tests and contracts rather than feature expansion.

## Failing-First Workflow

Step 1 created pytest tests before backend implementation existed. The initial tests intentionally failed because these targets were missing:

- `app.main`
- `app.services.auth_service`
- `app.services.menu_service`
- `app.services.order_service`

This produced failing-first evidence for:

- Registration and login.
- Menu retrieval.
- Quantity boundaries.
- Empty cart rejection.
- Duplicate order prevention.
- Kitchen dashboard access.
- Status update validation.
- Invalid token rejection.

## Implementation Driven By Tests

Step 2 implemented only the backend needed to satisfy those tests:

- FastAPI application setup.
- SQLite and SQLAlchemy setup.
- Minimal models for users, menu items, orders, and order items.
- Pydantic request/response schemas.
- Simple bearer-token authentication.
- Service-layer business rules.
- API routers matching the documented contracts.

No unrelated features were added.

## Edge-Case Padlocks

The test suite locks down these boundary and failure cases:

| Edge Case | Evidence |
| --- | --- |
| Quantity `0` | Unit and integration tests reject it. |
| Quantity `-1` | Unit and integration tests reject it. |
| Quantity `11` | Unit and integration tests reject it. |
| Empty order items | Unit and integration tests return a validation error. |
| Duplicate `client_order_key` | Unit and integration tests reject duplicate order submission. |
| Invalid token | Unit and integration tests return unauthorized access. |
| Customer accessing kitchen endpoints | Integration tests return 403. |
| Invalid status `archived` | Unit and integration tests return 400 and preserve the old status. |
| Customer tracking after kitchen update | Unit and integration tests verify the customer sees the latest status. |

## Iterative Debugging Evidence

During implementation, the first full test run showed that service-level tests passed while integration tests initially needed the HTTP client dependency used by FastAPI `TestClient`. After installing the declared dependency, remaining failures showed stale database state between tests. A small clean database fixture was added to `tests/conftest.py`, preserving duplicate checks inside a single test while making the suite repeatable.

## Duplicate Registration Regression

Manual QA discovered that duplicate email registration incorrectly succeeded. The root cause was in `auth_service.register_user`, which returned the existing user instead of rejecting the duplicate.

Regression tests were added first:

- Unit test: duplicate registration raises `ValueError("Email already registered")`.
- Integration test: duplicate `POST /auth/register` returns HTTP 400 with `{"detail": "Email already registered"}`.

The service was then changed minimally so duplicate email registration fails correctly. The frontend already displayed backend validation messages through the existing API error handling.

## Customer Tracking Enhancement

A final enhancement added failing tests first for customer order tracking. The tests initially failed because `list_customer_orders` and `GET /orders/my` did not exist. The backend then added only the read path needed for customers to refresh and see their own latest order status, payment status, and order summary.

## Current Regression Status

The backend pytest suite currently includes 43 tests across unit and integration layers. Playwright adds browser-level smoke coverage for homepage loading and register-login-menu display.

The TDP evidence demonstrates:

- Failing tests before implementation.
- Minimal implementation to satisfy requirements.
- Iterative debugging based on test output.
- Regression test added before fixing a discovered bug.
- Edge cases preserved as executable tests.

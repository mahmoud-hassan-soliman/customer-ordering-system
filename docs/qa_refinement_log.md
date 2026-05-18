# QA Refinement Log

This log converts vague requirements into measurable criteria, as required by the rubric.

| Original Wording | QA Issue | Refined Metric | Requirement IDs |
| --- | --- | --- | --- |
| The app should be fast. | "Fast" is not testable. | Normal API responses for demo data must complete in under 2 seconds. | NFR-01 |
| Login should be secure. | "Secure" is too broad for this project. | Password must be at least 8 characters; invalid login returns 401 and no token. | FR-03, NFR-02 |
| Orders should update quickly. | "Quickly" is not measurable. | A successful status update must be reflected by the API within 1 second. | FR-10 |
| The cart should prevent bad input. | "Bad input" is unclear. | Quantity must be an integer from 1 to 10 inclusive. | FR-05 |
| The system should avoid duplicate orders. | Duplicate conditions are undefined. | Reusing the same client order key must not create more than one order. | FR-08 |
| Kitchen access should be protected. | "Protected" is vague. | Missing/customer token for kitchen routes must return 401 or 403 before modifying data. | FR-11 |
| Tokens should be valid. | "Valid" needs an observable result. | Expired or malformed access tokens must return 401 before protected route logic reads or writes order data. | FR-13 |
| Staff users should be restricted. | "Staff" needs a measurable domain rule. | Kitchen staff registration and access require email ending with `@ejust.edu.eg`. | FR-14 |
| Payment should be demo-only. | "Payment" could imply real integration. | Mock payment stores only method and `paid`/`unpaid` status; no real gateway or transaction is used. | FR-15 |
| Customers should see order progress. | "Progress" needs an observable refresh behavior. | Customer order tracking must show the latest status returned by `GET /orders/my` after kitchen updates. | FR-16 |
| The app should be maintainable. | Maintainability must be bounded. | No Docker, Redis, PostgreSQL, Redux, real payment integration, analytics, or cloud deployment code. | NFR-03 |

## Senior QA Audit Decisions

- Keep the scope to one vertical slice: customer order submission through kitchen status update.
- Prefer explicit validation errors over silent UI-only prevention.
- Ensure edge cases are tested at service/API level so the frontend cannot bypass constraints.
- Preserve traceability IDs in test names, service docstrings, and reports.
- Add screenshots only as validation evidence, not as a substitute for executable tests.

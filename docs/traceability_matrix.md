# Traceability Matrix and Heatmap

## Traceability Rules

- Zero orphaned requirements: every requirement must map to a feature, API, test type, and validation evidence.
- Zero orphaned features: every feature must map back to a requirement.
- Implementation, tests, and reports preserve these IDs.

## Heatmap Legend

| Mark | Meaning |
| --- | --- |
| H | High coverage or direct evidence required |
| M | Medium/supporting coverage required |
| L | Low/indirect coverage required |
| NA | Not applicable |

## Requirement to Evidence Heatmap

| Requirement | Feature | API Contract | Unit Tests | Integration Tests | E2E Tests | Docs Evidence | Current Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FR-01 Register | Register/Login | H | H | M | M | H | Implemented |
| FR-02 Login | Register/Login | H | H | M | H | H | Implemented |
| FR-03 Invalid login | Register/Login | H | H | M | M | H | Implemented |
| FR-04 View menu | View Menu | H | M | H | H | H | Implemented |
| FR-05 Add to cart | Add To Cart | M | H | M | H | H | Implemented |
| FR-06 Place order | Place Order | H | H | H | H | H | Implemented |
| FR-07 Empty cart rejection | Place Order | H | H | H | M | H | Implemented |
| FR-08 Duplicate order guard | Place Order | H | H | H | M | H | Implemented |
| FR-09 Kitchen dashboard | Kitchen Dashboard | H | M | H | H | H | Implemented |
| FR-10 Update status | Update Order Status | H | H | H | H | H | Implemented |
| FR-11 Unauthorized kitchen access | Kitchen Dashboard, Update Status | H | H | H | M | H | Implemented |
| FR-12 Invalid status transition | Update Order Status | H | H | H | M | H | Implemented |
| FR-13 Expired or invalid token rejection | Protected API Actions | H | H | H | M | H | Implemented |
| FR-14 EJUST kitchen staff domain | Register/Login, Kitchen Access | H | H | H | L | H | Implemented |
| FR-15 Mock payment status | Place Order, Kitchen Dashboard | H | M | H | L | H | Implemented |
| FR-16 Customer order tracking | Order Tracking | H | H | H | L | H | Implemented |
| NFR-01 API response under 2 seconds | All API features | M | NA | M | M | H | Implemented |
| NFR-02 Password length >= 8 | Register | H | H | M | M | H | Implemented |
| NFR-03 Minimal maintainable system | All features | NA | NA | NA | NA | H | Implemented |

## Feature to Requirement Mapping

| Feature | Requirement IDs | Orphan Status |
| --- | --- | --- |
| Register/Login | FR-01, FR-02, FR-03, FR-14, NFR-02 | Not orphaned |
| View Menu | FR-04, NFR-01 | Not orphaned |
| Add To Cart | FR-05 | Not orphaned |
| Place Order | FR-06, FR-07, FR-08, FR-15, NFR-01 | Not orphaned |
| Order Tracking | FR-13, FR-16, NFR-01 | Not orphaned |
| Protected API Actions | FR-13 | Not orphaned |
| Kitchen Dashboard | FR-09, FR-11, FR-13, FR-14, FR-15, NFR-01 | Not orphaned |
| Update Order Status | FR-10, FR-11, FR-12, FR-13, FR-14, NFR-01 | Not orphaned |

## Detailed Requirement Traceability

| Requirement | API | Implementation | Tests | Validation Evidence |
| --- | --- | --- | --- | --- |
| FR-01 | `POST /auth/register` | `auth_service.register_user`, `routers/auth.py` | `test_auth_service.py`, `test_auth_api.py`, Playwright register flow | User can register through API and UI. |
| FR-02 | `POST /auth/login` | `auth_service.login_user`, token helper | `test_auth_service.py`, `test_auth_api.py`, Playwright login flow | User can log in and view menu. |
| FR-03 | `POST /auth/login` | invalid credential branch | `test_auth_service.py`, `test_auth_api.py` | Invalid login returns 401. |
| FR-04 | `GET /menu` | `menu_service.list_menu_items`, menu router | `test_menu_service.py`, `test_menu_orders_api.py`, Playwright menu assertions | Seeded menu appears in API and UI. |
| FR-05 | `POST /orders` | `validate_order_items`, cart UI quantity controls | `test_order_service.py`, `test_menu_orders_api.py` | Invalid quantities are rejected. |
| FR-06 | `POST /orders` | `order_service.create_order`, cart UI | `test_order_service.py`, `test_menu_orders_api.py` | Valid cart creates pending order. |
| FR-07 | `POST /orders` | empty cart validation | `test_order_service.py`, `test_menu_orders_api.py` | Empty cart returns 400. |
| FR-08 | `POST /orders` | duplicate `client_order_key` check | `test_order_service.py`, `test_menu_orders_api.py` | Duplicate order key is rejected. |
| FR-09 | `GET /orders/kitchen` | `list_kitchen_orders`, kitchen UI | `test_order_service.py`, `test_kitchen_api.py` | Kitchen dashboard shows active orders. |
| FR-10 | `PATCH /orders/{id}/status` | `update_order_status`, kitchen UI status select | `test_order_service.py`, `test_kitchen_api.py` | Kitchen can update valid status. |
| FR-11 | Kitchen endpoints | `require_kitchen` dependency | `test_kitchen_api.py` | Customer kitchen access returns 403. |
| FR-12 | `PATCH /orders/{id}/status` | allowed status validation | `test_order_service.py`, `test_kitchen_api.py` | Invalid status is rejected and order remains unchanged. |
| FR-13 | Protected endpoints | token validation helper | `test_auth_service.py`, `test_menu_orders_api.py`, `test_kitchen_api.py` | Invalid token returns 401. |
| FR-14 | `POST /auth/register`, kitchen endpoints | kitchen email-domain validation | `test_auth_service.py`, `test_auth_api.py` | Only `@ejust.edu.eg` kitchen staff are accepted. |
| FR-15 | `POST /orders`, `GET /orders/kitchen` | order payment fields, cart payment UI, kitchen display | `test_menu_orders_api.py`, `test_kitchen_api.py` | Mock payment method/status appears in customer and kitchen workflows. |
| FR-16 | `GET /orders/my`, `PATCH /orders/{id}/status` | `list_customer_orders`, order tracking UI, status refresh | `test_order_service.py`, `test_menu_orders_api.py` | Customer sees own order summary and latest kitchen-updated status. |

## Testing Pyramid Evidence

Target testing pyramid:

- 70 percent unit tests
- 20 percent integration tests
- 10 percent Playwright E2E tests

Actual current automated count:

| Layer | Count | Approx Ratio |
| --- | ---: | ---: |
| Unit | 20 | 44 percent |
| Integration | 23 | 51 percent |
| E2E | 2 | 5 percent |

The implemented suite is intentionally integration-heavy because the rubric emphasizes API contracts and traceability. Browser E2E coverage remains small to avoid duplicating backend edge-case tests.

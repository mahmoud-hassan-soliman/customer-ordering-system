# API Contracts

These contracts define shared interfaces for backend, frontend, and tests. Internal implementation details such as SQLAlchemy models, password hashing helpers, and database sessions are intentionally hidden.

Base URL during local development: `http://127.0.0.1:8000`

JSON request headers:

```http
Content-Type: application/json
```

Standard structured error shape:

```json
{
  "detail": "Human-readable error message"
}
```

## Authentication

### POST `/auth/register`

Covers: FR-01, FR-14, NFR-02

Headers:

```http
Content-Type: application/json
```

Request:

```json
{
  "name": "Mina",
  "email": "mina@example.com",
  "password": "password123",
  "role": "customer"
}
```

Validation:

- `name`: non-empty string
- `email`: valid email-like string
- `password`: minimum 8 characters
- `role`: `customer` or `kitchen`
- kitchen role requires an email ending with `@ejust.edu.eg`

Success response `201`:

```json
{
  "id": 1,
  "name": "Mina",
  "email": "mina@example.com",
  "role": "customer"
}
```

Failure responses:

- `400` duplicate email
- `400` kitchen email outside `@ejust.edu.eg`
- `422` invalid payload

Example `400` response:

```json
{
  "detail": "Email already registered"
}
```

Example kitchen domain `400` response:

```json
{
  "detail": "Kitchen staff email must end with @ejust.edu.eg"
}
```

### POST `/auth/login`

Covers: FR-02, FR-03

Headers:

```http
Content-Type: application/json
```

Request:

```json
{
  "email": "mina@example.com",
  "password": "password123"
}
```

Success response `200`:

```json
{
  "access_token": "token-value",
  "token_type": "bearer",
  "role": "customer"
}
```

Failure responses:

- `401` invalid credentials
- `422` invalid payload

Example `401` response:

```json
{
  "detail": "Invalid credentials"
}
```

## Menu

### GET `/menu`

Covers: FR-04, NFR-01

Success response `200`:

```json
[
  {
    "id": 1,
    "name": "Chicken Sandwich",
    "price": 80.0,
    "available": true
  }
]
```

Metric: response time under 2 seconds for seeded demo data.

## Orders

### POST `/orders`

Covers: FR-05, FR-06, FR-07, FR-08, FR-13, FR-15, FR-16

Headers:

```http
Content-Type: application/json
Authorization: Bearer token-value
```

Request:

```json
{
  "client_order_key": "unique-client-key",
  "payment_method": "card",
  "payment_status": "paid",
  "items": [
    {
      "menu_item_id": 1,
      "quantity": 2
    }
  ]
}
```

Validation:

- Authenticated customer required.
- `items` must contain at least 1 item.
- `quantity` must be an integer from 1 to 10.
- Reused `client_order_key` must not create duplicate orders.
- `payment_method` is optional and must be `cash`, `card`, or `wallet`.
- `payment_status` is optional and must be `paid` or `unpaid`.

Success response `201`:

```json
{
  "id": 1,
  "status": "pending",
  "items": [
    {
      "menu_item_id": 1,
      "quantity": 2,
      "line_total": 160.0
    }
  ],
  "total": 160.0,
  "payment_method": "card",
  "payment_status": "paid"
}
```

Failure responses:

- `400` empty cart, invalid quantity, duplicate order key conflict
- `401` missing/invalid token
- `403` role not allowed
- `422` invalid payload

Example `400` response:

```json
{
  "detail": "Order must contain at least one item"
}
```

Example `401` response:

```json
{
  "detail": "Unauthorized access"
}
```

Example `403` response:

```json
{
  "detail": "Kitchen role required"
}
```

### GET `/orders/my`

Covers: FR-13, FR-16, NFR-01

Headers:

```http
Authorization: Bearer token-value
```

Authorization: customer role required.

Success response `200`:

```json
[
  {
    "id": 1,
    "status": "preparing",
    "total": 160.0,
    "payment_method": "card",
    "payment_status": "paid",
    "items": [
      {
        "name": "Chicken Sandwich",
        "quantity": 2,
        "line_total": 160.0
      }
    ]
  }
]
```

Failure responses:

- `401` missing/invalid token
- `403` authenticated non-customer user

Example `401` response:

```json
{
  "detail": "Unauthorized access"
}
```

### GET `/orders/kitchen`

Covers: FR-09, FR-11, FR-13, FR-14, FR-15, NFR-01

Headers:

```http
Authorization: Bearer token-value
```

Authorization: kitchen role required.

Success response `200`:

```json
[
  {
    "id": 1,
    "customer_email": "mina@example.com",
    "status": "pending",
    "total": 160.0,
    "payment_method": "card",
    "payment_status": "paid",
    "items": [
      {
        "name": "Chicken Sandwich",
        "quantity": 2
      }
    ]
  }
]
```

Failure responses:

- `401` missing/invalid token
- `403` authenticated non-kitchen user

Example `401` response:

```json
{
  "detail": "Unauthorized access"
}
```

Example `403` response:

```json
{
  "detail": "Kitchen role required"
}
```

### PATCH `/orders/{order_id}/status`

Covers: FR-10, FR-11, FR-12, FR-13

Headers:

```http
Content-Type: application/json
Authorization: Bearer token-value
```

Request:

```json
{
  "status": "preparing"
}
```

Allowed statuses:

- `pending`
- `preparing`
- `ready`
- `completed`

Success response `200`:

```json
{
  "id": 1,
  "status": "preparing"
}
```

Failure responses:

- `400` invalid status
- `401` missing/invalid token
- `403` authenticated non-kitchen user
- `404` order not found

Example `400` response:

```json
{
  "detail": "Invalid order status"
}
```

Example `401` response:

```json
{
  "detail": "Unauthorized access"
}
```

Example `403` response:

```json
{
  "detail": "Kitchen role required"
}
```

Metric: successful update visible from API within 1 second.

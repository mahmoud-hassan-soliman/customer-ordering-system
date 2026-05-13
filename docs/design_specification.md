# Design Specification

## Design Goal

Build one small vertical slice: customer registration/login, menu browsing, cart order submission, kitchen dashboard, and order status update.

The design favors explicit contracts, simple modules, SQLite persistence, and testable service functions.

## Architecture

```mermaid
flowchart LR
    Customer["Customer"] --> React["React Vite UI"]
    Kitchen["Kitchen Staff"] --> React
    React --> API["FastAPI REST API"]
    API --> Auth["Auth Service"]
    API --> MenuSvc["Menu Service"]
    API --> OrderSvc["Order Service"]
    Auth --> DB["SQLite via SQLAlchemy"]
    MenuSvc --> DB
    OrderSvc --> DB
```

## Module Boundaries

| Layer | Responsibility | Hidden Details |
| --- | --- | --- |
| Frontend pages | User workflows and basic client-side validation. | Database, password hashing, SQLAlchemy. |
| API routers | HTTP request/response mapping and auth checks. | Business rule internals. |
| Services | Registration, login, order placement, status update rules. | HTTP framework details. |
| Models | Persistent entities. | UI and test runner details. |
| Schemas | Request/response validation. | Database session internals. |

## System Sequence Diagram: Place Order Happy Path

```mermaid
sequenceDiagram
    actor Customer
    participant UI as React UI
    participant API as FastAPI
    participant Auth as Auth Service
    participant Order as Order Service
    participant DB as SQLite DB

    Customer->>UI: Click Place Order
    UI->>API: POST /orders with token and cart
    API->>Auth: Validate customer token
    Auth-->>API: Customer identity
    API->>Order: create_order(customer, items, client_order_key)
    Order->>DB: Validate menu items and save order
    DB-->>Order: Saved order
    Order-->>API: Order summary with pending status
    API-->>UI: 201 Created
    UI-->>Customer: Show order confirmation
```

## System Sequence Diagram: Empty Cart Failure Path

```mermaid
sequenceDiagram
    actor Customer
    participant UI as React UI
    participant API as FastAPI
    participant Auth as Auth Service
    participant Order as Order Service

    Customer->>UI: Click Place Order with empty cart
    UI->>API: POST /orders with empty items
    API->>Auth: Validate customer token
    Auth-->>API: Customer identity
    API->>Order: create_order(customer, empty_items, client_order_key)
    Order-->>API: Reject empty cart
    API-->>UI: 400 Bad Request
    UI-->>Customer: Show validation message
```

## Activity Diagram: Order Placement

```mermaid
flowchart TD
    A["Start"] --> B["Customer opens menu"]
    B --> C["Add item to cart"]
    C --> D{"Quantity between 1 and 10?"}
    D -- No --> E["Show quantity validation error"]
    E --> C
    D -- Yes --> F["Cart updated"]
    F --> G{"Cart empty at submit?"}
    G -- Yes --> H["Reject order with 400"]
    G -- No --> I["Send POST /orders"]
    I --> J{"Authenticated customer?"}
    J -- No --> K["Reject with 401 or 403"]
    J -- Yes --> L{"Duplicate client order key?"}
    L -- Yes --> M["Return existing order or reject duplicate"]
    L -- No --> N["Persist order as pending"]
    N --> O["Return 201 Created"]
    O --> P["End"]
```

## Activity Diagram: Kitchen Status Update

```mermaid
flowchart TD
    A["Start"] --> B["Kitchen staff opens dashboard"]
    B --> C{"Kitchen role token valid?"}
    C -- No --> D["Reject with 401 or 403"]
    C -- Yes --> E["Load active orders"]
    E --> F["Select new status"]
    F --> G{"Status is allowed?"}
    G -- No --> H["Reject with 400 and keep old status"]
    G -- Yes --> I["Update order status"]
    I --> J["Return updated status within 1 second"]
    J --> K["End"]
```

## Data Model Sketch

| Entity | Fields |
| --- | --- |
| User | id, name, email, password_hash, role |
| MenuItem | id, name, price, available |
| Order | id, customer_id, status, client_order_key, created_at |
| OrderItem | id, order_id, menu_item_id, quantity, line_total |
## Class Diagram

```mermaid
classDiagram
    class User {
        +id
        +name
        +email
        +password_hash
        +role
    }

    class MenuItem {
        +id
        +name
        +price
        +available
    }

    class Order {
        +id
        +customer_id
        +status
        +client_order_key
        +created_at
    }

    class OrderItem {
        +id
        +order_id
        +menu_item_id
        +quantity
        +line_total
    }

    User "1" --> "*" Order : places
    Order "1" --> "*" OrderItem : contains
    MenuItem "1" --> "*" OrderItem : referenced_by
```







## Design Decisions

- Use SQLite for local demo persistence.
- Use service functions for business rules so unit tests can avoid HTTP setup.
- Use API contracts as the boundary between frontend and backend.
- Use a simple bearer token for academic demo authentication.
- Keep cart state in the frontend until order submission succeeds.

## Technology Justification

- FastAPI was selected because it supports small REST APIs with automatic request validation and OpenAPI documentation, which helps keep API contracts measurable and testable.
- SQLite was selected because it is file-based, simple to run locally, and sufficient for a demo-sized ordering workflow without deployment infrastructure.
- React + Vite was selected because it provides a lightweight frontend setup with fast local development and minimal configuration.
- pytest was selected for backend unit and integration tests because it supports clear boundary-focused tests; Playwright was selected for E2E validation because it can execute browser workflows using the Page Object Model.

## Traceability

Each diagram and endpoint maps to the requirement IDs in `traceability_matrix.md` and `api_contracts.md`.

# Customer Ordering System

Small Software Engineering term project for CSE323. The project implements a minimal customer-to-kitchen ordering workflow and emphasizes requirements engineering, traceability, TDD evidence, automated testing, and validation.

## Project Overview

Implemented features:

- Register and login
- View menu
- Add items to cart
- Place order
- Kitchen dashboard
- Update order status

Intentionally out of scope:

- Payments
- Notifications
- Analytics
- Admin management systems
- Docker
- Redis
- PostgreSQL
- Cloud deployment
- Redux or complex frontend state management

## Technology Stack

Backend:

- Python
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic

Frontend:

- React
- Vite
- Simple CSS
- Browser `fetch`

Testing:

- pytest for unit and integration tests
- FastAPI `TestClient` for API contract tests
- Playwright for browser-level E2E smoke workflows

## Architecture Summary

The project uses one small vertical slice:

```text
React UI -> FastAPI routers -> service layer -> SQLAlchemy models -> SQLite
```

Backend organization:

- `backend/app/main.py`: FastAPI app setup and CORS.
- `backend/app/routers/`: HTTP endpoints.
- `backend/app/services/`: business rules.
- `backend/app/models/`: SQLAlchemy models.
- `backend/app/schemas/`: Pydantic schemas.
- `backend/app/db/`: SQLite session and seed setup.
- `backend/app/auth/`: simple bearer-token helpers.

Frontend organization:

- `frontend/src/pages/`: Register, login, menu, cart, and kitchen dashboard pages.
- `frontend/src/components/`: shared navigation and message components.
- `frontend/src/services/api.js`: API client for the documented backend endpoints.

## Project Structure

```text
FinalProject/
├── backend/
│   ├── app/
│   │   ├── auth/
│   │   ├── db/
│   │   ├── models/
│   │   ├── routers/
│   │   ├── schemas/
│   │   └── services/
│   └── requirements.txt
├── docs/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   └── tests/e2e/
├── tests/
│   ├── integration/
│   ├── unit/
│   └── utils/
├── screenshots/
├── demo/
└── README.md
```

## Documentation

- `docs/requirements_report.md`
- `docs/design_specification.md`
- `docs/validation_report.md`
- `docs/traceability_matrix.md`
- `docs/gherkin_scenarios.md`
- `docs/qa_refinement_log.md`
- `docs/api_contracts.md`
- `docs/verification_vs_validation.md`
- `docs/testing_pyramid_report.md`
- `docs/playwright_automation.md`
- `docs/tdp_iteration_evidence.md`

## Backend Setup

```bash
cd "/Volumes/My Macbook/Study/Semester 8/Software Engineering/Projects/FinalProject"
python3 -m venv backend/venv
source backend/venv/bin/activate
pip install -r backend/requirements.txt
```

Run backend:

```bash
cd "/Volumes/My Macbook/Study/Semester 8/Software Engineering/Projects/FinalProject"
PYTHONPATH=backend python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Backend URL:

```text
http://127.0.0.1:8000
```

## Frontend Setup

```bash
cd "/Volumes/My Macbook/Study/Semester 8/Software Engineering/Projects/FinalProject/frontend"
npm install
```

Run frontend:

```bash
cd "/Volumes/My Macbook/Study/Semester 8/Software Engineering/Projects/FinalProject/frontend"
npm run dev
```

Frontend URL:

```text
http://127.0.0.1:5173
```

Build frontend:

```bash
cd "/Volumes/My Macbook/Study/Semester 8/Software Engineering/Projects/FinalProject/frontend"
npm run build
```

## Pytest Commands

Run all backend tests:

```bash
cd "/Volumes/My Macbook/Study/Semester 8/Software Engineering/Projects/FinalProject"
pytest
```

Run unit tests only:

```bash
pytest tests/unit
```

Run integration tests only:

```bash
pytest tests/integration
```

## Playwright Commands

Start the backend and frontend first:

```bash
cd "/Volumes/My Macbook/Study/Semester 8/Software Engineering/Projects/FinalProject"
PYTHONPATH=backend python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

```bash
cd "/Volumes/My Macbook/Study/Semester 8/Software Engineering/Projects/FinalProject/frontend"
npm run dev
```

Run Playwright tests:

```bash
cd "/Volumes/My Macbook/Study/Semester 8/Software Engineering/Projects/FinalProject/frontend"
npx playwright test tests/e2e
```

## Demo Workflow

1. Register a customer.
2. Log in as the customer.
3. View the seeded menu.
4. Add an item to the cart.
5. Place an order.
6. Register or log in as kitchen staff.
7. Open the kitchen dashboard.
8. Update the order status.

## GitHub Structure Explanation

The repository is organized by engineering evidence:

- `docs/` contains rubric-facing reports and traceability evidence.
- `backend/` contains the FastAPI implementation.
- `frontend/` contains the Vite React implementation and Playwright tests.
- `tests/` contains pytest unit and integration tests.
- `screenshots/` is reserved for demo and validation screenshots.
- `demo/` is reserved for presentation/demo support material.


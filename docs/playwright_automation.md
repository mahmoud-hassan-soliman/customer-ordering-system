# Playwright Automation

## Purpose

Playwright provides browser-level validation for the React frontend. The tests confirm that the implemented UI can be opened in a real browser context and can communicate with the FastAPI backend for the main demo workflow.

## Setup

Playwright is listed in `frontend/package.json` as a development dependency:

```json
"@playwright/test": "^1.60.0"
```

The current E2E tests are located in:

- `frontend/tests/e2e/login.spec.js`
- `frontend/tests/e2e/menu.spec.js`

The tests expect:

- Backend running at `http://127.0.0.1:8000`
- Frontend running at `http://127.0.0.1:5173`

## E2E Workflow Coverage

| Playwright Test | Workflow | Related Requirements |
| --- | --- | --- |
| `menu.spec.js` | Opens the homepage and verifies that the login workflow is visible. | FR-02 |
| `login.spec.js` | Registers a new user, logs in through the UI, and verifies seeded menu items are visible. | FR-01, FR-02, FR-04 |

The Playwright suite intentionally stays small. Backend unit and integration tests cover edge cases such as invalid quantity, empty cart, duplicate order key, unauthorized kitchen access, invalid status, and invalid token rejection.

## Relationship To Gherkin

The Playwright tests implement browser-level slices of the Gherkin scenarios:

- `Feature: Frontend smoke workflows`
- `Scenario: Homepage loads`
- `Scenario: Register, login, and view seeded menu`

Gherkin scenarios remain the readable specification. Playwright scripts are the executable browser automation evidence.

## Regression Testing Value

Playwright protects the project against regressions that backend-only tests cannot see, including:

- The frontend route/page renders correctly.
- Form labels and buttons remain discoverable by accessible role or label.
- Browser registration and login flow still works after frontend changes.
- The menu page displays data returned by the backend.

## Run Command

Start the backend:

```bash
cd "/Volumes/My Macbook/Study/Semester 8/Software Engineering/Projects/FinalProject"
PYTHONPATH=backend /Users/mahmoudhasssan/anaconda3/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Start the frontend:

```bash
cd "/Volumes/My Macbook/Study/Semester 8/Software Engineering/Projects/FinalProject/frontend"
npm run dev
```

Run Playwright:

```bash
cd "/Volumes/My Macbook/Study/Semester 8/Software Engineering/Projects/FinalProject/frontend"
npx playwright test tests/e2e
```


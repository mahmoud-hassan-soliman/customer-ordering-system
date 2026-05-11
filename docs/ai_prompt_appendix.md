# AI Assistance Appendix

## Purpose

This appendix documents how Codex/AI assistance was used during the Customer Ordering System project. AI support was used as an engineering assistant for requirements analysis, test design, implementation scaffolding, debugging, refactoring, and documentation. Human project constraints controlled the scope: the system remained minimal, rubric-focused, and limited to the implemented customer ordering workflow.

No secrets, private credentials, API keys, or sensitive personal data were included in prompts.

## How AI Tools Were Used

AI assistance was used to:

- Interpret the project overview and grading rubric.
- Convert rubric expectations into requirements, traceability, Gherkin scenarios, API contracts, and validation evidence.
- Create failing-first pytest tests before backend implementation.
- Implement the minimal FastAPI, SQLite, SQLAlchemy backend needed to satisfy the tests.
- Build a small React/Vite frontend connected to the documented backend APIs.
- Debug test failures and a duplicate-registration defect.
- Refactor Playwright E2E tests into Page Object Model structure.
- Finalize documentation for verification, validation, testing pyramid evidence, Playwright automation, and TDP iteration evidence.

AI assistance did not add unsupported features such as payments, notifications, analytics, Docker, Redis, PostgreSQL, cloud deployment, or advanced authentication.

## Prompt Categories Used

| Prompt Category | Purpose | Project Artifact Impact |
| --- | --- | --- |
| Requirements prompts | Extract actors, requirements, edge cases, and traceability from the rubric. | `requirements_report.md`, `traceability_matrix.md` |
| Design prompts | Define Gherkin scenarios, API contracts, UML diagrams, and technology justification. | `gherkin_scenarios.md`, `api_contracts.md`, `design_specification.md` |
| Testing prompts | Create failing-first unit and integration tests with requirement IDs. | `tests/unit/`, `tests/integration/`, `pytest.ini` |
| Implementation prompts | Implement only the backend/frontend behavior required by tests and API contracts. | `backend/`, `frontend/src/` |
| Debugging prompts | Diagnose failing tests and manual QA defects. | Duplicate registration regression tests and fix |
| Refactoring prompts | Convert Playwright tests to Page Object Model without changing behavior. | `frontend/tests/pages/`, `frontend/tests/e2e/` |
| Documentation prompts | Finalize validation, testing pyramid, Playwright, TDP, README, and audit docs. | `docs/`, `README.md` |

## Representative Requirement Prompts

Examples of requirement-focused prompts used:

- Analyze the project PDFs and create actor classification, traceability heatmap, persona discovery, and edge cases.
- Keep the project minimal and focused on the required Customer Ordering System features only.
- Add a requirement for expired or invalid access token rejection and preserve existing requirement IDs.
- Verify that all requirements map to features, API contracts, tests, and validation evidence.

These prompts supported requirements engineering and traceability rather than feature expansion.

## Representative Testing Prompts

Examples of testing-focused prompts used:

- Create a failing pytest suite before backend implementation.
- Cover FR-01 through FR-13 with unit and integration tests.
- Include edge-case padlocks for invalid quantities, empty cart, duplicate order key, invalid token, unauthorized kitchen access, and invalid status.
- Run pytest and report which tests fail before implementation.
- Preserve requirement IDs in test names or docstrings.

These prompts produced TDD evidence and helped keep implementation tied to measurable behavior.

## Representative Debugging Prompts

Examples of debugging-focused prompts used:

- Fix the duplicate registration bug with minimal changes only.
- Add or update tests so duplicate email registration fails correctly.
- Return a structured backend error message such as `Email already registered`.
- Verify existing tests still pass and the frontend displays backend validation messages.

The duplicate-registration bug was handled with a regression-first workflow: tests were added first, then the service behavior was corrected.

## Representative Refactoring Prompts

Examples of refactoring-focused prompts used:

- Refactor existing Playwright tests to use Page Object Model.
- Keep current tested behavior exactly the same.
- Create reusable page object classes under `frontend/tests/pages/`.
- Do not change application implementation code.

This produced reusable Playwright page objects for navigation, registration, login, and menu assertions.

## Representative Documentation Prompts

Examples of documentation-focused prompts used:

- Improve Gherkin scenarios with happy paths, failure paths, and edge cases.
- Create testing pyramid evidence with unit, integration, and E2E counts.
- Document verification versus validation using pytest, Playwright, ordering workflow, and kitchen workflow evidence.
- Create Playwright automation and TDP iteration evidence documents.
- Run a final submission audit for generated files, caches, README accuracy, and command verification.

These prompts helped align the final submission with the rubric.

## Human Oversight And Constraints

The project scope and implementation constraints were explicitly controlled:

- The selected subsystem remained a small Customer Ordering System.
- Only required features were implemented.
- Tests and documentation were checked against current implementation.
- Generated artifacts and cache files were removed or ignored before submission.
- Implementation changes were avoided during final documentation and audit phases.

## AI Use Disclosure Summary

Codex/AI assistance was used throughout the project as a guided development and documentation assistant. The final project artifacts remain aligned with the stated academic requirements: requirements discovery, traceability, software design, TDD evidence, testing, validation, and engineering process quality.


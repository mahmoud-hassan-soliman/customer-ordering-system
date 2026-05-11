"""Shared pytest fixtures for failing-first backend tests.

These fixtures intentionally fail with clear TDD messages until the backend
FastAPI app and service modules are implemented in the next phase.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

from tests.utils.seed_data import (
    CUSTOMER_USER,
    INVALID_TOKEN,
    KITCHEN_USER,
    MENU_ITEMS,
    VALID_CLIENT_ORDER_KEY,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = PROJECT_ROOT / "backend"

for path in (PROJECT_ROOT, BACKEND_ROOT):
    path_text = str(path)
    if path_text not in sys.path:
        sys.path.insert(0, path_text)


@pytest.fixture(autouse=True)
def clean_backend_database():
    """Start each test with a clean seeded database once implementation exists."""

    try:
        init_module = importlib.import_module("app.db.init_db")
        security_module = importlib.import_module("app.auth.security")
    except Exception:
        yield
        return

    init_module.reset_db()
    if hasattr(security_module, "_TOKENS"):
        security_module._TOKENS.clear()
    yield


def _missing_backend_failure(target: str, exc: Exception) -> None:
    pytest.fail(
        f"TDD failing-first evidence: expected backend target '{target}' is not "
        f"implemented yet. Original error: {exc}",
        pytrace=False,
    )


@pytest.fixture()
def customer_payload() -> dict:
    return dict(CUSTOMER_USER)


@pytest.fixture()
def kitchen_payload() -> dict:
    return dict(KITCHEN_USER)


@pytest.fixture()
def seeded_menu_items() -> list[dict]:
    return [dict(item) for item in MENU_ITEMS]


@pytest.fixture()
def valid_order_payload() -> dict:
    return {
        "client_order_key": VALID_CLIENT_ORDER_KEY,
        "items": [{"menu_item_id": 1, "quantity": 2}],
    }


@pytest.fixture()
def invalid_token() -> str:
    return INVALID_TOKEN


@pytest.fixture()
def service_modules():
    """Load planned service modules.

    Expected implementation targets:
    - app.services.auth_service
    - app.services.menu_service
    - app.services.order_service
    """

    modules = {}
    for target in (
        "app.services.auth_service",
        "app.services.menu_service",
        "app.services.order_service",
    ):
        try:
            modules[target.rsplit(".", 1)[-1]] = importlib.import_module(target)
        except Exception as exc:  # pragma: no cover - intentionally fails first
            _missing_backend_failure(target, exc)
    return modules


@pytest.fixture()
def fastapi_app():
    """Load the planned FastAPI application object."""

    try:
        main = importlib.import_module("app.main")
    except Exception as exc:  # pragma: no cover - intentionally fails first
        _missing_backend_failure("app.main", exc)

    app = getattr(main, "app", None)
    if app is None and hasattr(main, "create_app"):
        app = main.create_app()
    if app is None:
        pytest.fail(
            "TDD failing-first evidence: app.main must expose 'app' or "
            "'create_app()'.",
            pytrace=False,
        )
    return app


@pytest.fixture()
def client(fastapi_app):
    """FastAPI TestClient fixture for integration tests."""

    try:
        from fastapi.testclient import TestClient
    except Exception as exc:  # pragma: no cover - dependency may not exist yet
        pytest.fail(
            f"FastAPI TestClient is unavailable. Install backend test "
            f"dependencies before implementation verification. Original error: {exc}",
            pytrace=False,
        )
    return TestClient(fastapi_app)


@pytest.fixture()
def auth_headers(client, customer_payload) -> dict:
    """Register/login a customer and return bearer headers."""

    client.post("/auth/register", json=customer_payload)
    response = client.post(
        "/auth/login",
        json={
            "email": customer_payload["email"],
            "password": customer_payload["password"],
        },
    )
    token = response.json().get("access_token")
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def kitchen_headers(client, kitchen_payload) -> dict:
    """Register/login kitchen staff and return bearer headers."""

    client.post("/auth/register", json=kitchen_payload)
    response = client.post(
        "/auth/login",
        json={
            "email": kitchen_payload["email"],
            "password": kitchen_payload["password"],
        },
    )
    token = response.json().get("access_token")
    return {"Authorization": f"Bearer {token}"}

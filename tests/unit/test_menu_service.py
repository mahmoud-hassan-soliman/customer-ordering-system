"""Failing-first unit tests for menu retrieval."""

import pytest


pytestmark = [pytest.mark.unit, pytest.mark.tdd]


def test_fr_04_menu_retrieval_returns_seeded_items(service_modules, seeded_menu_items):
    """FR-04, NFR-01: menu retrieval returns at least 3 demo items."""

    menu_service = service_modules["menu_service"]

    items = menu_service.list_menu_items()

    assert len(items) >= 3
    assert {item.name for item in items} >= {item["name"] for item in seeded_menu_items}


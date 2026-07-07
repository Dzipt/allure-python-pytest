import json
import os
from datetime import datetime, timezone

import allure
import pytest


def pytest_configure(config):
    config.addinivalue_line("markers", "testops_demo: demo suite for TestOps presentations")
    config.addinivalue_line("markers", "api: API checks")
    config.addinivalue_line("markers", "ui: UI checks")
    config.addinivalue_line("markers", "mobile: mobile checks")
    config.addinivalue_line("markers", "contract: contract checks")
    config.addinivalue_line("markers", "flaky_demo: controlled flaky checks for demo launches")
    config.addinivalue_line("markers", "manual_demo: generated manual checks for demo launches")


@pytest.fixture
def demo_context():
    run_variant = os.getenv("TESTOPS_DEMO_RUN", "1")
    context = {
        "project": "QATools Demo Shop",
        "environment": os.getenv("TESTOPS_DEMO_ENV", "stage"),
        "release": os.getenv("TESTOPS_DEMO_RELEASE", "2026.07-demo"),
        "run_variant": run_variant,
        "started_at": datetime.now(timezone.utc).isoformat(),
    }
    allure.dynamic.label("environment", context["environment"])
    allure.dynamic.label("release", context["release"])
    allure.attach(
        json.dumps(context, indent=2),
        name="Demo launch context",
        attachment_type=allure.attachment_type.JSON,
    )
    return context


@pytest.fixture
def demo_user():
    user = {
        "id": "USR-1042",
        "email": "demo.customer@qatools.example",
        "loyalty_tier": "gold",
        "cart_total": 7390,
    }
    allure.attach(
        json.dumps(user, indent=2),
        name="Customer profile",
        attachment_type=allure.attachment_type.JSON,
    )
    return user

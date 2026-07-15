import json
import os
import random
from datetime import datetime, timezone

import allure
import pytest


def pytest_configure(config):
    config.addinivalue_line("markers", "testops_demo: demo suite for TestOps presentations")
    config.addinivalue_line("markers", "unit: unit checks")
    config.addinivalue_line("markers", "api: API checks")
    config.addinivalue_line("markers", "e2e: end-to-end checks")
    config.addinivalue_line("markers", "flaky_demo: controlled flaky checks for demo launches")
    config.addinivalue_line("markers", "manual_demo: generated manual checks for demo launches")


@pytest.fixture
def demo_context():
    run_variant = os.getenv("TESTOPS_DEMO_RUN", "1")
    context = {
        "project": "Демо-магазин QATools",
        "environment": os.getenv("TESTOPS_DEMO_ENV", "stage"),
        "browser": os.getenv("TESTOPS_DEMO_BROWSER", os.getenv("BROWSER", "chrome")),
        "platform": os.getenv("TESTOPS_DEMO_PLATFORM", os.getenv("PLATFORM", "ubuntu-latest")),
        "release": os.getenv("TESTOPS_DEMO_RELEASE", "2026.07-demo"),
        "run_type": os.getenv("RUN_TYPE", "regression"),
        "run_variant": run_variant,
        "branch": os.getenv("TESTOPS_DEMO_BRANCH", os.getenv("BRANCH", "local")),
        "started_at": datetime.now(timezone.utc).isoformat(),
    }
    allure.dynamic.label("environment", context["environment"])
    allure.dynamic.label("release", context["release"])
    allure.attach(
        json.dumps(context, indent=2, ensure_ascii=False),
        name="Контекст запуска",
        attachment_type=allure.attachment_type.JSON,
    )
    return context


@pytest.fixture
def demo_user():
    user = {
        "id": "USR-1042",
        "email": "demo.customer@qatools.example",
        "loyalty_tier": "Золотой",
        "cart_total": 7390,
        "name": "Анна Смирнова",
        "city": "Москва",
    }
    allure.attach(
        json.dumps(user, indent=2, ensure_ascii=False),
        name="Профиль покупателя",
        attachment_type=allure.attachment_type.JSON,
    )
    return user


@pytest.fixture
def flaky_demo_check():
    def check(scenario):
        with allure.step("Проверить результат нестабильного демо-сценария"):
            failure_roll = random.random()
            allure.attach(
                f"{failure_roll:.6f}",
                name=f"Случайное значение: {scenario}",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert failure_roll >= 0.5, (
                f"Имитация нестабильного сбоя с вероятностью 50%: "
                f"{scenario}, значение {failure_roll:.6f}"
            )

    return check

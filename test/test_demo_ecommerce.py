# test_demo_ecommerce.py
import random
import allure
import pytest
from allure_commons.types import Severity

# ============================================================
# ДАННЫЕ ДЛЯ ТЕСТОВ
# ============================================================

# 1000 наборов данных для тестов
TEST_DATA = []

# Authentication (50)
for i in range(1, 51):
    TEST_DATA.append({
        "id": f"AUTH-{i:03d}",
        "feature": "Authentication",
        "story": "User Registration" if i <= 20 else ("User Login" if i <= 40 else "Password Reset"),
        "title": f"Auth scenario {i}: {random.choice(['valid credentials', 'invalid password', 'locked account', 'email exists'])}",
        "passes": i not in [18, 29, 35, 38, 47],
        "flake": i in [20, 40],
        "scenario": "auth"
    })

# Catalog (100)
for i in range(51, 151):
    TEST_DATA.append({
        "id": f"CAT-{i-50:03d}",
        "feature": "Catalog",
        "story": random.choice(["Product Search", "Product Filters", "Product Details"]),
        "title": f"Catalog scenario {i-50}: {random.choice(['search by name', 'filter by category', 'view details'])}",
        "passes": i not in [62, 73, 86, 99, 112, 123, 134, 145],
        "flake": i in [150],
        "scenario": "catalog"
    })

# Shopping Cart (150)
for i in range(151, 301):
    TEST_DATA.append({
        "id": f"CART-{i-150:03d}",
        "feature": "Shopping Cart",
        "story": random.choice(["Add to Cart", "Remove from Cart", "Update Cart", "Cart Total"]),
        "title": f"Cart scenario {i-150}: {random.choice(['add item', 'remove item', 'update quantity', 'calculate total'])}",
        "passes": i not in [155, 168, 182, 195, 208, 222, 235, 248, 259, 272, 285, 298],
        "flake": i in [160, 200, 250, 300],
        "scenario": "cart"
    })

# Payment Processing (300)
for i in range(301, 601):
    TEST_DATA.append({
        "id": f"PAY-{i-300:03d}",
        "feature": "Payment Processing",
        "story": random.choice(["Credit Card", "PayPal", "Bank Transfer", "Gift Cards", "Refunds"]),
        "title": f"Payment scenario {i-300}: {random.choice(['process payment', 'decline', 'refund', 'history'])}",
        "passes": i not in [312, 327, 343, 358, 372, 389, 405, 418, 432, 447, 463, 478, 492, 508, 523, 538, 552, 567, 583, 598],
        "flake": i in [350, 400, 450, 500, 550, 600],
        "scenario": "payment"
    })

# Order Management (150)
for i in range(601, 751):
    TEST_DATA.append({
        "id": f"ORD-{i-600:03d}",
        "feature": "Order Management",
        "story": random.choice(["Order Creation", "Order Status", "Order History", "Cancellation"]),
        "title": f"Order scenario {i-600}: {random.choice(['create order', 'check status', 'view history', 'cancel'])}",
        "passes": i not in [608, 623, 639, 654, 668, 678, 692, 705, 719, 726, 734, 746],
        "flake": i in [700, 750],
        "scenario": "order"
    })

# User Profile (50)
for i in range(751, 801):
    TEST_DATA.append({
        "id": f"PROF-{i-750:03d}",
        "feature": "User Profile",
        "story": random.choice(["Profile Management", "Address Management", "User Preferences"]),
        "title": f"Profile scenario {i-750}: {random.choice(['view profile', 'add address', 'update preferences'])}",
        "passes": i not in [757, 764, 778, 785, 792],
        "flake": False,
        "scenario": "profile"
    })

print(f"✅ Total test cases: {len(TEST_DATA)}")


# ============================================================
# ОДНА ПАРАМЕТРИЗИРОВАННАЯ ФУНКЦИЯ
# ============================================================

@allure.epic("E-Commerce Platform")
@pytest.mark.parametrize("test_data", TEST_DATA, ids=lambda x: x["id"])
def test_ecommerce_scenario(test_data):
    """
    Единая параметризированная функция для всех тестов.
    Allure TestOps создаёт отдельный тест-кейс для каждого набора данных.
    """
    
    # Динамические аттрибуты Allure (работают во время выполнения)
    allure.dynamic.title(test_data["title"])
    allure.dynamic.feature(test_data["feature"])
    allure.dynamic.story(test_data["story"])
    allure.dynamic.severity(Severity.CRITICAL if "Critical" in test_data.get("severity", "") else Severity.NORMAL)
    
    test_id = test_data["id"]
    should_pass = test_data["passes"]
    is_flaky = test_data.get("flake", False)
    scenario = test_data["scenario"]
    
    with allure.step(f"Execute scenario: {scenario}"):
        # --- Симуляция бизнес-логики ---
        with allure.step("Prepare test data"):
            result = {"status": "processing"}
            allure.attach(f"Test ID: {test_id}", "Test Info", allure.attachment_type.TEXT)
        
        with allure.step("Execute business operation"):
            # Имитация работы с разными вероятностями успеха
            success_probability = 0.98
            if not should_pass:
                success_probability = 0.1
            
            # Flaky тесты имеют нестабильную вероятность успеха
            if is_flaky:
                success_probability = 0.6
            
            # Случайное решение о прохождении теста
            if random.random() > success_probability:
                if is_flaky:
                    pytest.fail(f"Flaky failure in {test_id} - retry may succeed")
                elif not should_pass:
                    failure_reasons = [
                        "Validation failed: expected value does not match actual",
                        "Business rule violation: invalid operation",
                        "Integration error: external service unavailable",
                        "Permission denied: insufficient rights",
                        "Data consistency error: state mismatch"
                    ]
                    reason = random.choice(failure_reasons)
                    pytest.fail(f"[{test_id}] {reason}")
                else:
                    # Редкие непредвиденные падения (1-2% шума)
                    if random.random() < 0.02:
                        raise Exception(f"Unexpected error in {test_id}")
        
        with allure.step("Verify result"):
            assert True, f"Test {test_id} passed successfully"


# ============================================================
# ОТДЕЛЬНЫЙ ТЕСТ ДЛЯ СТАТИСТИКИ (опционально)
# ============================================================

@allure.id("DEMO-STATS")
@allure.epic("E-Commerce Platform")
@allure.feature("Test Statistics")
@allure.title("Verify test suite statistics")
@allure.severity(Severity.NORMAL)
def test_demo_statistics():
    """Проверяет, что у нас правильное количество тестов"""
    
    with allure.step("Count total test cases"):
        total = len(TEST_DATA)
    
    with allure.step("Count expected passing tests"):
        passed = sum(1 for t in TEST_DATA if t["passes"])
    
    with allure.step("Count expected failing tests"):
        failed = sum(1 for t in TEST_DATA if not t["passes"])
    
    with allure.step("Count flaky tests"):
        flaky = sum(1 for t in TEST_DATA if t.get("flake", False))
    
    with allure.step("Verify counts"):
        assert total == 800, f"Expected 800 test cases, got {total}"
        assert failed == 50, f"Expected 50 failing tests, got {failed}"
        assert flaky == 20, f"Expected 20 flaky tests, got {flaky}"
    
    allure.attach(
        f"Total test cases: {total}\n"
        f"Passing (expected): {passed}\n"
        f"Failing: {failed}\n"
        f"Flaky: {flaky}",
        "Test Statistics",
        allure.attachment_type.TEXT
    )


# ============================================================
# КОГДА ПАРАМЕТРИЗАЦИЯ НЕ РАБОТАЕТ
# ============================================================

# Если вы хотите, чтобы каждый тест был отдельной функцией
# (иногда нужно для более сложных сценариев), используйте:

def create_test(data):
    @pytest.mark.parametrize("_", [None])
    def test():
        allure.dynamic.id(data["id"])
        allure.dynamic.title(data["title"])
        # ... логика теста
    test.__name__ = f"test_{data['id'].replace('-', '_')}"
    return test

# Затем добавляем в глобальную область ПЕРЕД сбором тестов
# for data in TEST_DATA:
#     globals()[f"test_{data['id'].replace('-', '_')}"] = create_test(data)
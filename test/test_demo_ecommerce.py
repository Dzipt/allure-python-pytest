# test_demo_ecommerce.py
import random
import allure
import pytest
from allure_commons.types import Severity

# ============================================================
# 1. БИЗНЕС-ЛОГИКА (моки для демо)
# ============================================================

class User:
    def __init__(self, id, email, password, tier="standard"):
        self.id = id
        self.email = email
        self.password = password
        self.tier = tier
        self.cart = []
        self.orders = []

class Product:
    def __init__(self, id, name, price, category, in_stock=True):
        self.id = id
        self.name = name
        self.price = price
        self.category = category
        self.in_stock = in_stock

class ShoppingCart:
    def __init__(self, user):
        self.user = user
        self.items = []
    
    def add(self, product, quantity=1):
        if not product.in_stock:
            raise ValueError(f"Product {product.name} is out of stock")
        self.items.append({"product": product, "quantity": quantity})
    
    def remove(self, product_id):
        self.items = [i for i in self.items if i["product"].id != product_id]
    
    def total(self):
        return sum(i["product"].price * i["quantity"] for i in self.items)

class CheckoutService:
    def process(self, cart, payment_method):
        if not cart.items:
            raise ValueError("Cart is empty")
        if payment_method == "expired_card":
            raise ValueError("Payment method expired")
        if payment_method == "declined":
            return {"status": "declined", "message": "Insufficient funds"}
        return {"status": "success", "order_id": random.randint(10000, 99999)}

class PaymentGateway:
    def charge(self, amount, card):
        if random.random() < 0.03:  # 3% flaky failure
            raise TimeoutError("Gateway timeout")
        if random.random() < 0.02:  # 2% flaky failure  
            return {"status": "failed", "message": "Network error"}
        return {"status": "success", "transaction_id": f"txn_{random.randint(1000, 9999)}"}

# Global mocks
USERS = {
    i: User(
        id=i,
        email=f"user{i}@example.com",
        password=f"pass{i}",
        tier=random.choice(["standard", "premium", "guest"])
    )
    for i in range(1, 101)
}

PRODUCTS = [
    Product(1, "Gaming Laptop", 999.99, "Electronics"),
    Product(2, "Wireless Mouse", 29.99, "Accessories"),
    Product(3, "USB-C Cable", 15.99, "Accessories"),
    Product(4, "4K Monitor", 349.99, "Electronics"),
    Product(5, "Bluetooth Headphones", 89.99, "Audio"),
    Product(6, "Coffee Mug", 12.99, "Kitchen"),
    Product(7, "T-Shirt", 19.99, "Clothing"),
    Product(8, "Running Shoes", 79.99, "Sports"),
    Product(9, "Backpack", 49.99, "Bags"),
    Product(10, "Phone Charger", 24.99, "Accessories"),
]


# ============================================================
# 2. СЦЕНАРИИ ДЛЯ ГЕНЕРАЦИИ ТЕСТОВ
# ============================================================

def generate_auth_tests():
    """50 тестов: регистрация, логин, восстановление пароля"""
    tests = []
    
    # Registration (20 tests)
    for i in range(1, 21):
        tests.append({
            "id": f"AUTH-{i:03d}",
            "feature": "Authentication",
            "story": "User Registration",
            "title": f"User registration with {random.choice(['valid', 'valid', 'valid', 'valid', 'missing_field', 'weak_password'])} credentials",
            "epic": "E-Commerce Platform",
            "severity": Severity.CRITICAL if i < 5 else Severity.NORMAL,
            "scenario": "registration",
            "data": {"user_id": i},
            "passes": i != 18,  # one failing test: AUTH-018
            "flake": i == 20,   # one flaky test: AUTH-020
        })
    
    # Login (20 tests)
    for i in range(21, 41):
        tests.append({
            "id": f"AUTH-{i:03d}",
            "feature": "Authentication",
            "story": "User Login",
            "title": f"User login with {random.choice(['correct', 'correct', 'correct', 'correct', 'incorrect_password', 'locked_account'])} credentials",
            "epic": "E-Commerce Platform",
            "severity": Severity.CRITICAL if i < 25 else Severity.NORMAL,
            "scenario": "login",
            "data": {"user_id": i},
            "passes": i not in [29, 35, 38],
            "flake": i == 40,
        })
    
    # Password Reset (10 tests)
    for i in range(41, 51):
        tests.append({
            "id": f"AUTH-{i:03d}",
            "feature": "Authentication",
            "story": "Password Reset",
            "title": f"Password reset for {random.choice(['existing_user', 'existing_user', 'existing_user', 'nonexistent_user'])}",
            "epic": "E-Commerce Platform",
            "severity": Severity.NORMAL,
            "scenario": "reset_password",
            "data": {"user_id": i},
            "passes": i != 47,
            "flake": False,
        })
    
    return tests


def generate_catalog_tests():
    """100 тестов: поиск, фильтры, детали товара"""
    tests = []
    
    # Search (40 tests)
    for i in range(1, 41):
        query = random.choice(["laptop", "mouse", "monitor", "headphones", "shoes", "bag", "charger"])
        tests.append({
            "id": f"CAT-{i:03d}",
            "feature": "Catalog",
            "story": "Product Search",
            "title": f"Search products by '{query}'",
            "epic": "E-Commerce Platform",
            "severity": Severity.CRITICAL if i < 10 else Severity.NORMAL,
            "scenario": "search",
            "data": {"query": query},
            "passes": i not in [12, 23, 34],
            "flake": i in [39, 40],
        })
    
    # Filters (30 tests)
    for i in range(41, 71):
        category = random.choice(["Electronics", "Accessories", "Audio", "Clothing", "Sports", "Kitchen"])
        tests.append({
            "id": f"CAT-{i:03d}",
            "feature": "Catalog",
            "story": "Product Filters",
            "title": f"Filter products by category '{category}'",
            "epic": "E-Commerce Platform",
            "severity": Severity.NORMAL,
            "scenario": "filter",
            "data": {"category": category},
            "passes": i not in [42, 55, 68, 69],
            "flake": i == 70,
        })
    
    # Product Details (30 tests)
    for i in range(71, 101):
        product = random.choice(PRODUCTS)
        tests.append({
            "id": f"CAT-{i:03d}",
            "feature": "Catalog",
            "story": "Product Details",
            "title": f"View product details for '{product.name}'",
            "epic": "E-Commerce Platform",
            "severity": Severity.NORMAL,
            "scenario": "details",
            "data": {"product_id": product.id},
            "passes": i not in [73, 86, 99],
            "flake": i == 100,
        })
    
    return tests


def generate_cart_tests():
    """150 тестов: добавление, удаление, обновление корзины"""
    tests = []
    
    # Add to cart (50 tests)
    for i in range(1, 51):
        product = random.choice(PRODUCTS)
        quantity = random.choice([1, 2, 3, 5])
        tests.append({
            "id": f"CART-{i:03d}",
            "feature": "Shopping Cart",
            "story": "Add to Cart",
            "title": f"Add {quantity} x '{product.name}' to cart",
            "epic": "E-Commerce Platform",
            "severity": Severity.CRITICAL if i < 15 else Severity.NORMAL,
            "scenario": "add_to_cart",
            "data": {"product_id": product.id, "quantity": quantity},
            "passes": i not in [8, 22, 35, 44],
            "flake": i in [48, 50],
        })
    
    # Remove from cart (40 tests)
    for i in range(51, 91):
        product = random.choice(PRODUCTS)
        tests.append({
            "id": f"CART-{i:03d}",
            "feature": "Shopping Cart",
            "story": "Remove from Cart",
            "title": f"Remove '{product.name}' from cart",
            "epic": "E-Commerce Platform",
            "severity": Severity.NORMAL,
            "scenario": "remove_from_cart",
            "data": {"product_id": product.id},
            "passes": i not in [55, 68, 82],
            "flake": i == 90,
        })
    
    # Update cart (30 tests)
    for i in range(91, 121):
        product = random.choice(PRODUCTS)
        tests.append({
            "id": f"CART-{i:03d}",
            "feature": "Shopping Cart",
            "story": "Update Cart",
            "title": f"Update quantity of '{product.name}' in cart",
            "epic": "E-Commerce Platform",
            "severity": Severity.NORMAL,
            "scenario": "update_cart",
            "data": {"product_id": product.id},
            "passes": i not in [95, 108, 115],
            "flake": False,
        })
    
    # Cart total (30 tests)
    for i in range(121, 151):
        tests.append({
            "id": f"CART-{i:03d}",
            "feature": "Shopping Cart",
            "story": "Cart Total",
            "title": f"Calculate cart total with {random.choice(['multiple_items', 'discount', 'empty'])}",
            "epic": "E-Commerce Platform",
            "severity": Severity.NORMAL,
            "scenario": "cart_total",
            "data": {"user_id": i % 50 + 1},
            "passes": i not in [125, 139, 147],
            "flake": i == 150,
        })
    
    return tests


def generate_payment_tests():
    """300 тестов: все способы оплаты, транзакции, ошибки"""
    tests = []
    
    # Credit Card (100 tests)
    for i in range(1, 101):
        card_type = random.choice(["visa", "mastercard", "amex", "discover"])
        amount = round(random.uniform(10, 500), 2)
        tests.append({
            "id": f"PAY-{i:03d}",
            "feature": "Payment Processing",
            "story": "Credit Card Payment",
            "title": f"Process {card_type.upper()} payment for ${amount}",
            "epic": "E-Commerce Platform",
            "severity": Severity.CRITICAL,
            "scenario": "card_payment",
            "data": {"card_type": card_type, "amount": amount},
            "passes": i not in [12, 27, 43, 58, 72, 89, 94],
            "flake": i in [98, 100],
        })
    
    # PayPal (50 tests)
    for i in range(101, 151):
        amount = round(random.uniform(10, 500), 2)
        tests.append({
            "id": f"PAY-{i:03d}",
            "feature": "Payment Processing",
            "story": "PayPal Payment",
            "title": f"Process PayPal payment for ${amount}",
            "epic": "E-Commerce Platform",
            "severity": Severity.CRITICAL if i < 120 else Severity.NORMAL,
            "scenario": "paypal_payment",
            "data": {"amount": amount},
            "passes": i not in [108, 125, 139, 147],
            "flake": i == 149,
        })
    
    # Bank Transfer (40 tests)
    for i in range(151, 191):
        amount = round(random.uniform(50, 1000), 2)
        tests.append({
            "id": f"PAY-{i:03d}",
            "feature": "Payment Processing",
            "story": "Bank Transfer",
            "title": f"Process bank transfer for ${amount}",
            "epic": "E-Commerce Platform",
            "severity": Severity.NORMAL,
            "scenario": "bank_transfer",
            "data": {"amount": amount},
            "passes": i not in [155, 172, 185],
            "flake": False,
        })
    
    # Payment History (30 tests)
    for i in range(191, 221):
        user = random.choice(list(USERS.values()))
        tests.append({
            "id": f"PAY-{i:03d}",
            "feature": "Payment Processing",
            "story": "Payment History",
            "title": f"Get payment history for user '{user.email}'",
            "epic": "E-Commerce Platform",
            "severity": Severity.MINOR,
            "scenario": "payment_history",
            "data": {"user_id": user.id},
            "passes": i not in [198, 212, 219],
            "flake": False,
        })
    
    # Refund (30 tests)
    for i in range(221, 251):
        amount = round(random.uniform(10, 200), 2)
        reason = random.choice(["cancelled", "defective", "wrong_item"])
        tests.append({
            "id": f"PAY-{i:03d}",
            "feature": "Payment Processing",
            "story": "Refunds",
            "title": f"Process refund of ${amount} due to {reason}",
            "epic": "E-Commerce Platform",
            "severity": Severity.NORMAL,
            "scenario": "refund",
            "data": {"amount": amount, "reason": reason},
            "passes": i not in [224, 238, 247],
            "flake": False,
        })
    
    # Gift Cards (30 tests)
    for i in range(251, 281):
        amount = round(random.uniform(25, 100), 2)
        tests.append({
            "id": f"PAY-{i:03d}",
            "feature": "Payment Processing",
            "story": "Gift Cards",
            "title": f"Redeem gift card worth ${amount}",
            "epic": "E-Commerce Platform",
            "severity": Severity.MINOR,
            "scenario": "gift_card",
            "data": {"amount": amount},
            "passes": i not in [253, 270, 278],
            "flake": i == 280,
        })
    
    # Payment Declines (20 tests)
    for i in range(281, 301):
        tests.append({
            "id": f"PAY-{i:03d}",
            "feature": "Payment Processing",
            "story": "Payment Declines",
            "title": f"Handle declined payment for {random.choice(['insufficient_funds', 'fraud_risk', 'expired_card', 'limit_exceeded'])}",
            "epic": "E-Commerce Platform",
            "severity": Severity.CRITICAL if i < 290 else Severity.NORMAL,
            "scenario": "decline",
            "data": {},
            "passes": i not in [285, 296],
            "flake": False,
        })
    
    return tests


def generate_order_tests():
    """150 тестов: создание заказа, статусы, история"""
    tests = []
    
    # Order Creation (60 tests)
    for i in range(1, 61):
        items = random.randint(1, 5)
        tests.append({
            "id": f"ORD-{i:03d}",
            "feature": "Order Management",
            "story": "Order Creation",
            "title": f"Create order with {items} item(s)",
            "epic": "E-Commerce Platform",
            "severity": Severity.CRITICAL if i < 20 else Severity.NORMAL,
            "scenario": "create_order",
            "data": {"items": items},
            "passes": i not in [8, 23, 39, 54],
            "flake": i in [57, 60],
        })
    
    # Order Status (40 tests)
    for i in range(61, 101):
        status = random.choice(["pending", "processing", "shipped", "delivered", "cancelled"])
        tests.append({
            "id": f"ORD-{i:03d}",
            "feature": "Order Management",
            "story": "Order Status",
            "title": f"Get order status for {status} order",
            "epic": "E-Commerce Platform",
            "severity": Severity.NORMAL,
            "scenario": "order_status",
            "data": {"status": status},
            "passes": i not in [66, 78, 92],
            "flake": False,
        })
    
    # Order History (30 tests)
    for i in range(101, 131):
        user = random.choice(list(USERS.values()))
        tests.append({
            "id": f"ORD-{i:03d}",
            "feature": "Order Management",
            "story": "Order History",
            "title": f"Get order history for user '{user.email}'",
            "epic": "E-Commerce Platform",
            "severity": Severity.MINOR,
            "scenario": "order_history",
            "data": {"user_id": user.id},
            "passes": i not in [105, 119, 126],
            "flake": False,
        })
    
    # Order Cancellation (20 tests)
    for i in range(131, 151):
        tests.append({
            "id": f"ORD-{i:03d}",
            "feature": "Order Management",
            "story": "Order Cancellation",
            "title": f"Cancel order {i}",
            "epic": "E-Commerce Platform",
            "severity": Severity.NORMAL,
            "scenario": "cancel_order",
            "data": {"order_id": i},
            "passes": i not in [134, 146],
            "flake": False,
        })
    
    return tests


def generate_profile_tests():
    """50 тестов: профиль пользователя, адреса, настройки"""
    tests = []
    
    # Profile (20 tests)
    for i in range(1, 21):
        user = random.choice(list(USERS.values()))
        tests.append({
            "id": f"PROF-{i:03d}",
            "feature": "User Profile",
            "story": "Profile Management",
            "title": f"Get profile for user '{user.email}'",
            "epic": "E-Commerce Platform",
            "severity": Severity.NORMAL,
            "scenario": "get_profile",
            "data": {"user_id": user.id},
            "passes": i not in [7, 14, 18],
            "flake": False,
        })
    
    # Address (15 tests)
    for i in range(21, 36):
        tests.append({
            "id": f"PROF-{i:03d}",
            "feature": "User Profile",
            "story": "Address Management",
            "title": f"Add new shipping address for user",
            "epic": "E-Commerce Platform",
            "severity": Severity.NORMAL,
            "scenario": "add_address",
            "data": {"user_id": i % 20 + 1},
            "passes": i not in [24, 32],
            "flake": False,
        })
    
    # Preferences (15 tests)
    for i in range(36, 51):
        tests.append({
            "id": f"PROF-{i:03d}",
            "feature": "User Profile",
            "story": "User Preferences",
            "title": f"Update user preferences {random.choice(['notifications', 'language', 'currency'])}",
            "epic": "E-Commerce Platform",
            "severity": Severity.MINOR,
            "scenario": "update_preferences",
            "data": {"user_id": i % 20 + 1},
            "passes": i not in [38, 45],
            "flake": False,
        })
    
    return tests


# ============================================================
# 3. ГЕНЕРАЦИЯ ТЕСТОВЫХ ФУНКЦИЙ
# ============================================================

ALL_TESTS = (
    generate_auth_tests() +
    generate_catalog_tests() +
    generate_cart_tests() +
    generate_payment_tests() +
    generate_order_tests() +
    generate_profile_tests()
)

print(f"Total tests generated: {len(ALL_TESTS)}")

# Count failures and flaky for verification
failed_count = sum(1 for t in ALL_TESTS if not t["passes"])
flaky_count = sum(1 for t in ALL_TESTS if t.get("flake", False))
print(f"Expected failures: {failed_count} ({failed_count/len(ALL_TESTS)*100:.1f}%)")
print(f"Flaky tests: {flaky_count} ({flaky_count/len(ALL_TESTS)*100:.1f}%)")


def generate_test_function(test_spec):
    """Создаёт тестовую функцию из спецификации"""
    
    test_id = test_spec["id"]
    title = test_spec["title"]
    feature = test_spec.get("feature", "General")
    story = test_spec.get("story", "General")
    epic = test_spec.get("epic", "E-Commerce Platform")
    severity = test_spec.get("severity", Severity.NORMAL)
    passes = test_spec.get("passes", True)
    flake = test_spec.get("flake", False)
    scenario = test_spec.get("scenario", "general")
    data = test_spec.get("data", {})
    
    def test_func():
        # Allure decorators applied via dynamic API
        allure.dynamic.id(test_id)
        allure.dynamic.title(title)
        allure.dynamic.epic(epic)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)
        allure.dynamic.severity(severity)
        
        # Business logic steps based on scenario
        with allure.step(f"Scenario: {scenario}"):
            with allure.step("Prepare test data"):
                # Log what we're testing
                if "user_id" in data:
                    user = USERS.get(data["user_id"], USERS[1])
                    allure.attach(f"User: {user.email}", "User Info", attachment_type=allure.attachment_type.TEXT)
                if "product_id" in data:
                    product = next((p for p in PRODUCTS if p.id == data["product_id"]), PRODUCTS[0])
                    allure.attach(f"Product: {product.name} (${product.price})", "Product Info", attachment_type=allure.attachment_type.TEXT)
            
            # Execute scenario
            with allure.step(f"Execute {scenario} scenario"):
                # Simulate business operation
                if scenario == "registration":
                    result = {"status": "success", "user_id": 1001}
                elif scenario == "login":
                    result = {"status": "success", "session": f"sess_{random.randint(1000,9999)}"}
                elif scenario == "reset_password":
                    result = {"status": "success"}
                elif scenario in ["search", "filter", "details"]:
                    result = {"items": random.sample(PRODUCTS, min(3, len(PRODUCTS)))}
                elif scenario in ["add_to_cart", "remove_from_cart", "update_cart", "cart_total"]:
                    result = {"total": random.uniform(10, 500)}
                elif scenario in ["card_payment", "paypal_payment", "bank_transfer"]:
                    result = PaymentGateway().charge(data.get("amount", 50), "valid_card")
                elif scenario in ["payment_history", "gift_card"]:
                    result = {"transactions": [{"id": 1, "amount": 50}, {"id": 2, "amount": 75}]}
                elif scenario in ["refund", "decline"]:
                    result = {"status": "processed"}
                elif scenario in ["create_order", "order_status", "order_history", "cancel_order"]:
                    result = {"order_id": random.randint(10000, 99999)}
                elif scenario in ["get_profile", "add_address", "update_preferences"]:
                    result = {"status": "success"}
                else:
                    result = {"status": "success"}
            
            # Validate result
            with allure.step("Validate result"):
                # Fail if test is supposed to fail
                if not passes:
                    if random.random() < 0.3:
                        pytest.fail(f"Deterministic failure in {test_id}: expected condition not met")
                    else:
                        # Some failures happen in different steps for variety
                        failure_step = random.choice(["validation", "business_rule", "integration"])
                        if failure_step == "validation":
                            assert False, f"Validation failed: invalid data in {test_id}"
                        elif failure_step == "business_rule":
                            raise ValueError(f"Business rule violation in {test_id}")
                        else:
                            raise Exception(f"Integration error in {test_id}")
                
                # Flaky tests: sometimes fail
                if flake:
                    # Fail randomly with different probabilities per test
                    fail_chance = random.random()
                    if fail_chance < 0.35:
                        pytest.fail(f"Flaky failure in {test_id} - retry may succeed")
                
                # Check for specific failure conditions based on test_id
                if test_id == "AUTH-018":
                    assert False, "Registration failed: email already exists"
                if test_id == "PAY-072":
                    assert False, "Payment declined: fraud risk detected"
                if test_id == "CART-044":
                    assert False, "Inventory check failed: product out of stock"
                if test_id == "ORD-039":
                    assert False, "Cannot create order with empty cart"
                
                # Default: pass
                assert True, "Test passed successfully"
    
    # Set name for pytest discovery
    test_func.__name__ = f"test_{test_id.lower().replace('-', '_')}_{scenario}"
    
    return test_func


# ============================================================
# 4. СОЗДАНИЕ ТЕСТОВ В ГЛОБАЛЬНОЙ ОБЛАСТИ
# ============================================================

for spec in ALL_TESTS:
    test_func = generate_test_function(spec)
    globals()[test_func.__name__] = test_func


# ============================================================
# 5. ДОПОЛНИТЕЛЬНЫЙ ТЕСТ ДЛЯ ДЕМО СТАТИСТИКИ
# ============================================================

@allure.id("DEMO-001")
@allure.epic("E-Commerce Platform")
@allure.feature("Demo")
@allure.story("Test Statistics")
@allure.title("Verify test suite statistics")
@allure.severity(Severity.NORMAL)
def test_demo_statistics():
    with allure.step("Count total tests"):
        total = len(ALL_TESTS)
    with allure.step("Count passing tests"):
        passed = sum(1 for t in ALL_TESTS if t["passes"])
    with allure.step("Count failing tests"):
        failed = sum(1 for t in ALL_TESTS if not t["passes"])
    with allure.step("Count flaky tests"):
        flaky = sum(1 for t in ALL_TESTS if t.get("flake", False))
    with allure.step("Verify counts"):
        assert total == 1000, f"Expected 1000 tests, got {total}"
        assert failed == 50, f"Expected 50 failing tests, got {failed}"
        assert flaky == 20, f"Expected 20 flaky tests, got {flaky}"
    
    allure.attach(
        f"Total: {total}\nPassing: {passed}\nFailing: {failed}\nFlaky: {flaky}",
        "Statistics",
        allure.attachment_type.TEXT
    )

print("All 1000 tests generated successfully!")
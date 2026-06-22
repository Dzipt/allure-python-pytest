# generate_tests.py
import os
import random

os.makedirs("tests", exist_ok=True)

TEMPLATE = '''# tests/test_{module}.py
import random
import allure
import pytest
from allure_commons.types import Severity

{imports}

@allure.epic("E-Commerce Platform")
@allure.feature("{feature}")
class Test{feature_class}:
    """Tests for {feature}"""
    
{tests}
'''

TEST_TEMPLATE = '''
    @allure.id("{test_id}")
    @allure.story("{story}")
    @allure.title("{title}")
    @allure.severity(Severity.NORMAL)
    def test_{test_id_lower}(self):
        """{title}"""
        with allure.step("Prepare test data"):
            allure.attach("Test ID: {test_id}", "Test Info", allure.attachment_type.TEXT)
        
        with allure.step("Execute business logic"):
            {execution_logic}
        
        with allure.step("Verify result"):
            {assertion}
'''


def generate_auth_tests():
    tests = []
    for i in range(1, 51):
        is_pass = i not in [2, 3, 7, 10, 18, 22, 29, 35, 38, 47]
        is_flake = i in [20, 40]
        
        if i <= 20:
            story = "Registration"
            title = f"User registration with {random.choice(['valid', 'invalid', 'existing'])} credentials"
            logic = f'''result = {{"status": "processing"}}
if random.random() < 0.1:
    pytest.fail("Registration failed: email already exists")'''
        elif i <= 40:
            story = "Login"
            title = f"User login with {random.choice(['correct', 'incorrect', 'locked'])} credentials"
            logic = f'''result = {{"status": "processing"}}
if random.random() < 0.15:
    pytest.fail("Login failed: invalid credentials")'''
        else:
            story = "Password Reset"
            title = f"Password reset for {random.choice(['existing', 'nonexistent'])} user"
            logic = f'''result = {{"status": "processing"}}
if random.random() < 0.1:
    pytest.fail("Password reset failed: user not found")'''
        
        if not is_pass:
            logic = f'pytest.fail("Deterministic failure in AUTH-{i:03d}")'
        elif is_flake:
            logic = f'''if random.random() < 0.4:
    pytest.fail("Flaky failure in AUTH-{i:03d} - retry may succeed")'''
        
        tests.append({
            "id": f"AUTH-{i:03d}",
            "story": story,
            "title": title,
            "logic": logic
        })
    
    return tests


def generate_catalog_tests():
    tests = []
    for i in range(1, 101):
        is_pass = i not in [5, 12, 18, 23, 29, 34, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95]
        is_flake = i in [20, 40, 60, 80]
        
        story = random.choice(["Search", "Filters", "Product Details"])
        title = f"Catalog {story.lower()} with {random.choice(['laptop', 'mouse', 'monitor', 'headphones'])}"
        
        logic = f'''result = {{"status": "success", "items": 5}}
if random.random() < 0.02:
    pytest.fail("Search timeout")'''
        
        if not is_pass:
            logic = f'pytest.fail("Catalog failure in CAT-{i:03d}")'
        elif is_flake:
            logic = f'''if random.random() < 0.35:
    pytest.fail("Flaky catalog failure in CAT-{i:03d}")'''
        
        tests.append({
            "id": f"CAT-{i:03d}",
            "story": story,
            "title": title,
            "logic": logic
        })
    
    return tests


def generate_cart_tests():
    tests = []
    for i in range(1, 151):
        is_pass = i not in [5, 12, 18, 23, 29, 34, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120]
        is_flake = i in [25, 50, 75, 100, 125]
        
        story = random.choice(["Add to Cart", "Remove from Cart", "Update Cart"])
        title = f"Cart {story.lower()} for product {i % 10 + 1}"
        
        logic = f'''product_id = {i % 10 + 1}
if random.random() < 0.01:
    raise ValueError("Product not found")'''
        
        if not is_pass:
            logic = f'pytest.fail("Cart failure in CART-{i:03d}")'
        elif is_flake:
            logic = f'''if random.random() < 0.35:
    pytest.fail("Flaky cart failure in CART-{i:03d}")'''
        
        tests.append({
            "id": f"CART-{i:03d}",
            "story": story,
            "title": title,
            "logic": logic
        })
    
    return tests


def generate_payment_tests():
    tests = []
    for i in range(1, 301):
        is_pass = i not in [
            5, 12, 19, 27, 34, 42, 49, 57, 64, 72, 79, 87, 94, 102, 
            109, 117, 124, 132, 139, 147, 154, 162, 169, 177, 184, 
            192, 199, 207, 214, 222, 229, 237, 244, 252, 259, 267, 
            274, 282, 289, 297
        ]
        is_flake = i in [50, 100, 150, 200, 250]
        
        story = random.choice(["Credit Card", "PayPal", "Bank Transfer", "Refunds"])
        title = f"Payment {story.lower()} for ${round(random.uniform(10, 500), 2)}"
        
        logic = f'''amount = {round(random.uniform(10, 500), 2)}
if random.random() < 0.01:
    raise TimeoutError("Gateway timeout")'''
        
        if not is_pass:
            logic = f'pytest.fail("Payment failure in PAY-{i:03d}")'
        elif is_flake:
            logic = f'''if random.random() < 0.4:
    pytest.fail("Flaky payment failure in PAY-{i:03d}")'''
        
        tests.append({
            "id": f"PAY-{i:03d}",
            "story": story,
            "title": title,
            "logic": logic
        })
    
    return tests


def generate_order_tests():
    tests = []
    for i in range(1, 151):
        is_pass = i not in [
            5, 12, 18, 23, 29, 34, 40, 45, 50, 55, 
            60, 65, 70, 75, 80, 85, 90, 95, 100, 105
        ]
        is_flake = i in [30, 60, 90, 120]
        
        story = random.choice(["Order Creation", "Order Status", "Order History"])
        title = f"Order {story.lower()} for order #{i}"
        
        logic = f'''order_id = {i+1000}
if random.random() < 0.01:
    raise ValueError("Invalid order data")'''
        
        if not is_pass:
            logic = f'pytest.fail("Order failure in ORD-{i:03d}")'
        elif is_flake:
            logic = f'''if random.random() < 0.3:
    pytest.fail("Flaky order failure in ORD-{i:03d}")'''
        
        tests.append({
            "id": f"ORD-{i:03d}",
            "story": story,
            "title": title,
            "logic": logic
        })
    
    return tests


def write_test_file(filename, feature, tests, imports=""):
    tests_text = ""
    for test in tests:
        tests_text += TEST_TEMPLATE.format(
            test_id=test["id"],
            test_id_lower=test["id"].lower().replace("-", "_"),
            story=test["story"],
            title=test["title"],
            execution_logic=test["logic"],
            assertion="assert True" if "pytest.fail" not in test["logic"] else "pass"
        )
    
    feature_class = feature.replace(" ", "")
    
    content = TEMPLATE.format(
        module=filename,
        imports=imports,
        feature=feature,
        feature_class=feature_class,
        tests=tests_text
    )
    
    with open(f"tests/test_{filename}.py", "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ Created test_{filename}.py with {len(tests)} tests")


def main():
    print("🚀 Generating test files...")
    print()
    
    write_test_file("auth", "Authentication", generate_auth_tests())
    write_test_file("catalog", "Catalog", generate_catalog_tests())
    write_test_file("cart", "Shopping Cart", generate_cart_tests())
    write_test_file("payment", "Payment Processing", generate_payment_tests())
    write_test_file("order", "Order Management", generate_order_tests())
    
    print()
    print("✅ All test files created successfully!")
    print()
    print("📊 Summary:")
    print(f"   - test_auth.py: 50 tests")
    print(f"   - test_catalog.py: 100 tests")
    print(f"   - test_cart.py: 150 tests")
    print(f"   - test_payment.py: 300 tests")
    print(f"   - test_order.py: 150 tests")
    print(f"   {'='*30}")
    print(f"   TOTAL: 750 tests")
    print()
    print("📁 Files created in: tests/")


if __name__ == "__main__":
    main()
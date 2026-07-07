import json

import allure
import pytest


DOMAINS = [
    {
        "code": "AUTH",
        "feature": "Authentication",
        "stories": ["Registration", "Login", "Session refresh", "Password reset"],
        "owner": "identity-team",
        "layer": "api",
        "count": 35,
    },
    {
        "code": "CAT",
        "feature": "Catalog",
        "stories": ["Search", "Filters", "Product details", "Recommendations"],
        "owner": "catalog-team",
        "layer": "api",
        "count": 45,
    },
    {
        "code": "CART",
        "feature": "Cart",
        "stories": ["Add item", "Remove item", "Promotions", "Inventory reservation"],
        "owner": "cart-team",
        "layer": "ui",
        "count": 35,
    },
    {
        "code": "CHK",
        "feature": "Checkout",
        "stories": ["Quote calculation", "Payment authorization", "Delivery selection", "Receipt"],
        "owner": "checkout-team",
        "layer": "api",
        "count": 45,
    },
    {
        "code": "ORD",
        "feature": "Orders",
        "stories": ["Order creation", "Order status", "Cancellation", "Refund request"],
        "owner": "orders-team",
        "layer": "api",
        "count": 35,
    },
    {
        "code": "LOY",
        "feature": "Loyalty",
        "stories": ["Points accrual", "Tier benefits", "Coupons", "Personal offers"],
        "owner": "growth-team",
        "layer": "api",
        "count": 25,
    },
    {
        "code": "NTF",
        "feature": "Notifications",
        "stories": ["Email", "Push", "SMS", "Marketing consent"],
        "owner": "communications-team",
        "layer": "mobile",
        "count": 20,
    },
]


def build_case(domain, number, global_number):
    story = domain["stories"][(number - 1) % len(domain["stories"])]
    severity_cycle = [
        allure.severity_level.CRITICAL,
        allure.severity_level.NORMAL,
        allure.severity_level.MINOR,
        allure.severity_level.NORMAL,
    ]
    outcome = "passed"
    if global_number % 53 == 0:
        outcome = "manual"
    elif global_number % 41 == 0:
        outcome = "broken"
    elif global_number % 29 == 0:
        outcome = "flaky"
    elif global_number % 17 == 0:
        outcome = "failed"

    return {
        "id": f"TDS-{domain['code']}-{number:03d}",
        "domain": domain["feature"],
        "story": story,
        "owner": domain["owner"],
        "layer": domain["layer"],
        "severity": severity_cycle[number % len(severity_cycle)],
        "title": f"{domain['feature']}: {story.lower()} scenario #{number:03d}",
        "outcome": outcome,
        "global_number": global_number,
        "risk": "high" if outcome in {"failed", "broken"} else "medium",
    }


def build_cases():
    cases = []
    global_number = 1
    for domain in DOMAINS:
        for number in range(1, domain["count"] + 1):
            cases.append(build_case(domain, number, global_number))
            global_number += 1
    return cases


REGRESSION_CASES = build_cases()


def case_marks(case):
    marks = [pytest.mark.testops_demo]
    marks.append(getattr(pytest.mark, case["layer"]))
    if case["outcome"] == "flaky":
        marks.append(pytest.mark.flaky_demo)
    if case["outcome"] == "manual":
        marks.append(pytest.mark.manual_demo)
    return marks


def case_param(case):
    return pytest.param(case, id=case["id"], marks=case_marks(case))


@pytest.mark.parametrize("case", [case_param(case) for case in REGRESSION_CASES])
def test_business_regression_matrix(case, demo_context):
    allure.dynamic.id(case["id"])
    allure.dynamic.title(case["title"])
    allure.dynamic.epic("QATools Demo Shop")
    allure.dynamic.feature(case["domain"])
    allure.dynamic.story(case["story"])
    allure.dynamic.parent_suite("Generated regression")
    allure.dynamic.suite(case["layer"].upper())
    allure.dynamic.severity(case["severity"])
    allure.dynamic.label("owner", case["owner"])
    allure.dynamic.label("layer", case["layer"])
    allure.dynamic.label("risk", case["risk"])
    allure.dynamic.tag("generated", "regression", case["layer"], case["outcome"])

    if case["outcome"] == "failed":
        allure.dynamic.issue(f"BUG-{case['global_number']:04d}", "Known demo defect")
    if case["outcome"] == "manual":
        allure.dynamic.manual()

    with allure.step("Prepare business scenario"):
        scenario = {
            "caseId": case["id"],
            "feature": case["domain"],
            "story": case["story"],
            "environment": demo_context["environment"],
            "release": demo_context["release"],
            "owner": case["owner"],
            "layer": case["layer"],
        }
        allure.attach(
            json.dumps(scenario, indent=2),
            name="Scenario metadata",
            attachment_type=allure.attachment_type.JSON,
        )

    if case["outcome"] == "manual":
        with allure.step("Route case to manual execution"):
            pytest.skip("Generated manual demo case: execute in TestOps")

    with allure.step("Execute simulated product behavior"):
        actual = {
            "status": "ok",
            "latencyMs": 80 + (case["global_number"] % 90),
            "traceId": f"trace-{case['global_number']:05d}",
        }
        allure.attach(
            json.dumps(actual, indent=2),
            name="Execution result",
            attachment_type=allure.attachment_type.JSON,
        )

        if case["outcome"] == "broken":
            raise RuntimeError(f"Demo integration error in {case['id']}: upstream contract is unavailable")

    with allure.step("Verify business expectation"):
        if case["outcome"] == "failed":
            pytest.fail(f"Demo assertion failure in {case['id']}: expected business rule was not met")
        if case["outcome"] == "flaky" and demo_context["run_variant"] == "1":
            pytest.fail(f"Controlled flaky failure in {case['id']}: retry should pass")
        assert actual["status"] == "ok"

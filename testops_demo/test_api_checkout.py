import json
import time

import allure
import pytest


@pytest.mark.testops_demo
@pytest.mark.api
@allure.epic("QATools Demo Shop")
@allure.feature("Checkout API")
@allure.parent_suite("Automated regression")
@allure.suite("API")
class TestCheckoutApi:
    @allure.label("external_id", "TDS-API-001")
    @allure.title("Checkout quote is created for a loyal customer")
    @allure.story("Quote calculation")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("owner", "qa-platform")
    @allure.tag("smoke", "api", "checkout")
    def test_checkout_quote_created(self, demo_context, demo_user):
        with allure.step("Prepare checkout request"):
            request = {
                "userId": demo_user["id"],
                "items": [
                    {"sku": "QA-BOOK-001", "qty": 1, "price": 3490},
                    {"sku": "QA-HOODIE-007", "qty": 1, "price": 3900},
                ],
                "promoCode": "TESTOPS10",
                "currency": "RUB",
            }
            allure.attach(
                json.dumps(request, indent=2),
                name="Request body",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Calculate quote"):
            response = {
                "status": "created",
                "quoteId": "Q-20260707-001",
                "subtotal": 7390,
                "discount": 739,
                "total": 6651,
                "environment": demo_context["environment"],
            }
            allure.attach(
                json.dumps(response, indent=2),
                name="Response body",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Verify customer discount and final amount"):
            assert response["status"] == "created"
            assert response["discount"] == 739
            assert response["total"] == 6651

    @allure.label("external_id", "TDS-API-002")
    @allure.title("Payment authorization is rejected when fraud score is high")
    @allure.story("Payment authorization")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.label("owner", "payments-team")
    @allure.issue("PAY-1845", "Fraud service returns stale risk score")
    @allure.tag("regression", "payments", "known-defect")
    def test_payment_authorization_rejected_by_fraud_score(self, demo_user):
        with allure.step("Send authorization request"):
            authorization = {
                "userId": demo_user["id"],
                "amount": 6651,
                "cardToken": "tok_demo_visa",
                "fraudScore": 0.91,
            }
            allure.attach(
                json.dumps(authorization, indent=2),
                name="Authorization request",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Verify authorization decision"):
            decision = {"status": "declined", "reason": "fraud_score_too_high"}
            allure.attach(
                json.dumps(decision, indent=2),
                name="Gateway decision",
                attachment_type=allure.attachment_type.JSON,
            )
            assert decision["status"] == "approved", "Payment must be approved for gold customers"

    @allure.label("external_id", "TDS-API-003")
    @allure.title("Delivery partner contract contains required fields")
    @allure.story("Partner integration")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("owner", "integration-team")
    @allure.tag("contract", "delivery")
    @pytest.mark.contract
    def test_delivery_partner_contract(self, demo_context):
        with allure.step("Load partner payload"):
            payload = {
                "orderId": "ORD-20260707-4242",
                "deliveryWindow": "2026-07-08T10:00:00+03:00/2026-07-08T13:00:00+03:00",
                "courier": None,
            }
            allure.attach(
                json.dumps(payload, indent=2),
                name="Partner payload",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Validate contract"):
            if payload["courier"] is None:
                raise RuntimeError(
                    f"Partner payload from {demo_context['environment']} does not contain courier data"
                )

    @allure.label("external_id", "TDS-API-004")
    @allure.title("Catalog search response time stays below SLA")
    @allure.story("Catalog search")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("owner", "catalog-team")
    @allure.tag("performance", "api")
    def test_catalog_search_response_time(self, demo_context):
        with allure.step("Execute search request"):
            started = time.perf_counter()
            time.sleep(0.03)
            elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
            metrics = f"metric,value\nresponse_time_ms,{elapsed_ms}\nsla_ms,250\n"
            allure.attach(metrics, name="SLA metrics", attachment_type=allure.attachment_type.CSV)

        with allure.step("Verify SLA"):
            assert elapsed_ms < 250

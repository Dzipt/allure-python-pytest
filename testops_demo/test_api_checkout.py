import json
import random
import time

import allure
import pytest


@pytest.mark.testops_demo
@pytest.mark.api
@allure.epic("Интернет-магазин QATools")
@allure.feature("Оформление заказа")
@allure.parent_suite("Регрессионная проверка")
@allure.suite("API")
class TestCheckoutApi:
    @allure.label("external_id", "TDS-API-001")
    @allure.title("Расчет итоговой суммы заказа для постоянного покупателя")
    @allure.description("""
    Проверяем, что сервис оформления заказа корректно применяет скидку постоянного покупателя,
    возвращает номер расчета и передает в ответе сумму к оплате в рублях.
    """)
    @allure.story("Расчет итоговой суммы")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("owner", "Платформа качества")
    @allure.label("layer", "api")
    @allure.label("Приоритет", "Критический")
    @allure.tag("дымовой", "api", "оформление")
    def test_checkout_quote_created(self, demo_context, demo_user):
        with allure.step("Подготовить запрос на расчет заказа"):
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
                json.dumps(request, indent=2, ensure_ascii=False),
                name="Тело запроса",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Получить расчет от сервиса оформления"):
            time.sleep(5)
            response = {
                "status": "created",
                "quoteId": "Q-20260707-001",
                "subtotal": 7390,
                "discount": 739,
                "total": 6651,
                "environment": demo_context["environment"],
            }
            allure.attach(
                json.dumps(response, indent=2, ensure_ascii=False),
                name="Ответ сервиса",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Проверить скидку и итоговую сумму"):
            assert response["status"] == "created"
            assert response["discount"] == 739
            assert response["total"] == 6651

    @allure.label("external_id", "TDS-API-002")
    @allure.title("Оплата постоянного покупателя не должна отклоняться из-за устаревшей оценки риска")
    @allure.description("""
    Сценарий демонстрирует дефект: антифрод возвращает устаревшую оценку риска,
    из-за чего платеж надежного покупателя ошибочно отклоняется.
    """)
    @allure.story("Авторизация платежа")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.label("owner", "Платежная команда")
    @allure.label("layer", "api")
    @allure.label("Приоритет", "Критический")
    @allure.issue("PAY-1845", "Антифрод возвращает устаревший риск-профиль")
    @allure.tag("регресс", "платежи", "известный-дефект")
    def test_payment_authorization_rejected_by_fraud_score(self, demo_user):
        with allure.step("Отправить запрос на авторизацию платежа"):
            authorization = {
                "userId": demo_user["id"],
                "amount": 6651,
                "cardToken": "tok_demo_visa",
                "riskScore": 0.91,
            }
            allure.attach(
                json.dumps(authorization, indent=2, ensure_ascii=False),
                name="Запрос авторизации",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Проверить решение платежного шлюза"):
            decision = {"status": "declined", "reason": "fraud_score_too_high"}
            allure.attach(
                json.dumps(decision, indent=2, ensure_ascii=False),
                name="Решение платежного шлюза",
                attachment_type=allure.attachment_type.JSON,
            )
            assert decision["status"] == "approved", "Платеж постоянного покупателя должен быть одобрен"

    @allure.label("external_id", "TDS-API-003")
    @allure.title("Контракт службы доставки содержит обязательные поля курьера")
    @allure.description("""
    Проверяем, что партнер доставки возвращает данные курьера и интервал доставки,
    необходимые для отображения заказа в личном кабинете покупателя.
    """)
    @allure.story("Интеграция со службой доставки")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("owner", "Команда интеграций")
    @allure.label("layer", "api")
    @allure.label("Приоритет", "Высокий")
    @allure.tag("контракт", "доставка")
    def test_delivery_partner_contract(self, demo_context):
        with allure.step("Получить ответ партнера доставки"):
            payload = {
                "orderId": "ORD-20260707-4242",
                "deliveryWindow": "2026-07-08T10:00:00+03:00/2026-07-08T13:00:00+03:00",
                "courier": None,
            }
            allure.attach(
                json.dumps(payload, indent=2, ensure_ascii=False),
                name="Ответ партнера",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Проверить обязательные поля контракта"):
            if payload["courier"] is None:
                raise RuntimeError(
                    f"Ответ партнера на стенде {demo_context['environment']} не содержит данные курьера"
                )

    @allure.label("external_id", "TDS-API-004")
    @allure.title("Поиск по каталогу укладывается в SLA")
    @allure.description("Проверяем, что API поиска возвращает результаты быстрее согласованного порога 250 мс.")
    @allure.story("Поиск товаров")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("owner", "Команда каталога")
    @allure.label("layer", "api")
    @allure.label("Приоритет", "Средний")
    @allure.tag("производительность", "api", "нестабильный")
    @pytest.mark.flaky_demo
    def test_catalog_search_response_time(self):
        with allure.step("Выполнить поисковый запрос"):
            started = time.perf_counter()
            time.sleep(0.03)
            elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
            metrics = f"metric,value\nresponse_time_ms,{elapsed_ms}\nsla_ms,250\n"
            allure.attach(metrics, name="Метрики SLA", attachment_type=allure.attachment_type.CSV)

        with allure.step("Проверить выполнение SLA"):
            assert elapsed_ms < 250

        with allure.step("Проверить результат нестабильного демо-сценария"):
            failure_roll = random.random()
            allure.attach(
                f"{failure_roll:.6f}",
                name="Случайное значение нестабильного сценария",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert failure_roll >= 0.5, (
                f"Имитация нестабильного сбоя с вероятностью 50%: значение {failure_roll:.6f}"
            )

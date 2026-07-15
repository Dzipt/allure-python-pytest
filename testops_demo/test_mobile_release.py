import time

import allure
import pytest


@pytest.mark.testops_demo
@pytest.mark.e2e
@allure.epic("Интернет-магазин QATools")
@allure.feature("Мобильное оформление заказа")
@allure.parent_suite("Релиз-кандидат")
@allure.suite("Мобильное приложение")
@allure.label("layer", "e2e")
class TestMobileRelease:
    @allure.label("external_id", "TDS-MOB-001")
    @allure.title("Мобильное приложение открывает сохраненную корзину из push-уведомления")
    @allure.description("Проверяем диплинк из push-уведомления о брошенной корзине.")
    @allure.story("Push-уведомления")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("owner", "Мобильная команда")
    @allure.label("Приоритет", "Высокий")
    @allure.tag("мобильный", "дымовой", "релиз")
    def test_open_cart_from_push_notification(self, demo_user):
        with allure.step("Получить push-уведомление"):
            time.sleep(5)
            push = {
                "title": "Ваша корзина ждет оформления",
                "deeplink": "qatools-demo://cart",
                "userId": demo_user["id"],
            }
            allure.attach(str(push), name="Payload push-уведомления", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Открыть экран корзины по диплинку"):
            current_screen = "Корзина"
            assert current_screen == "Корзина"

    @allure.label("external_id", "TDS-MOB-002")
    @allure.title("Нестабильный сценарий: подтверждение оплаты биометрией проходит при повторном запуске")
    @allure.description("""
    Демонстрационный нестабильный сценарий: первый запуск имитирует таймаут биометрического датчика,
    повторный запуск проходит успешно.
    """)
    @allure.story("Биометрическое подтверждение")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("owner", "Мобильная команда")
    @allure.label("Приоритет", "Средний")
    @allure.tag("мобильный", "нестабильный")
    def test_biometric_confirmation_flaky_demo(self, demo_context):
        with allure.step("Определить вариант демонстрационного запуска"):
            run_variant = demo_context["run_variant"]
            allure.attach(
                f"TESTOPS_DEMO_RUN={run_variant}",
                name="Переключатель нестабильного сценария",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Подтвердить оплату биометрией"):
            assert run_variant != "1", "Имитация нестабильной ошибки: таймаут биометрического датчика"

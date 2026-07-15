import time

import allure
import pytest


@pytest.mark.testops_demo
@pytest.mark.e2e
@allure.epic("Интернет-магазин QATools")
@allure.feature("Покупательский путь")
@allure.parent_suite("Регрессионная проверка")
@allure.suite("Веб-интерфейс")
@allure.label("layer", "e2e")
class TestCustomerWebJourney:
    @allure.label("external_id", "TDS-UI-001")
    @allure.title("Покупатель видит персонализированную главную страницу после входа")
    @allure.description("""
    Проверяем, что после авторизации покупатель попадает на главную страницу,
    где отображаются его уровень лояльности и персональные предложения.
    """)
    @allure.story("Авторизация")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("owner", "Веб-команда")
    @allure.label("Приоритет", "Высокий")
    @allure.tag("дымовой", "веб", "нестабильный")
    @pytest.mark.flaky_demo
    def test_customer_lands_on_personalized_page(self, demo_user, flaky_demo_check):
        with allure.step("Открыть страницу входа и авторизоваться"):
            time.sleep(5)
            page_state = {
                "url": "/login",
                "user": demo_user["email"],
                "result": "Пользователь авторизован",
            }
            allure.attach(str(page_state), name="Состояние браузера", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверить персонализацию главной страницы"):
            header = "Анна, ваш уровень лояльности: Золотой"
            assert "Золотой" in header

        flaky_demo_check("Персонализированная главная страница")

    @allure.label("external_id", "TDS-UI-002")
    @allure.title("Фильтрация результатов поиска по бренду QATools и цене")
    @allure.story("Поиск и фильтры")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("owner", "Веб-команда")
    @allure.label("Приоритет", "Средний")
    @allure.tag("регресс", "веб", "поиск")
    def test_search_filters_qatools_brand(self):
        self.check_search_filters("QATools", 5000, 4)

    @allure.label("external_id", "TDS-UI-003")
    @allure.title("Фильтрация результатов поиска по бренду Allure и цене")
    @allure.story("Поиск и фильтры")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("owner", "Веб-команда")
    @allure.label("Приоритет", "Средний")
    @allure.tag("регресс", "веб", "поиск")
    def test_search_filters_allure_brand(self):
        self.check_search_filters("Allure", 8000, 7)

    @allure.label("external_id", "TDS-UI-004")
    @allure.title("Фильтрация результатов поиска по бренду TestOps и цене")
    @allure.story("Поиск и фильтры")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("owner", "Веб-команда")
    @allure.label("Приоритет", "Низкий")
    @allure.tag("регресс", "веб", "поиск")
    def test_search_filters_testops_brand(self):
        self.check_search_filters("TestOps", 10000, 3)

    def check_search_filters(self, brand, max_price, expected_count):
        allure.dynamic.parameter("brand", brand)
        allure.dynamic.parameter("max_price", max_price)

        with allure.step("Применить фильтры каталога"):
            filtered_count = expected_count
            allure.attach(
                f"brand={brand}\nmax_price={max_price}\ncount={filtered_count}",
                name="Результат фильтрации",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Проверить, что найден хотя бы один товар"):
            assert filtered_count > 0

    @allure.label("external_id", "TDS-UI-005")
    @allure.title("Ручная проверка карточки товара на десктопе и смартфоне")
    @allure.manual(True)
    @allure.story("Визуальное качество")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("owner", "Дизайн QA")
    @allure.label("Приоритет", "Низкий")
    @allure.tag("ручной", "визуальный", "веб")
    @allure.description(
        """
        Ручная визуальная проверка карточки товара на основных разрешениях.
        Кейс нужен для демонстрации ручных проверок в TestOps и контроля верстки
        перед релизом витрины.
        """
    )
    @pytest.mark.skip(reason="Ручной сценарий TestOps: выполнить в исследовательской сессии")
    def test_product_card_visual_layout_manual(self):
        pass

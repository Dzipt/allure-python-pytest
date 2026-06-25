import allure
import pytest
import random

BROWSERS = ["chromium", "firefox", "webkit"]
VIEWPORTS = [
    ("desktop_hd", 1920, 1080),
    ("desktop", 1440, 900),
    ("laptop", 1280, 800),
    ("tablet", 768, 1024),
    ("mobile", 375, 812),
]
LOCALES = ["ru-RU", "en-US", "de-DE", "zh-CN"]
FORM_VALIDATIONS = [
    ("empty_email", "", "password123", "Email обязателен"),
    ("invalid_email", "notanemail", "password123", "Неверный формат email"),
    ("empty_password", "user@fin.app", "", "Пароль обязателен"),
    ("short_password", "user@fin.app", "123", "Пароль слишком короткий"),
]


@allure.epic("FinApp")
@allure.feature("Веб-приложение")
@allure.label("layer", "ui_tests")
@allure.label("Platform", "Web")
@allure.label("Team", "Web")
class TestWebAuth:

    @allure.id("web_001")
    @allure.title("Страница входа загружается и содержит форму авторизации")
    @allure.story("Авторизация в браузере")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("smoke", "web", "auth")
    @allure.label("jira", "FIN-501")
    def test_login_page_loads_with_form(self):
        with allure.step("Открыть https://app.finapp.demo/login"):
            url = "https://app.finapp.demo/login"
        with allure.step("Страница загружена с кодом 200"):
            status = 200
            assert status == 200
        with allure.step("Форма авторизации отображается"):
            form_elements = ["input[name='email']", "input[name='password']", "button[type='submit']"]
            assert len(form_elements) == 3

    @allure.id("web_002")
    @allure.title("Успешная авторизация перенаправляет на дашборд")
    @allure.story("Авторизация в браузере")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("smoke", "web", "auth")
    @allure.label("jira", "FIN-502")
    def test_successful_login_redirects_to_dashboard(self):
        with allure.step("Ввести корректный email и пароль"):
            credentials = {"email": "user@fin.app", "password": "SecurePass123!"}
        with allure.step("Нажать кнопку Войти"):
            pass
        with allure.step("Произошёл редирект на /dashboard"):
            current_url = "https://app.finapp.demo/dashboard"
            assert "/dashboard" in current_url

    @allure.id("web_003")
    @allure.title("Валидация формы показывает корректные ошибки")
    @allure.story("Валидация формы входа")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("regression", "web", "auth", "validation")
    @pytest.mark.parametrize("scenario,email,password,expected_error", FORM_VALIDATIONS)
    def test_form_validation_errors(self, scenario, email, password, expected_error):
        with allure.step(f"Сценарий: {scenario}"):
            with allure.step(f"Ввести email='{email}', password='{password}'"):
                pass
            with allure.step("Нажать Войти"):
                error_message = expected_error
            with allure.step(f"Отображается ошибка: '{expected_error}'"):
                assert error_message == expected_error

    @allure.id("web_004")
    @allure.title("Веб-приложение работает в разных браузерах")
    @allure.story("Кросс-браузерность")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("regression", "web", "cross-browser")
    @pytest.mark.parametrize("browser", BROWSERS)
    def test_app_works_in_browser(self, browser):
        with allure.step(f"Открыть приложение в {browser}"):
            result = {"browser": browser, "loaded": True, "js_errors": 0}
        with allure.step("Приложение загружено без JS-ошибок"):
            assert result["loaded"] is True
            assert result["js_errors"] == 0

    @allure.id("web_005")
    @allure.title("Адаптивная вёрстка корректна на всех разрешениях")
    @allure.story("Адаптивный дизайн")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("regression", "web", "responsive")
    @pytest.mark.parametrize("name,width,height", VIEWPORTS)
    def test_responsive_layout(self, name, width, height):
        with allure.step(f"Установить viewport {width}x{height} ({name})"):
            pass
        with allure.step("Проверить что элементы не выходят за границы"):
            result = {"viewport": name, "overflow_x": False, "elements_clipped": False}
        with allure.step("Вёрстка корректна"):
            assert result["overflow_x"] is False
            assert result["elements_clipped"] is False


@allure.epic("FinApp")
@allure.feature("Веб-приложение")
@allure.label("layer", "ui_tests")
@allure.label("Platform", "Web")
@allure.label("Team", "Web")
class TestWebTransfer:

    @allure.id("web_010")
    @allure.title("Форма перевода отображает актуальный баланс")
    @allure.story("Переводы через веб")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "web", "transfer")
    @allure.label("jira", "FIN-510")
    def test_transfer_form_shows_current_balance(self):
        with allure.step("Открыть страницу перевода"):
            balance = 150000.00
        with allure.step("Баланс отображается в форме"):
            displayed = {"balance": balance, "currency": "₽"}
            assert displayed["balance"] == balance

    @allure.id("web_011")
    @allure.title("Перевод через веб-форму проходит успешно")
    @allure.story("Переводы через веб")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("smoke", "web", "transfer")
    @allure.label("jira", "FIN-511")
    def test_web_transfer_success(self):
        with allure.step("Ввести получателя и сумму перевода 3000 руб."):
            form = {"recipient": "+7 900 123-45-67", "amount": 3000}
        with allure.step("Подтвердить перевод"):
            result = {"status": "success", "transaction_id": "TXN-WEB-001"}
        with allure.step("Перевод выполнен"):
            assert result["status"] == "success"

    @allure.id("web_012")
    @allure.title("Локализация интерфейса работает для всех поддерживаемых языков")
    @allure.story("Локализация")
    @allure.severity(allure.severity_level.MINOR)
    @allure.tag("regression", "web", "i18n")
    @pytest.mark.parametrize("locale", LOCALES)
    def test_ui_localization(self, locale):
        with allure.step(f"Установить язык интерфейса: {locale}"):
            response = {"locale": locale, "translations_loaded": True}
        with allure.step("Переводы загружены"):
            assert response["translations_loaded"] is True


@allure.epic("FinApp")
@allure.feature("Веб-приложение")
@allure.label("layer", "ui_tests")
@allure.label("Platform", "Web")
@allure.label("Team", "Web")
class TestWebFlaky:

    @allure.id("web_flaky_001")
    @allure.title("Страница дашборда загружается за < 2 сек (нестабильно)")
    @allure.story("Производительность")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("regression", "web", "performance", "flaky")
    def test_dashboard_page_load_time(self):
        with allure.step("Открыть страницу дашборда"):
            load_ms = random.choice([850, 920, 1100, 2300, 780, 1950, 890])
        with allure.step(f"Время загрузки: {load_ms}ms (лимит: 1500ms)"):
            assert load_ms < 1500, f"Медленная загрузка дашборда: {load_ms}ms"

    @allure.id("web_flaky_002")
    @allure.title("WebSocket соединение для котировок устанавливается (нестабильно)")
    @allure.story("Котировки в реальном времени")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("regression", "web", "websocket", "flaky")
    def test_websocket_connection_established(self):
        with allure.step("Инициировать WebSocket соединение"):
            connected = random.choice([True, True, True, False, True, False, True])
        with allure.step("Соединение установлено"):
            assert connected, "WebSocket не подключился (нестабильность сети)"

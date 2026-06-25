import allure
import pytest
import random

IOS_DEVICES = ["iPhone 15 Pro", "iPhone 14", "iPhone 13 mini", "iPhone SE 3"]
IOS_VERSIONS = ["17.4", "16.7", "15.8"]
BIOMETRIC_RESULTS = ["success", "success", "success", "not_enrolled", "lockout"]


@allure.epic("FinApp")
@allure.feature("iOS-приложение")
@allure.label("layer", "ui_tests")
@allure.label("Platform", "iOS")
@allure.label("Team", "iOS")
class TestiOSAuth:

    @allure.id("ios_001")
    @allure.title("Экран входа отображается корректно при запуске")
    @allure.story("Авторизация на iOS")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("smoke", "ios", "auth")
    @allure.label("jira", "FIN-301")
    def test_login_screen_displayed_on_launch(self):
        with allure.step("Запустить приложение"):
            app_state = "foreground"
        with allure.step("Проверить что экран логина отображается"):
            screen = {"name": "LoginScreen", "visible": True}
            assert screen["visible"] is True
        with allure.step("Проверить наличие полей email и пароль"):
            elements = ["email_field", "password_field", "login_button"]
            for el in elements:
                assert el in elements

    @allure.id("ios_002")
    @allure.title("Face ID авторизация выполняется успешно")
    @allure.story("Биометрическая авторизация")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "ios", "biometric")
    @allure.label("jira", "FIN-302")
    def test_face_id_auth_success(self):
        with allure.step("Открыть приложение с настроенным Face ID"):
            pass
        with allure.step("Инициировать Face ID авторизацию"):
            biometric_result = "success"
        with allure.step("Пользователь авторизован"):
            assert biometric_result == "success"
        with allure.step("Открыт главный экран"):
            screen = {"name": "DashboardScreen", "visible": True}
            assert screen["visible"] is True

    @allure.id("ios_003")
    @allure.title("Push-уведомление о переводе отображается корректно")
    @allure.story("Push-уведомления")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("regression", "ios", "notifications")
    @allure.label("jira", "FIN-303")
    def test_push_notification_transfer_displayed(self):
        with allure.step("Выполнить входящий перевод на счёт пользователя"):
            transfer = {"amount": 5000, "sender": "Мария С."}
        with allure.step("Проверить появление push-уведомления"):
            notification = {
                "title": "Входящий перевод",
                "body": f"Получено {transfer['amount']} руб. от {transfer['sender']}",
                "received": True
            }
        with allure.step("Уведомление содержит сумму и отправителя"):
            assert str(transfer["amount"]) in notification["body"]
            assert transfer["sender"] in notification["body"]

    @allure.id("ios_004")
    @allure.title("Приложение работает корректно на разных устройствах iOS")
    @allure.story("Совместимость устройств")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("regression", "ios", "compatibility")
    @pytest.mark.parametrize("device", IOS_DEVICES)
    def test_app_launches_on_device(self, device):
        with allure.step(f"Запустить приложение на {device}"):
            result = {"device": device, "launched": True, "crash": False}
        with allure.step("Приложение запущено без краша"):
            assert result["launched"] is True
            assert result["crash"] is False

    @allure.id("ios_005")
    @allure.title("Приложение работает на поддерживаемых версиях iOS")
    @allure.story("Совместимость ОС")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("regression", "ios", "compatibility")
    @pytest.mark.parametrize("ios_version", IOS_VERSIONS)
    def test_app_compatible_with_ios_version(self, ios_version):
        with allure.step(f"Запустить приложение на iOS {ios_version}"):
            result = {"ios_version": ios_version, "compatible": True}
        with allure.step("Приложение совместимо с версией iOS"):
            assert result["compatible"] is True

    @allure.id("ios_006")
    @allure.title("Deep link на экран перевода открывается корректно")
    @allure.story("Deep links")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("regression", "ios", "deeplink")
    @allure.label("jira", "FIN-304")
    def test_deep_link_transfer_screen(self):
        with allure.step("Открыть deep link finapp://transfer?to=USR-002&amount=1000"):
            deep_link = "finapp://transfer?to=USR-002&amount=1000"
        with allure.step("Открылся экран перевода с предзаполненными данными"):
            screen = {"name": "TransferScreen", "prefilled_amount": 1000, "prefilled_recipient": "USR-002"}
        with allure.step("Сумма предзаполнена"):
            assert screen["prefilled_amount"] == 1000


@allure.epic("FinApp")
@allure.feature("iOS-приложение")
@allure.label("layer", "ui_tests")
@allure.label("Platform", "iOS")
@allure.label("Team", "iOS")
class TestiOSFlaky:

    @allure.id("ios_flaky_001")
    @allure.title("Анимация экрана загрузки завершается до 3 секунд (нестабильно)")
    @allure.story("Производительность")
    @allure.severity(allure.severity_level.MINOR)
    @allure.tag("regression", "ios", "performance", "flaky")
    def test_splash_screen_animation_duration(self):
        with allure.step("Запустить приложение"):
            pass
        with allure.step("Измерить длительность анимации загрузки"):
            duration_ms = random.choice([800, 950, 1100, 3200, 750, 2900, 880])
        with allure.step(f"Анимация: {duration_ms}ms (лимит: 2000ms)"):
            assert duration_ms < 2000, f"Медленная анимация загрузки: {duration_ms}ms"

    @allure.id("ios_flaky_002")
    @allure.title("Биометрия срабатывает с первой попытки (нестабильно)")
    @allure.story("Биометрическая авторизация")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("regression", "ios", "biometric", "flaky")
    def test_biometric_first_attempt_success(self):
        with allure.step("Инициировать биометрическую авторизацию"):
            result = random.choice(BIOMETRIC_RESULTS)
        with allure.step(f"Результат первой попытки: {result}"):
            assert result == "success", f"Биометрия: '{result}' вместо 'success'"

import allure
import pytest
import random

ANDROID_DEVICES = ["Samsung Galaxy S24", "Pixel 8 Pro", "Xiaomi 14", "OnePlus 12", "OPPO Find X7"]
ANDROID_VERSIONS = ["14", "13", "12", "11"]
SCREEN_SIZES = ["360x800", "390x844", "412x915", "480x1040"]


@allure.epic("FinApp")
@allure.feature("Android-приложение")
@allure.label("layer", "ui_tests")
@allure.label("Platform", "Android")
@allure.label("Team", "Android")
class TestAndroidAuth:

    @allure.title("Экран входа отображается корректно при первом запуске")
    @allure.story("Авторизация на Android")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("smoke", "android", "auth")
    @allure.label("jira", "FIN-401")
    def test_login_screen_on_first_launch(self):
        with allure.step("Запустить приложение на Android"):
            pass
        with allure.step("Проверить отображение экрана логина"):
            screen = {"name": "LoginActivity", "visible": True}
            assert screen["visible"] is True
        with allure.step("Проверить наличие UI-элементов"):
            elements = ["et_email", "et_password", "btn_login", "tv_forgot_password"]
            assert len(elements) == 4

    @allure.title("Fingerprint-аутентификация выполняется успешно")
    @allure.story("Биометрическая авторизация")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "android", "biometric")
    @allure.label("jira", "FIN-402")
    def test_fingerprint_auth_success(self):
        with allure.step("Открыть приложение с настроенным Fingerprint"):
            pass
        with allure.step("Приложить палец к сенсору"):
            biometric_result = "authenticated"
        with allure.step("Пользователь авторизован"):
            assert biometric_result == "authenticated"
        with allure.step("Открыт главный экран"):
            activity = {"name": "MainActivity", "visible": True}
            assert activity["visible"] is True

    @allure.title("Приложение работает на разных устройствах Android")
    @allure.story("Совместимость устройств")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("regression", "android", "compatibility")
    @pytest.mark.parametrize("device", ANDROID_DEVICES)
    def test_app_launches_on_android_device(self, device):
        with allure.step(f"Запустить приложение на {device}"):
            result = {"device": device, "launched": True, "anr": False, "crash": False}
        with allure.step("Приложение запущено без ANR и краша"):
            assert result["launched"] is True
            assert result["anr"] is False
            assert result["crash"] is False

    @allure.title("Приложение поддерживает все целевые версии Android")
    @allure.story("Совместимость ОС")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("regression", "android", "compatibility")
    @pytest.mark.parametrize("version", ANDROID_VERSIONS)
    def test_app_compatible_with_android_version(self, version):
        with allure.step(f"Запустить приложение на Android {version}"):
            result = {"android_version": version, "compatible": True}
        with allure.step("Приложение совместимо"):
            assert result["compatible"] is True

    @allure.title("Адаптивная вёрстка корректна на разных разрешениях")
    @allure.story("Адаптивность")
    @allure.severity(allure.severity_level.MINOR)
    @allure.tag("regression", "android", "ui")
    @pytest.mark.parametrize("resolution", SCREEN_SIZES)
    def test_layout_adapts_to_screen_size(self, resolution):
        with allure.step(f"Проверить вёрстку на разрешении {resolution}"):
            result = {"resolution": resolution, "overflow": False, "clipped": False}
        with allure.step("Элементы не выходят за границы экрана"):
            assert result["overflow"] is False
            assert result["clipped"] is False

    @allure.title("Deep link на экран перевода открыается корректно")
    @allure.story("Deep links")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("regression", "android", "deeplink")
    @allure.label("jira", "FIN-403")
    def test_deep_link_opens_transfer_screen(self):
        with allure.step("Открыть deep link finapp://transfer"):
            pass
        with allure.step("Открылся экран перевода"):
            activity = {"name": "TransferActivity", "visible": True}
            assert activity["visible"] is True

    @allure.title("Push-уведомление о переводе открывает нужный экран")
    @allure.story("Push-уведомления")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("regression", "android", "notifications")
    @allure.label("jira", "FIN-404")
    def test_push_notification_opens_transaction_detail(self):
        with allure.step("Получить push-уведомление о входящем переводе"):
            notification = {"title": "Входящий перевод", "transaction_id": "TXN-999"}
        with allure.step("Нажать на уведомление"):
            pass
        with allure.step("Открылся экран деталей транзакции"):
            activity = {"name": "TransactionDetailActivity", "transaction_id": "TXN-999"}
            assert activity["transaction_id"] == notification["transaction_id"]


@allure.epic("FinApp")
@allure.feature("Android-приложение")
@allure.label("layer", "ui_tests")
@allure.label("Platform", "Android")
@allure.label("Team", "Android")
class TestAndroidFlaky:

    @allure.title("Время запуска приложения до первого экрана < 2 сек (нестабильно)")
    @allure.story("Производительность")
    @allure.severity(allure.severity_level.MINOR)
    @allure.tag("regression", "android", "performance", "flaky")
    def test_app_cold_start_time(self):
        with allure.step("Запустить приложение с холодного старта"):
            launch_ms = random.choice([850, 920, 780, 2100, 1050, 2400, 890])
        with allure.step(f"Время запуска: {launch_ms}ms (лимит: 1500ms)"):
            assert launch_ms < 1500, f"Медленный холодный старт: {launch_ms}ms"

    @allure.title("Синхронизация баланса после перевода < 3 сек (нестабильно)")
    @allure.story("Синхронизация данных")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("regression", "android", "sync", "flaky")
    def test_balance_sync_after_transfer(self):
        with allure.step("Выполнить перевод"):
            pass
        with allure.step("Ожидать обновления баланса в приложении"):
            sync_ms = random.choice([400, 550, 380, 3200, 490, 2800, 420])
        with allure.step(f"Синхронизация: {sync_ms}ms (лимит: 2000ms)"):
            assert sync_ms < 2000, f"Медленная синхронизация: {sync_ms}ms"

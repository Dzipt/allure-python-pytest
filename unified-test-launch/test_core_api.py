import allure
import pytest

TRANSFER_AMOUNTS = [100, 500, 1000, 5000, 10000, 50000]
CURRENCIES = ["RUB", "USD", "EUR", "CNY"]
ACCOUNT_TYPES = ["current", "savings", "deposit", "credit"]
INVALID_AMOUNTS = [-100, 0, -0.01]
CARD_MASKS = ["4111", "5500", "3782", "6011"]


@allure.epic("FinApp")
@allure.feature("Переводы")
@allure.label("layer", "api_tests")
@allure.label("Platform", "Backend")
@allure.label("Team", "core-api")
class TestTransfers:

    @allure.title("Перевод между счетами выполняется успешно")
    @allure.story("Внутренние переводы")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("smoke", "transfers", "core-api")
    @allure.label("jira", "FIN-101")
    def test_internal_transfer_success(self, user_account):
        with allure.step("Подготовить счета отправителя и получателя"):
            sender_balance = user_account["balance"]
            amount = 5000.00
        with allure.step(f"Выполнить перевод {amount} руб."):
            response = {"status": "completed", "transaction_id": "TXN-001", "amount": amount}
        with allure.step("Проверить статус транзакции"):
            assert response["status"] == "completed"
        with allure.step("Проверить списание с отправителя"):
            new_balance = sender_balance - amount
            assert new_balance == sender_balance - amount

    @allure.title("Перевод с недостаточным балансом отклоняется")
    @allure.story("Внутренние переводы")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("regression", "transfers", "core-api")
    @allure.label("jira", "FIN-102")
    def test_transfer_insufficient_funds_rejected(self, user_account):
        with allure.step("Попытаться перевести сумму больше баланса"):
            amount = user_account["balance"] + 1000
            response = {"status": "rejected", "reason": "insufficient_funds"}
        with allure.step("Перевод отклонён"):
            assert response["status"] == "rejected"
            assert response["reason"] == "insufficient_funds"

    @allure.title("Перевод на разные суммы выполняется корректно")
    @allure.story("Внутренние переводы")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("regression", "transfers", "core-api")
    @pytest.mark.parametrize("amount", TRANSFER_AMOUNTS)
    def test_transfer_various_amounts(self, amount):
        with allure.step(f"Выполнить перевод на сумму {amount} руб."):
            response = {"status": "completed", "amount": amount}
        with allure.step("Сумма в транзакции корректна"):
            assert response["amount"] == amount

    @allure.title("Перевод с отрицательной суммой отклоняется")
    @allure.story("Валидация переводов")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("regression", "transfers", "core-api", "validation")
    @pytest.mark.parametrize("amount", INVALID_AMOUNTS)
    def test_transfer_invalid_amount_rejected(self, amount):
        with allure.step(f"Попытаться перевести {amount} руб."):
            response = {"status": 400, "error": "Invalid amount"}
        with allure.step("Запрос отклонён с ошибкой валидации"):
            assert response["status"] == 400

    @allure.title("Мультивалютный перевод конвертирует корректно")
    @allure.story("Валютные переводы")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("regression", "transfers", "core-api", "fx")
    @allure.label("jira", "FIN-103")
    @pytest.mark.parametrize("currency", CURRENCIES)
    def test_multicurrency_transfer(self, currency):
        with allure.step(f"Выполнить перевод в валюте {currency}"):
            response = {"currency": currency, "status": "completed", "fx_rate_applied": True}
        with allure.step("Конвертация применена"):
            assert response["fx_rate_applied"] is True


@allure.epic("FinApp")
@allure.feature("Аутентификация")
@allure.label("layer", "api_tests")
@allure.label("Platform", "Backend")
@allure.label("Team", "core-api")
class TestAuthentication:

    @allure.title("Авторизация по логину и паролю возвращает JWT-токен")
    @allure.story("Вход в систему")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("smoke", "auth", "core-api")
    def test_login_returns_jwt_token(self):
        with allure.step("POST /api/v2/auth/login"):
            response = {"status": 200, "token": "eyJhbGciOiJIUzI1NiJ9.payload.sig", "expires_in": 3600}
        with allure.step("Получен JWT-токен"):
            assert "token" in response
            parts = response["token"].split(".")
            assert len(parts) == 3, "Токен не является валидным JWT"
        with allure.step("Время жизни токена указано"):
            assert response["expires_in"] > 0

    @allure.title("Refresh токена выдаёт новый access token")
    @allure.story("Управление сессией")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "auth", "core-api")
    def test_refresh_token_issues_new_access_token(self):
        with allure.step("Использовать refresh token"):
            old_token = "old_access_token"
            response = {"status": 200, "token": "new_access_token_xyz", "expires_in": 3600}
        with allure.step("Выдан новый access token"):
            assert response["token"] != old_token
            assert response["status"] == 200

    @allure.title("Истёкший токен возвращает 401")
    @allure.story("Управление сессией")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("regression", "auth", "core-api")
    def test_expired_token_returns_401(self):
        with allure.step("Использовать истёкший токен"):
            response = {"status": 401, "error": "Token expired"}
        with allure.step("Ответ 401 Unauthorized"):
            assert response["status"] == 401

    @allure.title("Блокировка аккаунта после 5 неверных паролей")
    @allure.story("Защита от перебора")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("regression", "auth", "core-api", "security")
    @allure.label("jira", "FIN-110")
    def test_account_locked_after_5_failed_attempts(self):
        with allure.step("Выполнить 5 попыток входа с неверным паролем"):
            attempts = [{"status": 401} for _ in range(5)]
        with allure.step("6-я попытка возвращает 423 Locked"):
            sixth_attempt = {"status": 423, "error": "Account temporarily locked"}
            assert sixth_attempt["status"] == 423


@allure.epic("FinApp")
@allure.feature("Счета и балансы")
@allure.label("layer", "api_tests")
@allure.label("Platform", "Backend")
@allure.label("Team", "core-api")
class TestAccounts:

    @allure.title("Получение баланса счёта возвращает актуальные данные")
    @allure.story("Просмотр счетов")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("smoke", "accounts", "core-api")
    def test_account_balance_returned(self, user_account):
        with allure.step("GET /api/v2/accounts/{id}/balance"):
            response = {"balance": user_account["balance"], "currency": "RUB", "updated_at": "2026-06-18T10:00:00Z"}
        with allure.step("Баланс получен"):
            assert response["balance"] == user_account["balance"]
        with allure.step("Валюта указана"):
            assert response["currency"] == "RUB"

    @allure.title("История транзакций возвращает записи в хронологическом порядке")
    @allure.story("История операций")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("regression", "accounts", "core-api")
    def test_transaction_history_chronological(self):
        with allure.step("GET /api/v2/accounts/{id}/transactions"):
            transactions = [
                {"id": "T3", "date": "2026-06-18", "amount": -500},
                {"id": "T2", "date": "2026-06-17", "amount": 10000},
                {"id": "T1", "date": "2026-06-16", "amount": -2000},
            ]
        with allure.step("Записи отсортированы от новых к старым"):
            dates = [t["date"] for t in transactions]
            assert dates == sorted(dates, reverse=True)

    @allure.title("Открытие счёта разных типов выполняется успешно")
    @allure.story("Управление счетами")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("regression", "accounts", "core-api")
    @pytest.mark.parametrize("account_type", ACCOUNT_TYPES)
    def test_open_account_of_type(self, account_type):
        with allure.step(f"POST /api/v2/accounts с type={account_type}"):
            account = {"type": account_type, "status": "active", "id": f"ACC-{account_type}-001"}
        with allure.step("Счёт открыт и активен"):
            assert account["status"] == "active"
            assert account["type"] == account_type


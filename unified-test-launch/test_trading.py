import allure
import pytest
import random

INSTRUMENTS = ["SBER", "GAZP", "YNDX", "LKOH", "MGNT", "ROSN", "NVTK", "GMKN"]
ORDER_TYPES = ["market", "limit", "stop", "stop_limit"]
ORDER_SIDES = ["buy", "sell"]
QUANTITIES = [1, 5, 10, 50, 100]
TIMEFRAMES = ["1m", "5m", "15m", "1h", "4h", "1d"]


@allure.epic("FinApp")
@allure.feature("Торговля ценными бумагами")
@allure.label("layer", "api_tests")
@allure.label("Platform", "Backend")
@allure.label("Team", "trading")
class TestOrders:

    @allure.id("trd_001")
    @allure.title("Рыночная заявка на покупку исполняется немедленно")
    @allure.story("Выставление заявок")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("smoke", "trading", "orders")
    @allure.label("jira", "FIN-201")
    def test_market_buy_order_executed(self, trading_account):
        with allure.step("Выставить рыночную заявку на покупку SBER"):
            order = {"type": "market", "side": "buy", "instrument": "SBER", "qty": 10}
        with allure.step("Заявка исполнена"):
            result = {"status": "filled", "filled_qty": 10, "avg_price": 305.50}
            assert result["status"] == "filled"
        with allure.step("Количество исполнено полностью"):
            assert result["filled_qty"] == order["qty"]

    @allure.id("trd_002")
    @allure.title("Лимитная заявка выставляется и ожидает исполнения")
    @allure.story("Выставление заявок")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "trading", "orders")
    @allure.label("jira", "FIN-202")
    def test_limit_order_placed_pending(self):
        with allure.step("Выставить лимитную заявку на покупку GAZP по 180.00"):
            order = {"type": "limit", "side": "buy", "instrument": "GAZP", "qty": 5, "price": 180.00}
        with allure.step("Заявка принята и ожидает исполнения"):
            result = {"status": "pending", "order_id": "ORD-TRD-001"}
            assert result["status"] == "pending"
        with allure.step("Order ID присвоен"):
            assert result["order_id"].startswith("ORD-")

    @allure.id("trd_003")
    @allure.title("Заявка на разные инструменты принимается")
    @allure.story("Выставление заявок")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("regression", "trading", "orders")
    @pytest.mark.parametrize("instrument", INSTRUMENTS)
    def test_order_accepted_for_instrument(self, instrument):
        with allure.step(f"Выставить заявку на {instrument}"):
            response = {"instrument": instrument, "status": "accepted"}
        with allure.step("Заявка принята"):
            assert response["status"] == "accepted"

    @allure.id("trd_004")
    @allure.title("Все типы заявок принимаются системой")
    @allure.story("Типы заявок")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("regression", "trading", "orders")
    @pytest.mark.parametrize("order_type", ORDER_TYPES)
    def test_all_order_types_accepted(self, order_type):
        with allure.step(f"Выставить заявку типа {order_type}"):
            response = {"type": order_type, "status": "accepted"}
        with allure.step("Тип заявки поддерживается"):
            assert response["status"] == "accepted"

    @allure.id("trd_005")
    @allure.title("Отмена активной заявки выполняется успешно")
    @allure.story("Управление заявками")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("regression", "trading", "orders")
    @allure.label("jira", "FIN-203")
    def test_cancel_active_order_success(self):
        with allure.step("Выставить лимитную заявку"):
            order_id = "ORD-TRD-999"
        with allure.step(f"Отменить заявку {order_id}"):
            result = {"order_id": order_id, "status": "cancelled"}
        with allure.step("Заявка отменена"):
            assert result["status"] == "cancelled"


@allure.epic("FinApp")
@allure.feature("Торговля ценными бумагами")
@allure.label("layer", "api_tests")
@allure.label("Platform", "Backend")
@allure.label("Team", "trading")
class TestPortfolio:

    @allure.id("trd_010")
    @allure.title("Стоимость портфеля рассчитывается корректно")
    @allure.story("Портфель")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "trading", "portfolio")
    def test_portfolio_value_calculated(self, trading_account):
        with allure.step("Получить стоимость портфеля"):
            response = {"portfolio_value": trading_account["portfolio_value"], "currency": "RUB"}
        with allure.step("Стоимость рассчитана и положительна"):
            assert response["portfolio_value"] > 0

    @allure.id("trd_011")
    @allure.title("Доходность позиции рассчитывается с учётом комиссий")
    @allure.story("Аналитика портфеля")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("regression", "trading", "portfolio")
    def test_position_pnl_includes_commission(self):
        with allure.step("Рассчитать P&L позиции"):
            buy_price = 300.00
            current_price = 315.00
            commission = 0.3
            gross_pnl = (current_price - buy_price) * 10
            net_pnl = gross_pnl - commission
        with allure.step("Чистый P&L меньше валового на размер комиссии"):
            assert net_pnl == gross_pnl - commission

    @allure.id("trd_012")
    @allure.title("Исторические котировки возвращаются для всех таймфреймов")
    @allure.story("Котировки и графики")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("regression", "trading", "quotes")
    @pytest.mark.parametrize("timeframe", TIMEFRAMES)
    def test_historical_quotes_for_timeframe(self, timeframe):
        with allure.step(f"GET /api/v2/instruments/SBER/candles?tf={timeframe}"):
            candles = [{"open": 300, "high": 310, "low": 298, "close": 305, "volume": 10000} for _ in range(5)]
        with allure.step("Свечи получены"):
            assert len(candles) > 0
        with allure.step("Структура свечи корректна"):
            assert all(c["high"] >= c["low"] for c in candles)


@allure.epic("FinApp")
@allure.feature("Торговля ценными бумагами")
@allure.label("layer", "api_tests")
@allure.label("Platform", "Backend")
@allure.label("Team", "trading")
class TestTradingFlaky:
    """
    Нестабильные тесты — зависят от рыночных данных в реальном времени.
    Имитируют флаки при интеграции с биржей.
    """

    @allure.id("trd_flaky_001")
    @allure.title("Котировки обновляются в течение 1 секунды (нестабильно)")
    @allure.story("Котировки и графики")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("regression", "trading", "quotes", "flaky")
    def test_quote_update_latency(self):
        with allure.step("Подписаться на котировки SBER"):
            pass
        with allure.step("Получить обновление котировки"):
            latency_ms = random.choice([85, 120, 95, 1200, 78, 950, 102])
        with allure.step(f"Задержка обновления: {latency_ms}ms (лимит: 500ms)"):
            assert latency_ms < 500, f"Задержка биржи: {latency_ms}ms"

    @allure.id("trd_flaky_002")
    @allure.title("Рыночная заявка исполняется в течение 200ms (нестабильно)")
    @allure.story("Выставление заявок")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("regression", "trading", "orders", "flaky")
    def test_market_order_execution_time(self):
        with allure.step("Выставить рыночную заявку"):
            pass
        with allure.step("Измерить время исполнения"):
            exec_ms = random.choice([45, 62, 38, 350, 71, 420, 55, 88])
        with allure.step(f"Время исполнения: {exec_ms}ms (лимит: 200ms)"):
            assert exec_ms < 200, f"Медленное исполнение: {exec_ms}ms"

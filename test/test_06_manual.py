import allure
import pytest

@allure.title("Визуальная проверка главной страницы")
@allure.description("""
## Ручной тест-кейс

Этот тест выполняется вручную. Результат проставляется исполнителем в ТестОпс.

### Предусловие
Открыт браузер, пользователь не авторизован.
""")
@allure.feature("UI")
@allure.story("Главная страница")
@allure.severity(allure.severity_level.NORMAL)
@allure.label("layer", "ui_tests")
@allure.tag("manual", "visual")
@pytest.mark.skip(reason="Manual test — execute by hand")
def test_main_page_visual():
    """
    Шаги:
    1. Открыть https://example.com
    2. Проверить что логотип отображается корректно
    3. Проверить что меню навигации содержит все пункты
    4. Проверить что баннер загружается без артефактов
    5. Проверить адаптивность на ширине 375px

    Ожидаемый результат:
    Все визуальные элементы отображаются корректно.
    """
    pass
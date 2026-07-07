import allure
import pytest


@pytest.mark.testops_demo
@pytest.mark.ui
@allure.epic("QATools Demo Shop")
@allure.feature("Customer web journey")
@allure.parent_suite("Automated regression")
@allure.suite("Web UI")
class TestCustomerWebJourney:
    @allure.id("TDS-UI-001")
    @allure.title("Guest sees personalized landing page after sign in")
    @allure.story("Authentication")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("owner", "web-team")
    @allure.tag("smoke", "ui")
    def test_customer_lands_on_personalized_page(self, demo_user):
        with allure.step("Open sign-in page and submit credentials"):
            page_state = {
                "url": "/login",
                "user": demo_user["email"],
                "result": "authenticated",
            }
            allure.attach(str(page_state), name="Browser state", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Verify personalized landing page"):
            header = "Welcome back, gold customer"
            assert "gold customer" in header

    @allure.id("TDS-UI-002")
    @allure.title("Search results can be filtered by brand and price")
    @allure.story("Product discovery")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("owner", "web-team")
    @allure.tag("regression", "ui", "search")
    @pytest.mark.parametrize(
        ("brand", "max_price", "expected_count"),
        [
            ("QATools", 5000, 4),
            ("Allure", 8000, 7),
            ("TestOps", 10000, 3),
        ],
    )
    def test_search_filters(self, brand, max_price, expected_count):
        allure.dynamic.parameter("brand", brand)
        allure.dynamic.parameter("max_price", max_price)

        with allure.step("Apply catalog filters"):
            filtered_count = expected_count
            allure.attach(
                f"brand={brand}\nmax_price={max_price}\ncount={filtered_count}",
                name="Filter result",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Verify filtered result count"):
            assert filtered_count > 0

    @allure.id("TDS-UI-003")
    @allure.title("Manual check: product card visual layout on desktop and mobile")
    @allure.manual(True)
    @allure.story("Visual quality")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("owner", "design-qa")
    @allure.tag("manual", "visual", "ui")
    @allure.description(
        """
        Preconditions:
        1. Open the staging storefront.
        2. Use a customer account with gold loyalty tier.

        Steps:
        1. Open a product card from search results.
        2. Check product image, price, delivery date, favorite button, and add-to-cart button.
        3. Repeat the check on 1440px, 768px, and 390px viewport widths.

        Expected result:
        Product card is readable, no controls overlap, and the add-to-cart action is visible.
        """
    )
    @pytest.mark.skip(reason="Manual TestOps case: execute during exploratory session")
    def test_product_card_visual_layout_manual(self):
        pass

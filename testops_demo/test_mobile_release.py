import allure
import pytest


@pytest.mark.testops_demo
@pytest.mark.mobile
@allure.epic("QATools Demo Shop")
@allure.feature("Mobile checkout")
@allure.parent_suite("Release candidate")
@allure.suite("Mobile")
class TestMobileRelease:
    @allure.id("TDS-MOB-001")
    @allure.title("Mobile app opens saved cart from push notification")
    @allure.story("Push notifications")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("owner", "mobile-team")
    @allure.tag("mobile", "smoke", "release")
    def test_open_cart_from_push_notification(self, demo_user):
        with allure.step("Receive push notification"):
            push = {
                "title": "Your cart is waiting",
                "deeplink": "qatools-demo://cart",
                "userId": demo_user["id"],
            }
            allure.attach(str(push), name="Push payload", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Open cart screen"):
            current_screen = "Cart"
            assert current_screen == "Cart"

    @allure.id("TDS-MOB-002")
    @allure.title("Flaky demo: biometric confirmation succeeds on repeat run")
    @allure.story("Biometric confirmation")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("owner", "mobile-team")
    @allure.tag("mobile", "flaky-demo")
    def test_biometric_confirmation_flaky_demo(self, demo_context):
        with allure.step("Read simulated launch variant"):
            run_variant = demo_context["run_variant"]
            allure.attach(
                f"TESTOPS_DEMO_RUN={run_variant}",
                name="Flaky demo switch",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Confirm payment by biometrics"):
            assert run_variant != "1", "Simulated flaky failure: biometric sensor timeout"

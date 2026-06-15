import random

import allure
import pytest
from allure_commons.types import Severity


def unstable_api_response() -> None:
    if random.random() < 0.5:
        pytest.fail("Flaky response: intermittent timeout or inconsistent payload")


@pytest.mark.parametrize("value", list(range(1, 1000)))
def test_stable_pass(value):
    assert value * 2 == value + value


@allure.title("Broken test: internal system error")
@allure.severity(Severity.CRITICAL)
def test_broken_internal_error():
    raise RuntimeError("Broken: internal system error occurred")


@allure.title("Broken test: type conversion failure")
@allure.severity(Severity.CRITICAL)
def test_broken_type_error():
    raise TypeError("Broken: invalid type conversion in test")


@allure.title("Failed test: validation mismatch")
@allure.severity(Severity.NORMAL)
def test_failed_validation_mismatch():
    pytest.fail("Failed: validation mismatch detected")


@allure.title("Failed test: expected result not matched")
@allure.severity(Severity.NORMAL)
def test_failed_expected_result():
    pytest.fail("Failed: expected result does not match actual output")


@allure.title("Failed test: permission denied")
@allure.severity(Severity.NORMAL)
def test_failed_permission_denied():
    pytest.fail("Failed: permission denied for action")


@allure.title("Flaky test: intermittent API response")
@allure.severity(Severity.MINOR)
def test_flaky_intermittent_api_response():
    unstable_api_response()

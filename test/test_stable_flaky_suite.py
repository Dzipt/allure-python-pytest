import random

import allure
import pytest
from allure_commons.types import Severity


def _create_stable_pass_test(value: int):
    def test_func():
        allure.dynamic.id(f"stable_pass_{value}")
        allure.dynamic.title(f"Stable passing test {value}")
        with allure.step("Prepare test data"):
            test_input = value
        with allure.step("Compute expected output"):
            expected = test_input + test_input
        with allure.step("Validate result"):
            assert expected == test_input * 2

    test_func.__name__ = f"test_stable_pass_{value}"
    return test_func


def _create_failure_test(value: int):
    def test_func():
        allure.dynamic.id(f"failed_{value}")
        allure.dynamic.title(f"Deterministic failing test {value}")
        with allure.step("Prepare failure condition"):
            reason = f"Failed deterministic test number {value}"
        with allure.step("Trigger failure"):
            pytest.fail(reason)

    test_func.__name__ = f"test_failed_{value}"
    return test_func


def _create_flaky_test(value: int):
    def test_func():
        allure.dynamic.id(f"flaky_{value}")
        allure.dynamic.title(f"Flaky test {value}")
        with allure.step("Run unstable check"):
            if random.random() < 0.5:
                pytest.fail(f"Flaky failure in test {value}")
        with allure.step("Confirm stability"):
            assert value > 0

    test_func.__name__ = f"test_flaky_{value}"
    return test_func


for value in range(1, 1001):
    globals()[f"test_stable_pass_{value}"] = _create_stable_pass_test(value)

for value in range(1, 41):
    globals()[f"test_failed_{value}"] = _create_failure_test(value)

for value in range(1, 11):
    globals()[f"test_flaky_{value}"] = _create_flaky_test(value)

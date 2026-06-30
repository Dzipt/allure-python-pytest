import pytest
import random

@pytest.fixture(autouse=True)
def reset_random():
    """Фикстура для консистентных флаки тестов"""
    random.seed(42)
    yield
"""conftest.py"""
import pytest
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.webdriver import LocalWebDriver


def pytest_addoption(parser):
    # Добавляем выбор браузера
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Браузер для тестов: chrome, firefox, edge"
    )
    # Добавляем базовый URL
    parser.addoption(
        "--url",
        action="store",
        default="http://localhost:8080/",
        help="Базовый URL PrestaShop"
    )


@pytest.fixture(scope="session")
def base_url(request):
    """Фикстура возвращает базовый URL без лишних слэшей на конце."""
    return request.config.getoption("--url").rstrip("/")


@pytest.fixture(scope="function")
def driver(request):
    browser_name = request.config.getoption("--browser").lower()

    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless") # Раскомментировать для CI
        driver = webdriver.Chrome(options=options)
    elif browser_name == "firefox":
        options = webdriver.FirefoxOptions()
        driver = webdriver.Firefox(options=options)
    elif browser_name == "edge":
        options = webdriver.EdgeOptions()
        driver = webdriver.Edge(options=options)
    else:
        raise Exception(f"Браузер {browser_name} не поддерживается")

    yield driver

    driver.quit()

"""conftest.py"""
import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from src.logger_config import setup_logger

setup_logger()


def pytest_addoption(parser):
    """Выбор браузера, по умолчанию хром"""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Браузер для тестов: chrome, firefox"
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


@pytest.fixture
def driver(request):
    """Создаёт выбранный браузер в headless-режиме для Docker."""
    browser_name = request.config.getoption("--browser").lower()

    if browser_name == "chrome":
        options = ChromeOptions()
        # НАСТРОЙКИ ДЛЯ DOCKER (Обязательны для Linux без графической оболочки)
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1280,900")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--lang=ru-RU")

        browser = webdriver.Chrome(options=options)

    elif browser_name == "firefox":
        options = FirefoxOptions()
        # НАСТРОЙКИ ДЛЯ DOCKER (Обязательны для Linux без графической оболочки)
        options.add_argument("--headless")

        browser = webdriver.Firefox(options=options)
    else:
        raise Exception(f"Браузер {browser_name} не поддерживается")

    yield browser
    browser.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """делает скриншоты при падении тестов"""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        try:
            if "driver" in item.fixturenames:
                web_driver = item.funcargs["driver"]
                allure.attach(
                    web_driver.get_screenshot_as_png(),
                    name="Скриншот при падении",
                    attachment_type=allure.attachment_type.PNG
                )
        except Exception as e:
            print(f"Не удалось сделать скриншот: {e}")

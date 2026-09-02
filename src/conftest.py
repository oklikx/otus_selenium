"""conftest.py"""
import allure
import pytest
import os
from selenium.webdriver.chrome.options import Options
from src.logger_config import setup_logger

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.webdriver import LocalWebDriver

setup_logger()

# def pytest_addoption(parser):
#     # Добавляем выбор браузера
#     parser.addoption(
#         "--browser",
#         action="store",
#         default="chrome",
#         help="Браузер для тестов: chrome, firefox, edge"
#     )
#     # Добавляем базовый URL
#     parser.addoption(
#         "--url",
#         action="store",
#         default="http://localhost:8080/",
#         help="Базовый URL PrestaShop"
#     )


# @pytest.fixture(scope="session")
# def base_url(request):
#     """Фикстура возвращает базовый URL без лишних слэшей на конце."""
#     return request.config.getoption("--url").rstrip("/")


# @pytest.fixture(scope="function")
# def driver(request):ы
#     browser_name = request.config.getoption("--browser").lower()

#     if browser_name == "chrome":
#         options = webdriver.ChromeOptions()
#         # options.add_argument("--headless") # Раскомментировать для CI
#         driver = webdriver.Chrome(options=options)
#     elif browser_name == "firefox":
#         options = webdriver.FirefoxOptions()
#         driver = webdriver.Firefox(options=options)
#     elif browser_name == "edge":
#         options = webdriver.EdgeOptions()
#         driver = webdriver.Edge(options=options)
#     else:
#         raise Exception(f"Браузер {browser_name} не поддерживается")

#     yield driver

#     driver.quit()


# """
# Инфраструктура запуска браузера (не PageObject).

# POM описывает страницы и компоненты UI.
# Создание драйвера — отдельная ответственность: фикстура pytest.
# """

@pytest.fixture
def driver():
    """
    Создаёт Chrome на время одного теста и закрывает его после.

    Как применяется:
    - pytest сам передаёт `driver` в тест как аргумент;
    - код после `yield` выполняется всегда (даже если тест упал).

    Сюда кладём только настройки браузера, не локаторы и не шаги сценария.
    """
    options = Options()
    # options.add_argument("--headless=new")  # без окна браузера
    options.add_argument("--window-size=1280,900")
    # чуть меньше шансов, что сайт поймёт автоматизацию
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--lang=ru-RU")

    browser = webdriver.Chrome(options=options)
    yield browser
    browser.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    # Если тест выполнялся и упал (FAILED)
    if rep.when == "call" and rep.failed:
        try:
            # Ищем фикстуру 'driver' в упавшем тесте
            if "driver" in item.fixturenames:
                web_driver = item.funcargs["driver"]

                # Делаем скриншот и прикрепляем его в Allure
                allure.attach(
                    web_driver.get_screenshot_as_png(),
                    name="Скриншот при падении",
                    attachment_type=allure.attachment_type.PNG
                )
        except Exception as e:
            print(f"Не удалось сделать скриншот: {e}")

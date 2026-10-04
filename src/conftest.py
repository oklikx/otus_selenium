"""conftest.py"""
import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from src.logger_config import setup_logger

setup_logger()


def pytest_addoption(parser):
    """Опции командной строки для выбора браузера и способа запуска."""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Браузер для тестов: chrome, firefox",
    )
    parser.addoption(
        "--url",
        action="store",
        default="http://localhost:8080/",
        help="Базовый URL PrestaShop",
    )
    parser.addoption(
        "--browser_version",
        action="store",
        default="128.0",
        help="Версия браузера для Selenoid (например, 128.0)",
    )
    parser.addoption(
        "--executor",
        action="store",
        default="local",
        choices=["local", "selenoid"],
        help="Где запускать тесты: local (локальный драйвер) или selenoid",
    )
    parser.addoption(
        "--selenoid_url",
        action="store",
        default="http://localhost:4444/wd/hub",
        help="URL Selenoid (wd/hub). Из контейнера: http://selenoid:4444/wd/hub",
    )


@pytest.fixture(scope="session")
def base_url(request):
    """Возвращает базовый URL без лишних слэшей на конце."""
    return request.config.getoption("--url").rstrip("/")


def _build_options(browser_name: str, executor: str):
    """Создаёт Options для выбранного браузера с учётом executor."""
    if browser_name == "chrome":
        options = ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1280,900")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--lang=ru-RU")
        # headless нужен только для локального запуска в Docker/Linux
        if executor == "local":
            options.add_argument("--headless=new")
        return options

    if browser_name == "firefox":
        options = FirefoxOptions()
        options.add_argument("--width=1280")
        options.add_argument("--height=900")
        if executor == "local":
            options.add_argument("--headless")
        return options

    raise Exception(f"Браузер {browser_name} не поддерживается")


@pytest.fixture
def driver(request):
    """Создаёт браузер локально или на Selenoid."""
    browser_name = request.config.getoption("--browser").lower()
    browser_version = request.config.getoption("--browser_version")
    executor = request.config.getoption("--executor")
    selenoid_url = request.config.getoption("--selenoid_url")

    options = _build_options(browser_name, executor)

    if executor == "local":
        # Локальный запуск: Selenium Manager сам подберёт драйвер
        if browser_name == "chrome":
            browser = webdriver.Chrome(options=options)
        else:
            browser = webdriver.Firefox(options=options)

    elif executor == "selenoid":
        # Удалённый запуск через Selenoid
        options.set_capability("browserName", browser_name)
        options.set_capability("browserVersion", browser_version)
        options.set_capability(
            "selenoid:options",
            {
                "enableVNC": True,
                "enableVideo": False,
                "name": request.node.name,
            },
        )
        browser = webdriver.Remote(
            command_executor=selenoid_url,
            options=options,
        )

    else:
        raise Exception(f"Executor {executor} не поддерживается")

    yield browser
    browser.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Делает скриншоты при падении тестов."""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        try:
            if "driver" in item.fixturenames:
                web_driver = item.funcargs["driver"]
                allure.attach(
                    web_driver.get_screenshot_as_png(),
                    name="Скриншот при падении",
                    attachment_type=allure.attachment_type.PNG,
                )
        except Exception as e:
            print(f"Не удалось сделать скриншот: {e}")
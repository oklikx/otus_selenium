"""conftest.py"""
import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from src.logger_config import setup_logger

setup_logger()


def pytest_addoption(parser):
    """Опции, которые можно передавать из Jenkins."""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Браузер для тестов: chrome, firefox"
    )
    parser.addoption(
        "--browser-version",
        action="store",
        default="128.0",
        help="Версия браузера, например 128.0"
    )
    parser.addoption(
        "--selenoid-url",
        action="store",
        default="http://localhost:4444/wd/hub",
        help="Адрес Selenoid (executor)"
    )
    parser.addoption(
        "--url",
        action="store",
        default="http://localhost:8080/",
        help="Базовый URL PrestaShop"
    )


@pytest.fixture(scope="session")
def base_url(request):
    """Базовый URL без лишних слэшей на конце."""
    return request.config.getoption("--url").rstrip("/")


@pytest.fixture(scope="session")
def selenoid_url(request):
    return request.config.getoption("--selenoid-url")


@pytest.fixture(scope="session")
def browser_name(request):
    return request.config.getoption("--browser").lower()


@pytest.fixture(scope="session")
def browser_version(request):
    return request.config.getoption("--browser-version")


@pytest.fixture
def driver(request, selenoid_url, browser_name, browser_version):
    """Создаёт Remote WebDriver в Selenoid."""
    test_name = request.node.name

    if browser_name == "chrome":
        options = ChromeOptions()
    elif browser_name == "firefox":
        options = FirefoxOptions()
    else:
        raise Exception(f"Браузер {browser_name} не поддерживается")

    options.set_capability("browserName", browser_name)
    options.set_capability("browserVersion", browser_version)
    options.set_capability("selenoid:options", {
        "enableVNC": True,
        "enableVideo": False,
        "name": test_name,
    })

    browser = webdriver.Remote(
        command_executor=selenoid_url,
        options=options,
    )

    browser.set_page_load_timeout(30)
    browser.implicitly_wait(0)

    yield browser

    try:
        browser.quit()
    except Exception as e:
        print(f"Не удалось корректно закрыть браузер: {e}")


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
                    attachment_type=allure.attachment_type.PNG
                )
        except Exception as e:
            print(f"Не удалось сделать скриншот: {e}")

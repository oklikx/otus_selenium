"""Базовый класс для всех Page"""
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait


class BasePage():
    """Базовый класс для всех Page"""

    def __init__(self, driver: WebDriver, base_url: str, timeout=15):
        self.driver = driver
        self.base_url = base_url
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
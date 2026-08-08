"""Общие компоненты шапки сайта"""
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from src.pom.locators.presta_shop_header_locators import HeaderLocators


class Header():
    """Общие компоненты"""

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def get_user_menu(self):
        """Польовательское меню"""
        return WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(HeaderLocators.USER_MENU)
        )

    def get_my_profile_link(self):
        """Ссылка на профиль пользователя"""
        return self.driver.find_element(*HeaderLocators.MY_PROFILE)

    def get_currency_select_options(self):
        """Опции валюты(массив из двух опций)"""
        currency_select = self.driver.find_element(
            *HeaderLocators.CURRENCY_SELECT)
        currency_options = currency_select.find_elements(
            *HeaderLocators.CURRENCY_OPTIONS)

        return currency_options

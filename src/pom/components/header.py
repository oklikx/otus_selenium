"""Общие компоненты шапки сайта"""
import logging
import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from src.pom.locators.presta_shop_header_locators import HeaderLocators

logger = logging.getLogger('AutomationFramework.HeaderComponent')


class Header():
    """Общие компоненты"""

    def __init__(self, driver: WebDriver):
        self.driver = driver

    @allure.step
    def get_user_menu(self):
        """Пользовательское меню"""
        logger.info("Получили элемент пользовательского меню")
        return WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(HeaderLocators.USER_MENU)
        )

    @allure.step
    def get_my_profile_link(self):
        """Ссылка на профиль пользователя"""

        logger.info("Получили ссылку на профиль пользователя")
        return self.driver.find_element(*HeaderLocators.MY_PROFILE)

    @allure.step
    def get_currency_select_options(self):
        """Опции валюты(массив из двух опций)"""
        currency_select = self.driver.find_element(
            *HeaderLocators.CURRENCY_SELECT)
        currency_options = currency_select.find_elements(
            *HeaderLocators.CURRENCY_OPTIONS)

        logger.info("Получили массив опций валют")
        return currency_options

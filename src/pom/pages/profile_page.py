"""Страница профиля"""
import logging
import allure
from src.pom.pages.base_page import BasePage
from src.pom.locators.presta_shop_profile_locators import ProfilePageLocators
from src.helpers.make_js_click import make_js_click


logger = logging.getLogger("AutomationFramework.ProfilePage")


class ProfilePage(BasePage):
    """Страница профиля"""

    @allure.step
    def get_page_title(self):
        """Получить элемент заголовка страницы"""
        logger.info("Получили элемент заголовка страницы")
        return self.driver.find_element(*ProfilePageLocators.PAGE_TITLE)

    @allure.step
    def click_signout_link(self):
        """Нажать на кнопку разлогина"""
        signout_link = self.driver.find_element(
            *ProfilePageLocators.SIGNOUT_LINK)

        logger.info("Нажали на кнопку разлогина")
        make_js_click(self.driver, signout_link)

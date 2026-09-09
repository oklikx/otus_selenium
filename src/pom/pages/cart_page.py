"""Страница корзины"""
import logging
import allure
from selenium.webdriver.support import expected_conditions as EC
from src.pom.pages.base_page import BasePage
from src.pom.locators.presta_shop_cart_locators import CartPageLocators
from src.data.urls import CART_PAGE_URL
from src.helpers.make_js_click import make_js_click

logger = logging.getLogger("AutomationFramework.CartPage")


class CartPage(BasePage):
    """Страница корзины"""

    @allure.step
    def open(self):
        """Открыть страницу корзины"""
        logger.info("Открываем страницу корзины - %s", CART_PAGE_URL)
        self.driver.get(CART_PAGE_URL)

    @allure.step
    def get_page_title(self):
        """Получение заголовка страницы корзины"""
        logger.info("Получили текст заголовка страницы")
        return self.wait.until(
            EC.presence_of_element_located(CartPageLocators.PAGE_TITLE)).text

    @allure.step
    def get_link_to_product(self):
        """Получить элемент ссылки на добавленный товар"""
        logger.info("Получили элемент ссылки на добавленный товар")
        link = self.wait.until(EC.presence_of_element_located(
            CartPageLocators.LINK_TO_PRODUCT))

        return link

    @allure.step
    def delete_product(self):
        """Удалить из корзины 1 товар"""
        logger.info("Удалили из корзины 1 товар")
        product = self.wait.until(
            EC.presence_of_element_located(CartPageLocators.PRODUCT))

        make_js_click(self.driver, product.find_element(
            *CartPageLocators.REMOVE_PRODUCT_BUTTON))

        self.wait.until(EC.staleness_of(product))

    @allure.step
    def get_update_alert(self):
        """Получить элемент плашки о том, что товар успешно удалён"""
        logger.info("Получили элемент плашки о том, что товар успешно удалён")
        return self.wait.until(
            EC.presence_of_element_located(CartPageLocators.UPDATE_ALERT)
        )

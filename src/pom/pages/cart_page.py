"""Страница корзины"""
from selenium.webdriver.support import expected_conditions as EC
from src.pom.pages.base_page import BasePage
from src.pom.locators.presta_shop_cart_locators import CartPageLocators
from src.data.urls import CART_PAGE_URL
from src.helpers.make_js_click import make_js_click


class CartPage(BasePage):
    """Страница корзины"""

    def open(self):
        """Открыть страницу корзины"""
        self.driver.get(CART_PAGE_URL)

    def get_page_title(self):
        """Получить текст заголовка страницы"""
        return self.wait.until(
            EC.presence_of_element_located(CartPageLocators.PAGE_TITLE)).text

    def get_link_to_product(self):
        """Получить элемент ссылки на добавленный товар"""
        return self.driver.find_element(*CartPageLocators.LINK_TO_PRODUCT)

    def delete_product(self):
        """Удалить из корзины 1 товар"""
        product = self.wait.until(
            EC.presence_of_element_located(CartPageLocators.PRODUCT))

        make_js_click(self.driver, product.find_element(
            *CartPageLocators.REMOVE_PRODUCT_BUTTON))

        self.wait.until(EC.staleness_of(product))

    def get_update_alert(self):
        """Получить элемент плашки о том, что товар успешно удалён"""
        return self.wait.until(
            EC.presence_of_element_located(CartPageLocators.UPDATE_ALERT)
        )

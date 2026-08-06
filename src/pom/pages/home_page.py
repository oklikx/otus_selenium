"""Главная страница"""
from selenium.webdriver.support import expected_conditions as EC
from src.pom.pages.base_page import BasePage
from src.data.urls import BASE_URL
from src.pom.locators.presta_shop_home_locators import PrestaShopHomeLocators
from src.helpers.make_js_click import make_js_click

import random


class HomePage(BasePage):
    """Главная страница"""

    def open(self):
        """Открыть главную страницу"""
        self.driver.get(BASE_URL)

    def add_random_product_to_cart(self):
        """Добавить случайный товар в корзину и получить ссылку на ожидаемый товар"""
        products = self.driver.find_elements(
            *PrestaShopHomeLocators.PRODUCTS
        )

        random_product = random.choice(products)
        random_product_link = random_product.find_element(
            *PrestaShopHomeLocators.RANDOM_PRODUCT_LINK)
        random_product_cart_button = random_product.find_element(
            *PrestaShopHomeLocators.RANDOM_PRODUCT_CART_BUTTON)

        # нужно сохранить href в переменную, пока не поменялась страница
        # иначе элемент устареет, его нельзя будет использовать с assert
        expected_url = random_product_link.get_attribute('href')

        make_js_click(self.driver, random_product_cart_button)

        return expected_url

    def open_cart_modal_and_go_to_cart(self):
        """Открыть модалку добавления товара и перейти в корзину"""
        self.wait.until(EC.presence_of_element_located(
            PrestaShopHomeLocators.CART_MODAL))

        proceed_to_checkout_link = self.driver.find_element(
            *PrestaShopHomeLocators.CHECKOUT_LINK)
        make_js_click(self.driver, proceed_to_checkout_link)

    def get_first_product(self):
        """Получить элемент первого товара"""
        return self.wait.until(EC.presence_of_element_located(
            PrestaShopHomeLocators.FIRST_PRODUCT))

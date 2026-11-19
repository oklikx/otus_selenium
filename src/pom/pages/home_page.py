"""Главная страница"""
import random
import logging
import allure
from selenium.webdriver.support import expected_conditions as EC
from src.pom.pages.base_page import BasePage
from src.pom.locators.presta_shop_home_locators import PrestaShopHomeLocators
from src.helpers.make_js_click import make_js_click


logger = logging.getLogger("AutomationFramework.HomePage")


class HomePage(BasePage):
    """Главная страница"""

    @allure.step
    def open(self, base_url):
        logger.info("Открываем главную страницу - %s", base_url)
        self.driver.get(base_url)

    @allure.step
    def add_random_product_to_cart(self):
        """Добавить случайный товар в корзину и получить ссылку на ожидаемый товар"""
        self.wait.until(EC.presence_of_all_elements_located(
            PrestaShopHomeLocators.PRODUCTS
        ))
        all_products = self.driver.find_elements(
            *PrestaShopHomeLocators.PRODUCTS)

        # Оставляем только товары, у которых есть кнопка "Add to cart"
        products_with_button = []
        for product in all_products:
            buttons = product.find_elements(
                *PrestaShopHomeLocators.RANDOM_PRODUCT_CART_BUTTON
            )
            if buttons:
                products_with_button.append((product, buttons[0]))

        if not products_with_button:
            raise AssertionError(
                f"На главной странице нет товаров с кнопкой Add to cart. "
                f"Всего товаров: {len(all_products)}. URL: {self.driver.current_url}"
            )

        random_product, random_product_cart_button = random.choice(
            products_with_button)
        random_product_link = random_product.find_element(
            *PrestaShopHomeLocators.RANDOM_PRODUCT_LINK)

        expected_url = random_product_link.get_attribute('href')

        logger.info("Добавили случайный товар в корзину")
        make_js_click(self.driver, random_product_cart_button)

        logger.info("Получили ссылку на ожидаемый товар")
        return expected_url

    @allure.step
    def open_cart_modal_and_go_to_cart(self):
        """Открыть модалку добавления товара и перейти в корзину"""
        self.wait.until(EC.presence_of_element_located(
            PrestaShopHomeLocators.CART_MODAL))

        logger.info("Открыли модальное окно добавления в товара")

        proceed_to_checkout_link = self.driver.find_element(
            *PrestaShopHomeLocators.CHECKOUT_LINK)
        make_js_click(self.driver, proceed_to_checkout_link)

        logger.info("Перешли в корзину")

    @allure.step
    def get_first_product(self):
        """Получить элемент первого товара"""
        logger.info("Получаем элемент первого товара")
        return self.wait.until(EC.presence_of_element_located(
            PrestaShopHomeLocators.FIRST_PRODUCT))

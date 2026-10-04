"""Локаторы главной страницы"""
from selenium.webdriver.common.by import By


class PrestaShopHomeLocators:
    """Локаторы главной страницы"""

    PRODUCTS = (By.CLASS_NAME, 'product-miniature__inner')
    RANDOM_PRODUCT_LINK = (By.CSS_SELECTOR, 'a')
    RANDOM_PRODUCT_CART_BUTTON = (
        By.CSS_SELECTOR, 'button[data-button-action="add-to-cart"]')
    CART_MODAL = (By.ID, 'blockcart-modal')
    CHECKOUT_LINK = (By.CSS_SELECTOR, 'a[href*="cart?action=show"]')
    FIRST_PRODUCT = (By.CLASS_NAME, 'product-miniature__price')

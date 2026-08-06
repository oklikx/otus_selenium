"""Локаторы страницы корзины"""
from selenium.webdriver.common.by import By


class CartPageLocators:
    """Локаторы страницы корзины"""
    PAGE_TITLE = (By.CLASS_NAME, 'page-title-section')
    LINK_TO_PRODUCT = (By.CSS_SELECTOR, 'a.product-line__title')
    PRODUCT = (By.CLASS_NAME, 'product-line')
    REMOVE_PRODUCT_BUTTON = (By.CLASS_NAME, 'js-remove-from-cart')
    UPDATE_ALERT = (By.CLASS_NAME, 'js-cart-update-alert')

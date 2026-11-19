"""Локаторы главной страницы"""
from selenium.webdriver.common.by import By


class PrestaShopHomeLocators:
    """Локаторы главной страницы"""

    # Карточка товара — article.product-miniature (F12 вернул 10 штук)
    PRODUCTS = (By.CSS_SELECTOR, 'article.product-miniature')
    FIRST_PRODUCT = (By.CSS_SELECTOR, 'article.product-miniature')

    # Ссылка на страницу товара внутри карточки
    RANDOM_PRODUCT_LINK = (By.CSS_SELECTOR, 'a.product-miniature__title')

    # Кнопка "Add to cart" — подтверждено через F12
    RANDOM_PRODUCT_CART_BUTTON = (
        By.CSS_SELECTOR, 'button[data-button-action="add-to-cart"]'
    )

    # Модалка корзины — подтверждено через F12
    CART_MODAL = (By.ID, 'blockcart-modal')

    # Ссылка "Proceed to checkout" — подтверждено через F12
    CHECKOUT_LINK = (By.CSS_SELECTOR, 'a[href*="cart?action=show"]')
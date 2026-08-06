"""Тесты для удаления товара из корзины"""
from src.pom.pages.home_page import HomePage
from src.pom.pages.cart_page import CartPage


def test_delete_product_from_cart(driver):
    """Тесты на добавление товара в корзину с последующим его удалением"""
    home_page = HomePage(driver)
    home_page.open()
    home_page.add_random_product_to_cart()
    home_page.open_cart_modal_and_go_to_cart()

    cart_page = CartPage(driver)
    cart_page.delete_product()

    assert 'has been removed from the cart' in cart_page.get_update_alert().text

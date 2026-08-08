"""Тесты для добавления продукта в корзину"""
from src.pom.pages.home_page import HomePage
from src.pom.pages.cart_page import CartPage


def test_add_product_to_cart(driver):
    """Тест на добавление рандомного продкута в корзину"""
    home_page = HomePage(driver)
    home_page.open()

    exptected_product_url = home_page.add_random_product_to_cart()

    home_page.open_cart_modal_and_go_to_cart()

    cart_page = CartPage(driver)
    product_link = cart_page.get_link_to_product().get_attribute('href')

    assert cart_page.get_page_title() == 'Shopping Cart'

    assert exptected_product_url == product_link

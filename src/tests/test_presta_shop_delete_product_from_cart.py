"""Тесты для удаления товара из корзины"""
import allure
from src.pom.pages.home_page import HomePage
from src.pom.pages.cart_page import CartPage


@allure.epic("Интернет-магазин PrestaShop")
@allure.feature("Добавление товара в корзину")
@allure.story("Добавить товар в корзину и удалить его")
@allure.severity(allure.severity_level.BLOCKER)
def test_delete_product_from_cart(driver, base_url):
    """Тесты на добавление товара в корзину с последующим его удалением"""
    home_page = HomePage(driver, base_url)
    home_page.open()
    home_page.add_random_product_to_cart()
    home_page.open_cart_modal_and_go_to_cart()

    cart_page = CartPage(driver, base_url)
    cart_page.delete_product()

    assert 'has been removed from the cart' in cart_page.get_update_alert().text

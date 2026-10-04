"""Тесты для добавления продукта в корзину"""
import allure
from src.pom.pages.home_page import HomePage
from src.pom.pages.cart_page import CartPage


@allure.epic("Интернет-магазин PrestaShop")
@allure.feature("Корзина")
@allure.story("Добавление товаров")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Добавление случайного продукта в корзину с проверкой в UI")
def test_add_product_to_cart(driver):
    """Тест на добавление рандомного продкута в корзину"""
    home_page = HomePage(driver)

    home_page.open()

    exptected_product_url = home_page.add_random_product_to_cart()

    home_page.open_cart_modal_and_go_to_cart()

    cart_page = CartPage(driver)
    product_link = cart_page.get_link_to_product().get_attribute('href')

    with allure.step("Проверяем что заголовок страницы - Shopping Cart"):
        assert cart_page.get_page_title() == 'Shopping Cart'

    with allure.step("Проверяем, что ожидаемая ссылка и сслыка на товар совпали"):
        assert exptected_product_url == product_link

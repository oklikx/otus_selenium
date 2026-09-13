"""Тесты для переключения валюты"""
import allure
from src.pom.pages.home_page import HomePage
from src.pom.components.header import Header


@allure.epic("Инетрнет-магазин PrestaShop")
@allure.feature("Валюта")
@allure.story("Переключение валюты с евро на доллары на главной странице")
@allure.severity(allure.severity_level.MINOR)
def test_currency_switch_home_page(driver):
    """Тест на переключение валюты с евро на доллары на главной странице"""
    home_page = HomePage(driver)
    home_page.open()

    assert '€19.12' in home_page.get_first_product().text

    header = Header(driver)
    [euro_option, usd_option] = header.get_currency_select_options()

    assert euro_option.get_attribute('selected') == 'true'
    assert usd_option.get_attribute('selected') is None

    usd_option.click()

    [euro_option, usd_option] = header.get_currency_select_options()

    assert usd_option.get_attribute('selected') == 'true'
    assert euro_option.get_attribute('selected') is None

    assert "$22.19" in home_page.get_first_product().text

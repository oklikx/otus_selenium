"""Тесты с использованием selenium"""
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def wait_for_element(driver, by, locator, timeout=5):
    """Вспомогательная функция для явного ожидания элемента"""
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, locator))
    )


# =====================================================================
# ЧАСТЬ 2: Проверка наличия элементов (5 страниц х 5 элементов)
# =====================================================================

def test_page_elements_main(driver, base_url):
    """тесты для главной страницы"""
    driver.get(base_url)

    assert wait_for_element(
        driver, By.XPATH,
        "//img[contains(@class, 'logo') and contains(@class, 'img-fluid')]")
    assert wait_for_element(driver, By.CSS_SELECTOR,
                            'div[aria-label="Carousel container"]')
    assert wait_for_element(driver, By.CLASS_NAME, "ps-customtext")
    assert wait_for_element(driver, By.CLASS_NAME, "ps-featuredproducts")
    assert wait_for_element(driver, By.CLASS_NAME, "ps-newproducts")


def test_page_elements_catalog(driver, base_url):
    """тесты для Страница каталога (все товары)"""
    driver.get(f"{base_url}/2-home")
    assert wait_for_element(driver, By.CLASS_NAME, "category__header")
    assert wait_for_element(driver, By.CSS_SELECTOR, 'a[title="Clothes"]')
    assert wait_for_element(driver, By.CLASS_NAME, "products__count")
    assert wait_for_element(driver, By.CLASS_NAME, "products__sort")
    assert wait_for_element(driver, By.CLASS_NAME, "pagination__container")


def test_page_elements_product_card(driver, base_url):
    """Карточка товара"""
    driver.get(f"{base_url}/1-1-hummingbird-printed-t-shirt.html")
    assert wait_for_element(driver, By.CLASS_NAME, "product__name")
    assert wait_for_element(driver, By.CLASS_NAME, "product__manufacturer")
    assert wait_for_element(driver, By.CLASS_NAME, "product__tax-infos")
    assert wait_for_element(driver, By.CLASS_NAME, "product-variant")
    assert wait_for_element(driver, By.CLASS_NAME,
                            "product__add-to-cart-button")


def test_page_elements_registration(driver, base_url):
    """Страница регистрации пользователя"""
    driver.get(f"{base_url}/login")
    assert wait_for_element(driver, By.ID, "field-email")
    assert wait_for_element(driver, By.ID, "field-password")
    assert wait_for_element(driver, By.CSS_SELECTOR,
                            'a[href*="password-recovery"]')
    assert wait_for_element(driver, By.ID, "submit-login")
    assert wait_for_element(driver, By.CSS_SELECTOR,
                            'a[href*="registration"]')


def test_page_elements_admin_login(driver, base_url):
    """Страница логина в админку"""
    driver.get(f"{base_url}/registration")
    assert wait_for_element(driver, By.ID, "field-id_gender-label")
    assert wait_for_element(driver, By.ID, "field-firstname")
    assert wait_for_element(driver, By.ID, "field-lastname")
    assert wait_for_element(driver, By.ID, "field-email")
    assert wait_for_element(driver, By.ID, "field-password")


# =====================================================================
# ЧАСТЬ 3: Покрытие бизнес-сценариев
# =====================================================================


def test_3_1_login_logout(driver, base_url):
    """Автотест логина-разлогина"""
    driver.get(f"{base_url}/login")
    driver.find_element(
        By.CSS_SELECTOR, 'a[data-link-action="display-register-form"]').click()
    driver.find_element(By.ID, 'field-id_gender_2').click()
    driver.find_element(By.ID, 'field-firstname').send_keys('Екатерина')
    driver.find_element(By.ID, 'field-lastname').send_keys('Капитальцева')
    # стоит добавить рандомайзер для почты
    driver.find_element(By.ID, 'field-email').send_keys('testemail20@mail.ru')
    driver.find_element(By.ID, 'field-password').send_keys('testemail@mail.ru')
    driver.execute_script(
        "arguments[0].click()", driver.find_element(By.ID, "field-psgdpr"))
    driver.execute_script("arguments[0].click()",
                          driver.find_element(By.ID, "field-customer_privacy"))
    driver.execute_script(
        "arguments[0].click()",
        driver.find_element(By.CSS_SELECTOR,
                            'button[data-link-action="save-customer"]'))

    user_menu = wait_for_element(driver, By.ID, 'userMenuButton')
    assert "Е.К." in user_menu.text

    user_menu.click()
    driver.find_element(By.CSS_SELECTOR, 'a[href*="my-account"]').click()

    page_title = wait_for_element(driver, By.CLASS_NAME, "page-title-section")
    assert "Welcome Екатерина Капитальцева" in page_title.text

    signout_link = driver.find_element(By.ID, 'signout_link')
    driver.execute_script('arguments[0].click()', signout_link)

    signout_page_title = wait_for_element(
        driver, By.CLASS_NAME, "page-title-section")

    assert "Sign in" in signout_page_title.text


def test_3_2_add_random_product_to_cart(driver, base_url):
    """Добавление случайного товара с главной в корзину"""
    driver.get(base_url)

    products = driver.find_elements(
        By.CLASS_NAME, 'product-miniature__inner'
    )

    random_product = random.choice(products)
    random_product_link = random_product.find_element(By.CSS_SELECTOR, 'a')
    random_product_cart_button = random_product.find_element(
        By.CSS_SELECTOR, 'button[data-button-action="add-to-cart"]')

    # нужно сохранить href в переменную, пока не поменялась страница
    # иначе элемент устареет, его нельзя будет использовать с assert
    expected_url = random_product_link.get_attribute('href')

    driver.execute_script(
        "arguments[0].click()", random_product_cart_button)

    wait_for_element(driver, By.ID, 'blockcart-modal')

    proceed_to_checkout_link = driver.find_element(
        By.CSS_SELECTOR, 'a[href*="cart?action=show"]')

    driver.execute_script("arguments[0].click()", proceed_to_checkout_link)

    page_title = wait_for_element(driver, By.CLASS_NAME, 'page-title-section')
    assert page_title.text == 'Shopping Cart'

    link_to_product_in_the_cart = driver.find_element(
        By.CSS_SELECTOR, 'a.product-line__title')

    assert expected_url == link_to_product_in_the_cart.get_attribute('href')


def test_3_3_currency_switch_main_page(driver, base_url):
    """Переключение валют на главной странице"""
    driver.get(base_url)

    first_product = driver.find_element(
        By.CLASS_NAME, 'product-miniature__price')
    assert '€19.12' in first_product.text

    currency_select = driver.find_element(
        By.CLASS_NAME, 'js-currency-selector')
    currency_options = currency_select.find_elements(By.TAG_NAME, 'option')

    [euro_option, usd_option] = currency_options

    assert euro_option.get_attribute('selected') == 'true'
    assert usd_option.get_attribute('selected') is None

    usd_option.click()

    currency_select = driver.find_element(
        By.CLASS_NAME, 'js-currency-selector')
    currency_options = currency_select.find_elements(By.TAG_NAME, 'option')

    [euro_option, usd_option] = currency_options

    assert usd_option.get_attribute('selected') == 'true'
    assert euro_option.get_attribute('selected') is None

    first_product_usd = wait_for_element(driver,
                                         By.CLASS_NAME,
                                         'product-miniature__price')
    assert "$21.80" in first_product_usd.text


def test_3_4_currency_switch_catalog_page(driver, base_url):
    """Переключение валют в каталоге"""
    driver.get(f"{base_url}/2-home")

    first_product = driver.find_element(
        By.CLASS_NAME, 'product-miniature__price')
    assert '€19.12' in first_product.text

    currency_select = driver.find_element(
        By.CLASS_NAME, 'js-currency-selector')
    currency_options = currency_select.find_elements(By.TAG_NAME, 'option')

    [euro_option, usd_option] = currency_options

    assert euro_option.get_attribute('selected') == 'true'
    assert usd_option.get_attribute('selected') is None

    usd_option.click()

    currency_select = driver.find_element(
        By.CLASS_NAME, 'js-currency-selector')
    currency_options = currency_select.find_elements(By.TAG_NAME, 'option')

    [euro_option, usd_option] = currency_options

    assert usd_option.get_attribute('selected') == 'true'
    assert euro_option.get_attribute('selected') is None

    first_product_usd = wait_for_element(driver,
                                         By.CLASS_NAME,
                                         'product-miniature__price')
    assert "$21.80" in first_product_usd.text

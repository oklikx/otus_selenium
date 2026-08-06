"""Локаторы шапки сайта(общие компоненты)"""
from selenium.webdriver.common.by import By


class HeaderLocators():
    """Локаторы шапки сайта(общие компоненты)"""
    USER_MENU = (By.ID, 'userMenuButton')
    MY_PROFILE = (By.CSS_SELECTOR, 'a[href*="my-account"]')
    CURRENCY_SELECT = (By.CLASS_NAME, 'js-currency-selector')
    CURRENCY_OPTIONS = (By.TAG_NAME, 'option')

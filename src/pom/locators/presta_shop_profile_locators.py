"""Локаторы страницы профиля"""
from selenium.webdriver.common.by import By


class ProfilePageLocators():
    """Локаторы страницы профиля"""
    PAGE_TITLE = (By.CLASS_NAME, "page-title-section")
    SIGNOUT_LINK = (By.ID, 'signout_link')

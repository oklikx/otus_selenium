"""Локаторы страницы регистрации"""
from selenium.webdriver.common.by import By


class SignupLocators():
    """Локаторы для страницы регистрации"""
    REGISTER_FORM_LINK = (
        By.CSS_SELECTOR, 'a[data-link-action="display-register-form"]')
    FEMALE_CHECKBOX = (By.ID, 'field-id_gender_2')
    FIRSTNAME_INPUT = (By.ID, 'field-firstname')
    LASTNAME_INPUT = (By.ID, 'field-lastname')
    EMAIL_INPUT = (By.ID, 'field-email')
    PASSWORD_INPUT = (By.ID, 'field-password')
    PSGDPR_CHECKBOX = (By.ID, 'field-psgdpr')
    CUSTOMER_PRIVACY_CHECKBOX = (By.ID, 'field-customer_privacy')
    SAVE_CUSTOMER_BUTTON = (
        By.CSS_SELECTOR, 'button[data-link-action="save-customer"]')

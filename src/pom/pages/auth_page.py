"""Страница регистрации"""
from src.pom.pages.base_page import BasePage
from src.pom.locators.presta_shop_signup_locators import SignupLocators
from src.data.urls import LOGIN_PAGE_URL
from src.helpers.make_js_click import make_js_click


class AuthPage(BasePage):
    """Страница регистрации"""

    def open(self):
        """Открыть страницу регистрации"""
        self.driver.get(LOGIN_PAGE_URL)

    def sign_up(self):
        """Заполнить форму регистрации и нажать submit"""
        self.driver.find_element(*SignupLocators.REGISTER_FORM_LINK).click()
        self.driver.find_element(*SignupLocators.FEMALE_CHECKBOX).click()
        self.driver.find_element(
            *SignupLocators.FIRSTNAME_INPUT).send_keys('Екатерина')
        self.driver.find_element(
            *SignupLocators.LASTNAME_INPUT).send_keys('Капитальцева')
        # Емейл сохраняется где-то в сторе приложения, из-за чего на форме
        # срабатывает валидация (такая почта уже есть), каждый раз,
        # если тест падает, надо придумывать новую почту
        self.driver.find_element(
            *SignupLocators.EMAIL_INPUT).send_keys('testemail326@mail.ru')
        self.driver.find_element(
            *SignupLocators.PASSWORD_INPUT).send_keys('testemail@mail.ru')

        make_js_click(self.driver, self.driver.find_element(
            *SignupLocators.PSGDPR_CHECKBOX))

        make_js_click(self.driver, self.driver.find_element(
            *SignupLocators.CUSTOMER_PRIVACY_CHECKBOX))
        make_js_click(self.driver, self.driver.find_element(
            *SignupLocators.SAVE_CUSTOMER_BUTTON))

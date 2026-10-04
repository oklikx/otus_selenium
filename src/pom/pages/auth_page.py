"""Страница регистрации"""
import logging
import allure
from src.pom.pages.base_page import BasePage
from src.pom.locators.presta_shop_signup_locators import SignupLocators
from src.data.urls import LOGIN_PAGE_URL
from src.helpers.generate_random_email import generate_random_email
from src.helpers.make_js_click import make_js_click


logger = logging.getLogger("AutomationFramework.AuthPage")


class AuthPage(BasePage):
    """Страница регистрации"""

    @allure.step("Открыть страницу")
    def open(self):
        """Открыть страницу регистрации"""
        logger.info("Открываем страницу логина")
        self.driver.get(LOGIN_PAGE_URL)

    @allure.step("Заполнение формы регистрации")
    def sign_up(self):
        """Заполнить форму регистрации и нажать submit"""
        logger.info("Открываем форму регистрации")
        self.driver.find_element(*SignupLocators.REGISTER_FORM_LINK).click()

        logger.info("Проставляем чекбокс Mrs.")
        self.driver.find_element(*SignupLocators.FEMALE_CHECKBOX).click()

        logger.info("Заполняем имя")
        self.driver.find_element(
            *SignupLocators.FIRSTNAME_INPUT).send_keys('Екатерина')

        logger.info("Заполняем фамилию")
        self.driver.find_element(
            *SignupLocators.LASTNAME_INPUT).send_keys('Капитальцева')

        # Емейл сохраняется где-то в сторе приложения, из-за чего на форме
        # срабатывает валидация (такая почта уже есть), каждый раз,
        # если тест падает, надо придумывать новую почту
        logger.info("Заполняем почту")
        email = generate_random_email()
        logger.info('Сгенерировали рандомную почту - %s', email)
        self.driver.find_element(
            *SignupLocators.EMAIL_INPUT).send_keys(email)

        logger.info("Заполняем пароль")
        self.driver.find_element(
            *SignupLocators.PASSWORD_INPUT).send_keys('testemail@mail.ru')

        logger.info(
            'Отмечаем чекбокс I agree to the terms and conditions and the privacy policy')
        make_js_click(self.driver, self.driver.find_element(
            *SignupLocators.PSGDPR_CHECKBOX))

        logger.info("Отмечаем чекбокс Customer data privacy")
        make_js_click(self.driver, self.driver.find_element(
            *SignupLocators.CUSTOMER_PRIVACY_CHECKBOX))

        logger.info("Нажимаем на кнопку Create Account")
        make_js_click(self.driver, self.driver.find_element(
            *SignupLocators.SAVE_CUSTOMER_BUTTON))

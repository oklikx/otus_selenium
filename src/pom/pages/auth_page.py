"""Страница регистрации"""
import logging
import allure
from selenium.webdriver.support import expected_conditions as EC

from src.pom.pages.base_page import BasePage
from src.pom.locators.presta_shop_signup_locators import SignupLocators
from src.data.urls import LOGIN_PAGE_URL
from src.helpers.generate_random_email import generate_random_email
from src.helpers.make_js_click import make_js_click


logger = logging.getLogger("AutomationFramework.AuthPage")


class AuthPage(BasePage):
    """Страница регистрации"""

    @allure.step("Открыть страницу")
    def open(self, base_url):
        """Открыть страницу логина"""
        login_url = f"{base_url}/login"
        logger.info("Открываем страницу логина - %s", login_url)
        self.driver.get(login_url)
        self.wait.until(EC.presence_of_element_located(
            SignupLocators.REGISTER_FORM_LINK
        ))

    @allure.step("Заполнение формы регистрации")
    def sign_up(self):
        """Заполнить форму регистрации и нажать submit"""
        logger.info("Открываем форму регистрации")
        self.wait.until(EC.element_to_be_clickable(
            SignupLocators.REGISTER_FORM_LINK
        )).click()

        logger.info("Проставляем чекбокс Mrs.")
        female = self.wait.until(EC.element_to_be_clickable(
            SignupLocators.FEMALE_CHECKBOX
        ))
        if not female.is_selected():
            female.click()

        logger.info("Заполняем имя")
        self.wait.until(EC.visibility_of_element_located(
            SignupLocators.FIRSTNAME_INPUT
        )).send_keys('Екатерина')

        logger.info("Заполняем фамилию")
        self.driver.find_element(
            *SignupLocators.LASTNAME_INPUT).send_keys('Капитальцева')

        logger.info("Заполняем почту")
        email = generate_random_email()
        logger.info('Сгенерировали рандомную почту - %s', email)
        self.driver.find_element(
            *SignupLocators.EMAIL_INPUT).send_keys(email)

        logger.info("Заполняем пароль")
        self.driver.find_element(
            *SignupLocators.PASSWORD_INPUT).send_keys('Xk9#mPq2$vLz')

        logger.info("Отмечаем чекбокс I agree to the terms and conditions")
        gdpr = self.wait.until(EC.presence_of_element_located(
            SignupLocators.PSGDPR_CHECKBOX
        ))
        if not gdpr.is_selected():
            make_js_click(self.driver, gdpr)

        logger.info("Отмечаем чекбокс Customer data privacy")
        privacy = self.driver.find_element(
            *SignupLocators.CUSTOMER_PRIVACY_CHECKBOX)
        if not privacy.is_selected():
            make_js_click(self.driver, privacy)

        logger.info("Нажимаем на кнопку Create Account")
        make_js_click(self.driver, self.driver.find_element(
            *SignupLocators.SAVE_CUSTOMER_BUTTON))

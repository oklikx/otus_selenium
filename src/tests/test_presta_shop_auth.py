"""Тесты для аутентификации"""
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.pom.pages.auth_page import AuthPage
from src.pom.components.header import Header
from src.pom.pages.profile_page import ProfilePage
from src.helpers.make_js_click import make_js_click


@allure.epic("Интернет-магазин PrestaShop")
@allure.feature("Авторизация")
@allure.story("Зарегистрировать пользователя и разлогиниться")
@allure.severity(allure.severity_level.BLOCKER)
@allure.title("Регистрация пользователя с последующим разлогином")
def test_auth(driver, base_url):
    """Тест на регистрацию профиля и разлогин"""
    auth_page = AuthPage(driver, base_url)

    auth_page.open()
    auth_page.sign_up()

    header = Header(driver)
    user_menu = header.get_user_menu()

    assert "Екатерина Капитальцева" in user_menu.text
    user_menu.click()
    make_js_click(driver, header.get_my_profile_link())

    profile_page = ProfilePage(driver, base_url)
    assert 'Welcome Екатерина Капитальцева' in profile_page.get_page_title().text

    profile_page.click_signout_link()

    wait = WebDriverWait(driver, 15)
    wait.until(EC.url_contains("login"))

    assert "Sign in" in profile_page.get_page_title().text

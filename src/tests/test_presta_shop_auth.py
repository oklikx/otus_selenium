"""Тесты для аутентификации"""
from src.pom.pages.auth_page import AuthPage
from src.pom.components.header import Header
from src.pom.pages.profile_page import ProfilePage


def test_auth(driver):
    """Тест на регистрацию профиля и разлогин"""
    auth_page = AuthPage(driver)

    auth_page.open()
    auth_page.sign_up()

    header = Header(driver)
    user_menu = header.get_user_menu()

    assert "Екатерина Капитальцева" in user_menu.text
    user_menu.click()
    header.get_my_profile_link().click()

    profile_page = ProfilePage(driver)
    assert 'Welcome Екатерина Капитальцева' in profile_page.get_page_title().text

    profile_page.click_signout_link()

    assert "Sign in" in profile_page.get_page_title().text

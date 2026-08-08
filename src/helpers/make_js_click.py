"""Хелпер для клика"""


def make_js_click(driver, element):
    """Имитирует клик через джаваскрипт, тк click из селениума
        не срабатывает на некоторых элементах"""
    driver.execute_script("arguments[0].click()", element)

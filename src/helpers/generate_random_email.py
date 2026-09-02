"""генерация рандомной почты"""
import random
import string
from datetime import datetime


def generate_random_email(prefix="user", domain="test.com"):
    """
    Генерация уникального email с префиксом и датой

    Args:
        prefix: префикс для email (например, 'test' или 'user')
        domain: домен почты

    Returns:
        str: email вида prefix_20260127_abc123@test.com
    """
    # Текущая дата для уникальности
    date_str = datetime.now().strftime("%Y%m%d")

    # Случайная строка
    random_str = ''.join(random.choices(
        string.ascii_lowercase + string.digits, k=6))

    return f"{prefix}_{date_str}_{random_str}@{domain}"

# Пример:
# generate_random_email("test_user")
# → test_user_20260127_a1b2c3@test.com

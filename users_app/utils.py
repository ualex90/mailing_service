import random

from users_app.models import User

# генератор списка символов для ключа (0-9, A-Z, a-z)
key_symbols = [chr(i) for i in list(range(48, 58)) + list(range(65, 91)) + list(range(97, 123))]

# генератор списка символов для пароля (спецсимволы, 0-9, A-Z, a-z)
password_symbols = [chr(i) for i in list(range(33, 58)) + list(range(65, 91)) + list(range(97, 123))]


def get_user_key() -> str:
    """Генератор уникального ключа пользователя"""

    # с целью оптимизации, вызов генератора списка символов производится один раз при запуске функции
    # и полученный список сохраняется в переменную symbols
    symbols = key_symbols
    key = ''.join([random.choice(symbols) for i in range(25)])
    # если сгенерированный ключ существует у какого либо из пользователей, генерируем новый
    # до тех пор, пока он не будет уникальным
    while User.objects.filter(key=key):
        key = ''.join([random.choice(symbols) for i in range(25)])

    return key


def get_password() -> str:
    """Генератор случайного пароля"""

    symbols = password_symbols
    password = ''.join([random.choice(symbols) for i in range(10)])
    return password

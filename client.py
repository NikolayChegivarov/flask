# Выполняем HTTP запрос.

import requests
print("client")

# Создаем пользователя.
# response = requests.post("http://127.0.0.1:5000/user/",
#                          json={'name': 'user_2', "password": "12345679"},
#                          # headers={'token': 'come-token'}
#                          )

# Проверяем наличие того или иного пользователя по id.
# response = requests.get("http://127.0.0.1:5000/user/1/")

# Изменяем данные пользователя. Обязательно указываем пароль или убираем валидацию из вьюшки.
# response = requests.patch("http://127.0.0.1:5000/user/1/",
#                           json={"name": "new_user_name", "password": "87654321"})

# Удаляем пользователя.
# response = requests.delete("http://127.0.0.1:5000/user/1/")

# Создаем новое объявление.
# response = requests.post("http://127.0.0.1:5000/ads/",
#                          json={"title": "Пирожки",
#                                "description": "Продаю пирожки.",
#                                "owner_id": 3})

# Читаем объявление.
# response = requests.get("http://127.0.0.1:5000/ads/10/")

# Редактируем объявление.
# response = requests.get("http://127.0.0.1:5000/ads/10/",
#                          json={"title": "Пирожки",
#                                "description": "Продаю пирожки.",
#                                "owner_id": 3})


print(response.status_code)
print(response.json())

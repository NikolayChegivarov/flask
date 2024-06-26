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

# response = requests.post("http://127.0.0.1:5000/ads/",
#                          json={"title": "Пирожки",
#                                "description": "Продаю пирожки.",
#                                "owner_id": 3})

# response = requests.get("http://127.0.0.1:5000/ads/10/")


# # URL для создания объявления
# url = "http://127.0.0.1:5000/ads/"
#
# # Тело запроса с данными для нового объявления
# data = {
#     "title": "Новый автомобиль",
#     "description": "Продаю новый автомобиль 2024 года выпуска."
# }
#
# # Отправляем POST запрос
# response = requests.post(url, json=data)
#
# # Проверяем результат
# if response.status_code == 201:
#     print("Объявление успешно создано.")
#     print(response.json())
# else:
#     print("Ошибка при создании объявления:", response.text)



print(response.status_code)
print(response.json())

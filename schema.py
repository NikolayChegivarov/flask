# Этот модуль обеспечивает структурирование данных пользователей, их валидацию и предоставляет удобный способ
# определения форматов данных для создания и обновления пользовательских записей.
print("schema")
from typing import Optional, Type  # Импорт типов Optional (для необязательных значений) и Type (для типа класса).

import pydantic  # Импорт модуля pydantic для работы с валидацией данных.
from pydantic import BaseModel  # Импорт базовой модели данных из pydantic.


class BaseUser(BaseModel):
    """Базовая модель данных пользователя."""
    name: Optional[str]  # Поле имя юзера.
    password: Optional[str]

    @pydantic.field_validator("password")
    @classmethod
    def secure_password(cls, value):
        """Метод класса для валидации пароля."""
        if len(value) < 8:
            raise ValueError("password is too short")  # Проверка на минимальную длину пароля.
        return value  # Возвращаем значение, если валидация прошла успешно.


class BaseAds(BaseModel):
    """Базовая модель данных объявления."""
    title: Optional[str]
    description: Optional[str]


class CreateUser(BaseUser):
    """Для создания новых записей о пользователях в системе, где необходимо указать обязательные данные: имя и пароль."""
    name: str  # Обязательное поле для имени пользователя.
    password: str  # Обязательное поле для пароля пользователя.


class UpdateUser(BaseUser):
    """Для изминения данных юзера."""
    name: Optional[str]  # Опциональное поле для обновления имени пользователя.
    password: Optional[str]  # Опциональное поле для обновления пароля пользователя.


class CreateAds(BaseAds):
    """Для создания новых объявлений."""
    title: str
    description: str
    owner_id: int


class UpdateAds(BaseUser):
    """Для редактирования новых объявлений."""
    title: Optional[str]
    description: Optional[str]
    owner_id: Optional[int] = None

Schema = Type[CreateUser] | Type[UpdateUser] | Type[CreateAds] | Type[UpdateAds]
  # Определение переменной Schema как объединения типов CreateUser и UpdateUser, Type[CreateAds] | Type[UpdateAds.

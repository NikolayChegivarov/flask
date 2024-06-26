print("server")
import flask_bcrypt  # Импорт модуля для работы с хешированием паролей в Flask.
import pydantic  # Импорт библиотеки pydantic для валидации данных.
from flask import Flask, Response, jsonify, request  # Импорт необходимых классов и функций из Flask для создания веб-приложения.
from flask.views import MethodView  # Импорт класса MethodView из Flask для создания классовых представлений.
from sqlalchemy.exc import IntegrityError  # Импорт исключения IntegrityError из SQLAlchemy для обработки ошибок целостности данных.

from models import Session, User, Ads  # Импорт моделей данных User и Ads из модуля models.
from schema import CreateUser, Schema, UpdateUser, CreateAds, UpdateAds  # Импорт схем данных CreateUser, Schema, UpdateUser из модуля schema.

app = Flask("app")  # Создание экземпляра Flask с именем "app".
bcrypt = flask_bcrypt.Bcrypt(app)  # Создание экземпляра Bcrypt для работы с хешированием паролей в приложении Flask.


def hash_password(password: str) -> str:
    """Хеширует пароль"""
    password = password.encode()  # Преобразование строки пароля в байтовый формат.
    password = bcrypt.generate_password_hash(password)  # Хеширование пароля с использованием bcrypt.
    password = password.decode()  # Преобразование хешированного пароля из байтового формата в строку.
    return password  # Возврат хешированного пароля в виде строки.


def hash_description(description: str) -> str:
    """Хеширует описание объявления."""
    description = description.encode()  # Преобразование строки описания в байтовый формат.
    hashed_description = bcrypt.generate_password_hash(description)  # Хеширование описания с использованием bcrypt.
    hashed_description = hashed_description.decode()  # Преобразование хешированного описания из байтового формата в строку.
    print(hashed_description)
    return hashed_description  # Возврат хешированного описания в виде строки.


def check_password(hashed_password: str, password: str) -> bool:
    """"Для проверки соответствия введенного пароля хешированному паролю с использованием библиотеки bcrypt."""
    hashed_password = hashed_password.encode()  # Преобразование хешированного пароля из строки в байтовый формат.
    password = password.encode()  # Преобразование введенного пароля из строки в байтовый формат.
    return bcrypt.check_password_hash(hashed_password, password)  # Проверка соответствия введенного пароля хешированному паролю.


class HttpError(Exception):
    """Получает ошибку, отправляет сообщение клиенту. Используется в add_user, add_ads."""
    def __init__(self, status_code: int, error_message: str | dict):
        self.status_code = status_code
        self.error_message = error_message


def validate_user(schema_cls: Schema, json_data: dict):
    """Для валидации данных JSON с использованием заданной схемы (schema_cls) с помощью библиотеки pydantic."""
    try:
        return schema_cls(**json_data).dict(exclude_unset=True)
    except pydantic.ValidationError as err:
        error = err.errors()[0]
        error.pop("ctx", None)
        raise HttpError(409, error)


def validate_ads(schema_cls: Schema, json_data: dict):
    """Для валидации данных JSON с использованием заданной схемы (schema_cls) с помощью библиотеки pydantic."""
    try:
        return schema_cls(**json_data).dict(exclude_unset=True)
    except pydantic.ValidationError as err:
        error = err.errors()[0]
        error.pop("ctx", None)
        raise HttpError(409, error)


@app.errorhandler(HttpError)
def error_handler(err: HttpError):
    """Функция, вызываемая в случае ошибки. Извлекает информацию из ошибки, формирует HTTP-ответ."""
    try:
        json_response = jsonify({"error": err.error_message})
        json_response.status_code = err.status_code
        return json_response
    except ValueError:
        # Обработка случаев, когда error_message не является сериализуемым в формате JSON.
        json_response = jsonify({"error": "Internal Server Error"})
        json_response.status_code = 500
        return json_response


# Декоратор регистрирует функцию before_request как функцию, которая будет выполняться
@app.before_request  # автоматически перед каждым HTTP-запросом к приложению Flask (app).
def before_request():
    """Для открытия ссессии."""
    session = Session()
    request.session = session


# Декоратор регистрирует функцию after_request, которая будет выполняться автоматически после каждого HTTP-запроса
@app.after_request
def after_request(response: Response):
    """Для закрытия сессии."""
    request.session.close()
    return response


def get_user(user_id):
    """Ищет юзера по id. Заодно проверяет наличие пользователя в бд."""
    user = request.session.get(User, user_id)
    if user is None:
        raise HttpError(404, "user not found")
    return user


def get_ads(ads_id):
    """Извлекает пользователя из запроса."""
    ads = request.session.get(Ads, ads_id)
    if ads is None:
        raise HttpError(404, "user not found")
    return ads


def add_user(user: User):
    """Для создания и обновления пользователя в б.д."""
    request.session.add(user)  # Добавляет объект пользователя user в текущую сессию.
    try:
        request.session.commit()  # Сохраняет изминения сделанные в текущей ссессии.
    except IntegrityError:  # Позволяет предотвратить добавление дублирующихся данных.
        raise HttpError(400, "user already exists")
    return user


def add_ads(ads: Ads):
    """Для создания и обновления объявления в б.д."""
    request.session.add(ads)  # Добавляет объект пользователя user в текущую сессию.
    try:
        request.session.commit()  # Сохраняет изминения сделанные в текущей ссессии.
    except IntegrityError:  # Позволяет предотвратить добавление дублирующихся данных.
        raise HttpError(400, "ad already exists")
    return ads


class UserView(MethodView):

    @property
    def session(self) -> Session:
        """Метод возвращает текущую сессию, нужен для доступа к б.д."""
        return request.session

    def get(self, user_id):
        """Получаем данные о пользователе по его user_id."""
        user = get_user(user_id)
        return jsonify(user.json)

    def post(self):
        """Создает пользователя"""
        json_data = validate_user(CreateUser, request.json)  # Валидирует JSON данные, где CreateUser - это схема для создания пользователя.
        json_data["password"] = hash_password(json_data["password"])  # Хеширует пароль.
        user = add_user(User(**json_data))  # Добавляет нового пользователя в базу данных.
        return jsonify(user.json)

    def patch(self, user_id):
        """Обрабатывает HTTP PATCH запросы для обновления данных пользователя по его user_id."""
        json_data = validate_user(UpdateUser, request.json)
        if "password" in json_data:
            json_data["password"] = hash_password(json_data["password"])
        user = get_user(user_id)
        for field, value in json_data.items():
            setattr(user, field, value)
        user = add_user(user)
        return jsonify(user.json)

    def delete(self, user_id):
        user = get_user(user_id)
        self.session.delete(user)
        self.session.commit()
        return jsonify({"status": "deleted"})


class AdsView(MethodView):
    @property
    def session(self) -> Session:
        return request.session

    def get(self, ads_id):
        ads = get_ads(ads_id)
        return jsonify(ads.json)


    def post(self):
        """Создает объявление"""
        try:
            json_data = request.json  # Получаем данные из запроса
            # Валидация и преобразование данных
            validated_data = CreateAds(**json_data)

            # Создание объявления
            new_ad = Ads(
                title=validated_data.title,
                description=validated_data.description,
                owner_id=validated_data.owner_id  # Передача owner_id из валидированных данных
            )

            # Добавление объявления в базу данных (предполагаемая функция add_ads)
            added_ad = add_ads(new_ad)

            # Возвращаем JSON-представление созданного объявления
            return jsonify(added_ad.json)

        except pydantic.ValidationError as e:
            # Обработка ошибок валидации данных от pydantic
            return jsonify({"error": str(e)}), 400

        except Exception as e:
            # Обработка других исключений
            return jsonify({"error": str(e)}), 500

    def patch(self, ads_id):
        """Редактирует объявление."""
        json_data = validate_ads(UpdateAds, request.json)
        if "description" in json_data:
            json_data["description"] = hash_description(json_data["description"])
        ads = get_ads(ads_id)
        for field, value in json_data.items():
            setattr(ads, field, value)
        ads = add_ads(ads)
        return jsonify(ads.json)

    def delete(self, ads_id):
        """Удаляет объявление."""
        ads = get_user(ads_id)
        self.session.delete(ads)
        self.session.commit()
        return jsonify({"status": "deleted"})

# Что бы мы могли привязывать наш класс к url приобразовываем класс во viev функцию
user_view = UserView.as_view("user")
ads_view = AdsView.as_view("ads")

# Привязываем маршруты к URL.
app.add_url_rule("/user/", view_func=user_view, methods=["POST"])
app.add_url_rule("/user/<int:user_id>/", view_func=user_view, methods=["GET", "PATCH", "DELETE"])

app.add_url_rule("/ads/", view_func=ads_view, methods=["POST"])
app.add_url_rule("/ads/<int:ads_id>/", view_func=ads_view, methods=["GET", "PATCH", "DELETE"])

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)

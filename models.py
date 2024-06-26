print("models")
import datetime
import os
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped  # Импорт необходимых инструментов ORM SQLAlchemy.
from sqlalchemy import Integer, String, DateTime, func, create_engine  # Импорт типов данных и функций SQLAlchemy.
# func позволяет делать функции на стороне бд.
from atexit import register  # Импорт функции регистрации обратного вызова для завершения работы программы.
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from dotenv import load_dotenv
load_dotenv()

# Получаем переменные окружения для настройки подключения к PostgreSQL.
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
print(f"получаем переменные окружения? - {POSTGRES_PORT}")


# Создаем строку подключения (DSN) для SQLAlchemy с использованием переменных окружения.
connection_string = (f"postgresql+psycopg2://"
                     f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
                     f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")

# Создаем движок SQLAlchemy для установления соединения с базой данных.
engine = create_engine(connection_string)

# Создаем класс сессии для управления соединениями с базой данных.
Session = sessionmaker(bind=engine)


# Базовый класс для определения ORM-моделей, он наследуется от DeclarativeBase.
class Base(DeclarativeBase):
    pass


# Определяем модели.
class Ads(Base):
    __tablename__ = "app_ads"

    ads_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(384), nullable=False)  # Описание.
    registration_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())

    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey('app_users.id'), nullable=False)
    owner: Mapped['User'] = relationship('User', back_populates='ads')

    @property
    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "registration_time": self.registration_time.isoformat(),
            "owner": self.owner.name  # Доступ к имени владельца через отношения
        }


class User(Base):
    __tablename__ = "app_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(72), nullable=False)
    registration_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())

    ads: Mapped[list['Ads']] = relationship('Ads', back_populates='owner')

    # для создания специальных методов, которые можно вызывать как атрибуты объекта, а не как обычные методы
    @property
    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "registration_time": self.registration_time.isoformat()
        }


# Создаем таблицы в базе данных на основе всех объявленных моделей, наследующихся от Base.
Base.metadata.create_all(bind=engine)

# Регистрируем функцию engine.dispose для вызова при завершении программы для корректного закрытия соединения с базой данных.
register(engine.dispose)

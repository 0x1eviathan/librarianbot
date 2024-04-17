from time import time_ns
from typing import List, Type, Any

from sqlalchemy import create_engine, Column, Values, Integer, BigInteger, Float, String, Boolean
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy.sql.expression import or_


# Создаем подключение
engine = create_engine('postgresql://postgres:postgres@localhost:5432/bot')

Base = declarative_base()


# ТАБЛИЦА ПОЛЬЗОВАТЕЛЕЙ
class Users(Base): 
    __tablename__ = 'users'
    
    id = Column(Integer, autoincrement=True, primary_key=True)
    chat_id = Column(BigInteger)
    username = Column(String)
    date = Column(BigInteger) 


# ТАБЛИЦА С КНИГАМИ
class Books(Base): 
    __tablename__ = 'books'
    
    id = Column(Integer, autoincrement=True, primary_key=True)
    book_owner = Column(BigInteger)
    book_name = Column(String)
    book_author = Column(String) 
    book_description = Column(String)
    book_genre = Column(String)
    date = Column(BigInteger)


# ТАБЛИЦА С ЖАНРАМИ
class Genres(Base):
    __tablename__ = 'genres'

    id = Column(Integer, autoincrement=True, primary_key=True)
    genre = Column(String)
    date = Column(BigInteger)


# DATABASE API    
class Database: 
    def __init__(self): 
        self.session = Session(bind=engine)

    # Создание таблиц
    @staticmethod
    def create_tables() -> None:
        Base.metadata.create_all(engine)

    def get_genres(self):
        return self.session.query(Genres).all()

    def add_genre(self, genre):
        self.session.add(
            Genres(
                genre=genre,
                date=time_ns()
            )
        )
        self.session.commit()

    # Получить пользователя
    def get_user(self, chat_id: int) -> Type[Users] | None:
        return self.session.query(Users).filter_by(chat_id=chat_id).first()

    # Добавить пользователя
    def add_user(self, chat_id: int, username: str) -> None: 
        self.session.add(
            Users(
                chat_id=chat_id,
                username=username,
                date=time_ns()
            )
        )
        self.session.commit()

    # Добавление книги
    def add_book(self, book_owner: int, book_name: str, book_author: str, book_description: str,
                 book_genre: str) -> None:
        self.session.add(
            Books(
                book_owner=book_owner,
                book_name=book_name,
                book_author=book_author,
                book_description=book_description,
                book_genre=book_genre,
                date=time_ns()
            )
        )
        self.session.commit()

    # Получение списка книг по chat id
    def get_my_books(self, chat_id: int) -> list[Type[Books]]:
        return self.session.query(Books).filter_by(book_owner=chat_id).all()

    # Получение книги по book id
    def get_my_book(self, book_id: int) -> Type[Books] | None:
        return self.session.query(Books).filter_by(id=book_id).first()

    # Проверка существует ли такая книга
    def check_book(self, book_owner: int, book_name: str) -> bool:
        return bool(self.session.query(Books).filter_by(book_owner=book_owner, book_name=book_name).first())

    # Получение книг пользователя по chat id + key word
    def get_searched_books(self, book_owner: int, key_word: str) -> list[Type[Books]]:
        return self.session.query(Books).filter(
            (Books.book_owner == book_owner)
            &
            (or_(
                Books.book_name.like(f'%{key_word}%'),
                Books.book_author.like(f'%{key_word}%')
            ))
        ).all()

    # Удаление книги из базы данных
    def delete_my_book(self, book_id: int) -> None:
        self.session.query(Books).filter_by(id=book_id).delete()
        self.session.commit()

    # Фиксация транзакции
    def session_commit(self) -> None:
        self.session.commit() 

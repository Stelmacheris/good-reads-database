from __future__ import annotations
from typing import Optional, List
from sqlalchemy import ForeignKey, Integer, Date, Column, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

books_authors = Table(
    'books_authors',
    Base.metadata,
    Column('index',Integer,primary_key=True,autoincrement=True),
    Column('books_id', Integer, ForeignKey('all_good_books_info.index')),
    Column('author_id', Integer, ForeignKey('author.index'))
)

books_genres = Table(
    'books_genres',
    Base.metadata,
    Column('index',Integer,primary_key=True,autoincrement=True),
    Column('books_id', Integer, ForeignKey('all_good_books_info.index')),
    Column('genres_id', Integer, ForeignKey('genres.index'))
)

books_characters = Table(
    'books_characters',
    Base.metadata,
    Column('index', Integer, primary_key=True, autoincrement=True),
    Column('books_id', Integer, ForeignKey('all_good_books_info.index')),
    Column('characters_id', Integer, ForeignKey('characters.index'))
)

books_awards = Table(
    'books_awards',
    Base.metadata,
    Column('index',Integer,primary_key=True,autoincrement=True),
    Column('books_id', Integer, ForeignKey('all_good_books_info.index')),
    Column('awards_id', Integer, ForeignKey('awards.index'))
)
books_settings = Table(
    'books_settings',
    Base.metadata,
    Column('index',Integer,primary_key=True,autoincrement=True),
    Column('books_id', Integer, ForeignKey('all_good_books_info.index')),
    Column('settings_id', Integer, ForeignKey('setting.index'))
)

books_stars = Table(
    'books_stars',
    Base.metadata,
    Column('index',Integer,primary_key=True,autoincrement=True),
    Column('books_id', Integer, ForeignKey('all_good_books_info.index')),
    Column('stars_id', Integer, ForeignKey('ratingsbystars.index'))
)
class Series(Base):
    """
    Represents a series of books.
    """
    __tablename__ = 'series'
    index: Mapped[int] = mapped_column(primary_key=True,unique=True,autoincrement=True)
    series: Mapped[Optional[str]] = mapped_column(nullable=True)
class AllGoodBooksInfo(Base):
    """
    Represents detailed information about a book.
    """
    __tablename__ = 'all_good_books_info'
    index: Mapped[int] = mapped_column(primary_key=True,unique=True,autoincrement=True)
    bookId: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str]
    series: Mapped[Optional[str]] = mapped_column(nullable=True)
    author: Mapped[str]
    rating: Mapped[float]
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    language: Mapped[Optional[str]] = mapped_column(nullable=True)
    isbn: Mapped[str]
    genres:Mapped[str]
    characters:Mapped[str]
    bookFormat: Mapped[Optional[str]] = mapped_column(nullable=True)
    edition: Mapped[Optional[str]] = mapped_column(nullable=True)
    pages: Mapped[Optional[int]] = mapped_column(nullable=True)
    publisher: Mapped[Optional[str]]
    publishDate: Mapped[Optional[str]] = mapped_column(Date(),nullable=True)
    firstPublishDate: Mapped[Optional[str]] = mapped_column(Date(),nullable=True)
    awards: Mapped[str]
    numRatings: Mapped[int]
    ratingsByStars: Mapped[str]
    likedPercent: Mapped[Optional[float]] = mapped_column(nullable=True)
    setting: Mapped[str]
    coverImg: Mapped[Optional[str]] = mapped_column(nullable=True)
    bbeScore: Mapped[float]
    bbeVotes: Mapped[int]
    price: Mapped[Optional[float]] = mapped_column(nullable=True)
    authors: Mapped[List[Author]] = relationship(secondary=books_authors,back_populates='books')
    genres_list: Mapped[List[Genres]] = relationship(secondary=books_genres,back_populates='books')
    characters_list: Mapped[List[Characters]] = relationship(secondary=books_characters,back_populates='books')
    awards_list: Mapped[List[Awards]] = relationship(secondary=books_awards,back_populates='books')
    settings_list: Mapped[List[Setting]] = relationship(secondary=books_settings,back_populates='books')
    stars_list: Mapped[List[RatingsByStars]] = relationship(secondary=books_stars,back_populates='books')
    series_id: Mapped[int] = mapped_column(ForeignKey('series.index'),nullable=True)
    publish_info_id: Mapped[int] = mapped_column(ForeignKey('publish_info.index'),nullable=True)

    booksSeries: Mapped[Series] = relationship('Series')
    publishSeries: Mapped[Series] = relationship('PublishInfo')

class Author(Base):
    """
    Represents an author.
    """
    __tablename__ = 'author'
    index: Mapped[int] = mapped_column(primary_key=True,unique=True,autoincrement=True)
    author:Mapped[str]
    books: Mapped[List[AllGoodBooksInfo]] = relationship(secondary=books_authors,back_populates='authors')

class Genres(Base):
    """
    Represents a genre.
    """
    __tablename__ = 'genres'
    index: Mapped[int] = mapped_column(primary_key=True,unique=True,autoincrement=True)
    genres:Mapped[str]
    books: Mapped[List[AllGoodBooksInfo]] = relationship(secondary=books_genres,back_populates='genres_list')

class Characters(Base):
    """
    Represents a character in a book.
    """
    __tablename__ = 'characters'
    index: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    characters: Mapped[str] = mapped_column(nullable=True)
    books: Mapped[List[AllGoodBooksInfo]] = relationship(secondary=books_characters, back_populates='characters_list')

class Awards(Base):
    """
    Represents an award a book has received.
    """
    __tablename__ = 'awards'
    index: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    awards: Mapped[str] = mapped_column(nullable=True)
    books: Mapped[List[AllGoodBooksInfo]] = relationship(secondary=books_awards, back_populates='awards_list')

class RatingsByStars(Base):
    """
    Represents star ratings for a book.
    """
    __tablename__ = 'ratingsbystars'
    index: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    ratingsByStars: Mapped[str] = mapped_column(nullable=True)
    books: Mapped[List[AllGoodBooksInfo]] = relationship(secondary=books_stars, back_populates='stars_list')

class Setting(Base):
    """
    Represents the setting of a book.
    """
    __tablename__ = 'setting'
    index: Mapped[int] = mapped_column(primary_key=True,unique=True,autoincrement=True)
    setting:Mapped[str] = mapped_column(nullable=True)
    books: Mapped[List[AllGoodBooksInfo]] = relationship(secondary=books_settings,back_populates='settings_list')

class PublishInfo(Base):
    """
    Represents publishing information for a book.
    """
    __tablename__ = 'publish_info'
    index: Mapped[int] = mapped_column(primary_key=True,unique=True,autoincrement=True)
    bookFormat: Mapped[Optional[str]] = mapped_column(nullable=True)
    edition: Mapped[Optional[str]] = mapped_column(nullable=True)
    pages: Mapped[Optional[int]] = mapped_column(nullable=True)
    publisher: Mapped[Optional[str]]
    publishDate: Mapped[Optional[str]] = mapped_column(Date(), nullable=True)
    firstPublishDate: Mapped[Optional[str]] = mapped_column(Date(), nullable=True)

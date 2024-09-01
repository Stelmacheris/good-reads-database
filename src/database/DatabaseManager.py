import pandas as pd
from sqlalchemy.orm import sessionmaker, Session
from src.database.Models import AllGoodBooksInfo, Genres, Author, Characters, Awards, RatingsByStars, Setting, Series, PublishInfo
from ast import literal_eval
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text, select
from typing import List,Dict,Tuple,Any
from sqlalchemy.engine import Engine

class DatabaseTableManager:
    """
    A manager class for handling database table operations such as inserting a DataFrame into a table 
    and dropping specified columns from a table.
    
    Attributes:
        engine (Engine): The SQLAlchemy engine connected to the database.
        df (pd.DataFrame): The DataFrame to be inserted into the database.
        table_name (str): The name of the table in the database.
    """

    def __init__(self, engine: Engine, df: pd.DataFrame, table_name: str) -> None:
        """
        Initializes the DatabaseTableManager with a database engine, a DataFrame, and a table name.

        Args:
            engine (Engine): The SQLAlchemy engine connected to the database.
            df (pd.DataFrame): The DataFrame to be inserted into the database.
            table_name (str): The name of the table in the database.
        """
        self.engine = engine
        self.df = df
        self.table_name = table_name

    def insert_df_into_database(self) -> None:
        """
        Inserts the DataFrame into the specified table in the database.

        If the table already exists, the DataFrame will be appended to it.
        """
        self.df.to_sql(self.table_name, self.engine, if_exists='append')

    def drop_columns(self, columns: List[str]) -> None:
        """
        Drops the specified columns from the table in the database.

        Args:
            columns (List[str]): A list of column names to be dropped from the table.
        """
        with self.engine.connect() as con:
            trans = con.begin()
            try:
                for col in columns:
                    query = f'ALTER TABLE public.{self.table_name} DROP COLUMN IF EXISTS {col};'
                    con.execute(text(query))
                trans.commit()
            except Exception as e:
                trans.rollback()
                raise e
    
class TableTransformation:
    """
    A class for handling table transformations and many-to-many relationship mappings in a database.
    
    Attributes:
        engine (Engine): The SQLAlchemy engine connected to the database.
        df (pd.DataFrame): The DataFrame to be used for transformations.
    """

    def __init__(self, engine: Engine, df: pd.DataFrame) -> None:
        """
        Initializes the TableTransformation with a database engine and a DataFrame.

        Args:
            engine (Engine): The SQLAlchemy engine connected to the database.
            df (pd.DataFrame): The DataFrame to be used for transformations.
        """
        self.engine = engine
        self.df = df

    def transform_many_to_many_relationships_to_df(self, data: List[Tuple[int, str]], 
                                                   all_good_books_info: List[Tuple[Any]], 
                                                   relationship_column_name: str, row_index: int) -> pd.DataFrame:
        """
        Transforms many-to-many relationships into a DataFrame.

        Args:
            data (List[Tuple[int, str]]): List of tuples containing relationship data.
            all_good_books_info (List[Tuple[Any]]): List of tuples containing all book information.
            relationship_column_name (str): The name of the relationship column.
            row_index (int): The index of the row to evaluate in the all_good_books_info.

        Returns:
            pd.DataFrame: DataFrame containing the transformed relationships.
        """
        dict_data = {val[1]: val[0] for val in data}
        books_id = []
        relationship_id = []

        try:
            for row in all_good_books_info:
                evaluated_values = self.make_eval(row[row_index])
                list_cross = [dict_data[val] for val in evaluated_values if val in dict_data]
                books_id.extend([row[0]] * len(list_cross))
                relationship_id.extend(list_cross)

            relationship_df = pd.DataFrame({
                'books_id': books_id,
                relationship_column_name: relationship_id
            })
            return relationship_df

        except SQLAlchemyError as e:
            print(f"An error occurred: {e}")
            return pd.DataFrame()

    def find_many_to_many_relationships(self) -> None:
        """
        Finds and transforms many-to-many relationships and inserts them into the database.
        """
        Session = sessionmaker(bind=self.engine)
        session = Session()
        
        try:
            all_good_books_info = session.query(
                AllGoodBooksInfo.index,
                AllGoodBooksInfo.author,
                AllGoodBooksInfo.genres,
                AllGoodBooksInfo.characters,
                AllGoodBooksInfo.awards,
                AllGoodBooksInfo.setting,
                AllGoodBooksInfo.ratingsByStars
            ).all()
            
            query_data = {
                'books_authors': session.query(Author.index, Author.author).all(),
                'books_genres': session.query(Genres.index, Genres.genres).all(),
                'books_characters': session.query(Characters.index, Characters.characters).all(),
                'books_awards': session.query(Awards.index, Awards.awards).all(),
                'books_settings': session.query(Setting.index, Setting.setting).all(),
                'books_stars': session.query(RatingsByStars.index, RatingsByStars.ratingsByStars).all()
            }

            relationship_column_names = ['author_id', 'genres_id', 'characters_id', 'awards_id', 'settings_id', 'stars_id']

            for i, (table_name, data) in enumerate(query_data.items()):
                relationship_df = self.transform_many_to_many_relationships_to_df(data, all_good_books_info, relationship_column_names[i], i + 1)
                relationship_table_manager = DatabaseTableManager(self.engine, relationship_df, table_name)
                relationship_table_manager.insert_df_into_database()

        except SQLAlchemyError as e:
            print(f"An error occurred while fetching data: {e}")
        finally:
            session.close()

    def find_index_of_values(self, first_list: Dict[str, int], second_list: List[str]) -> List[int]:
        """
        Finds the index of values in the first list that are present in the second list.

        Args:
            first_list (Dict[str, int]): A dictionary of values with their corresponding indices.
            second_list (List[str]): A list of values to find in the first list.

        Returns:
            List[int]: List of indices of the found values.
        """
        cross_list = set(list(first_list.keys())) & set(second_list)
        return [first_list[val] for val in cross_list]

    def make_eval(self, x: str) -> List[str]:
        """
        Safely evaluates a string to a list.

        Args:
            x (str): The string to evaluate.

        Returns:
            List[str]: The evaluated list or the original string wrapped in a list.
        """
        try:
            return literal_eval(x)
        except:
            return [x]

    def update_series_id(self, book_info: AllGoodBooksInfo, session: Session) -> None:
        """
        Updates the series ID for a given book.

        Args:
            book_info (AllGoodBooksInfo): The book information to update.
            session (Session): The SQLAlchemy session to use for the query.
        """
        if book_info.series:
            series_record = session.execute(select(Series).where(Series.series == book_info.series)).scalar_one_or_none()
            if series_record:
                book_info.series_id = series_record.index

    def update_all_series_ids(self) -> None:
        """
        Updates the series IDs for all books in the database.
        """
        Session = sessionmaker(bind=self.engine)
        session = Session()
        all_books = session.query(AllGoodBooksInfo).all()
        for book in all_books:
            self.update_series_id(book, session)
        session.commit()
        session.close()
    
    def update_series_id(self) -> None:
        """
        Updates the series ID for all books in the database based on the series name.
        """
        Session = sessionmaker(bind=self.engine)
        session = Session()

        series_dict = {s.series: s.index for s in session.query(Series).all()}
        books = session.query(AllGoodBooksInfo).all()
        
        for book in books:
            try:
                book.series_id = series_dict[book.series]
            except:
                pass

        session.commit()
        session.close()

    def update_publish_info_id(self) -> None:
        """
        Updates the publish info ID for all books in the database based on publish info.
        """
        Session = sessionmaker(bind=self.engine)
        session = Session()
        
        publish_info_dict = {
            (p.bookFormat, p.edition, p.pages, p.publisher, p.publishDate, p.firstPublishDate): p.index
            for p in session.query(PublishInfo).all()
        }
        
        books = session.query(AllGoodBooksInfo).all()
        for book in books:
            key = (book.bookFormat, book.edition, book.pages, book.publisher, book.publishDate, book.firstPublishDate)
            try:
                book.publish_info_id = publish_info_dict[key]
            except:
                pass     
        session.commit()
        session.close()




from src.DataHandler import CsvDataHandler,DataFrameCleansing
from src.database.PostgresConnection import PostgresConnection
from src.database.Models import Base
import pandas as pd
from src.database.DatabaseManager import DatabaseTableManager,TableTransformation
from sqlalchemy.engine import Engine

if __name__ == "__main__":
    file_path: str = "./books_Best_Books_Ever.csv"

    csv_data_handler: CsvDataHandler = CsvDataHandler(file_path)
    df: pd.core.frame.DataFrame = csv_data_handler.read_data_to_df()

    data_frame_cleansing: DataFrameCleansing = DataFrameCleansing(df)
    data_frame_cleansing.apply_cleansing()
    df_cleaned: pd.DataFrame = data_frame_cleansing.get_df()
    df_cleaned: pd.DataFrame = data_frame_cleansing.get_df()

    postgres_connection: PostgresConnection = PostgresConnection()
    engine: Engine = postgres_connection.get_engine()

    Base.metadata.create_all(engine)

    cleaned_data_table_manager: DatabaseTableManager = DatabaseTableManager(engine,df_cleaned,'all_good_books_info')
    cleaned_data_table_manager.insert_df_into_database()

    publish_info_df: pd.DataFrame = df_cleaned[['bookFormat','edition', 'pages', 'publisher', 'publishDate', 'firstPublishDate']].drop_duplicates()

    publish_info_table_manager: DatabaseTableManager = DatabaseTableManager(engine,publish_info_df,'publish_info')
    publish_info_table_manager.insert_df_into_database()

    list_columns: list[str] = ['author', 'genres', 'characters', 'awards', 'ratingsByStars', 'setting']
    for column in list_columns:
        df_column: pd.DataFrame = data_frame_cleansing.distinct_values_from_list(column)
        column_manager: DatabaseTableManager = DatabaseTableManager(engine,df_column,column.lower())
        column_manager.insert_df_into_database()

    df_series: pd.DataFrame = data_frame_cleansing.distinct_values_from_list('series')
    series_columns_manager: DatabaseTableManager = DatabaseTableManager(engine,df_series,'series')
    series_columns_manager.insert_df_into_database()

    table_transformation: TableTransformation = TableTransformation(engine,df_cleaned)
    table_transformation.find_many_to_many_relationships()
    table_transformation.update_series_id()
    table_transformation.update_publish_info_id()

    drop_columns_manager: DatabaseTableManager = DatabaseTableManager(engine,df_cleaned,'all_good_books_info')
    drop_columns_manager.drop_columns(['author','genres', 'characters', 'awards', 'setting','bookFormat','series','edition', 'pages', 'publisher', 'publishDate', 'firstPublishDate','"ratingsByStars"'])
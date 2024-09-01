import pandas as pd
from ast import literal_eval
from dateutil import parser
import re
from typing import Optional,Any

class CsvDataHandler:
    """
    A class to handle CSV data operations including reading data into a DataFrame.
    
    Attributes:
        file_path (str): The path to the CSV file.
        df (Optional[pd.DataFrame]): The DataFrame to hold the CSV data.
    """

    def __init__(self, file_path: str) -> None:
        """
        Initializes the CsvDataHandler with a file path.

        Args:
            file_path (str): The path to the CSV file.
        """
        self.file_path = file_path
        self.df: Optional[pd.DataFrame] = None

    def read_data_to_df(self) -> pd.DataFrame:
        """
        Reads the CSV data into a DataFrame.

        Returns:
            pd.DataFrame: The DataFrame containing the CSV data.
        """
        self.df = pd.read_csv(self.file_path, header=0)
        return self.df
    
class DataFrameCleansing:
    """
    A class to perform data cleansing operations on a DataFrame.
    
    Attributes:
        df (pd.DataFrame): The DataFrame to be cleansed.
    """

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Initializes the DataFrameCleansing with a DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame to be cleansed.
        """
        self.df = df

    def make_list(self, cell: str) -> list:
        """
        Converts a string cell to a list if it contains commas.

        Args:
            cell (str): The cell value to be converted.

        Returns:
            list: The converted list or the original cell value.
        """
        if cell is None:
            return None
        elif "," in cell:
            return str(cell.split(","))
        else:
            return cell

    def get_df(self) -> pd.DataFrame:
        """
        Returns the DataFrame.

        Returns:
            pd.DataFrame: The cleansed DataFrame.
        """
        return self.df

    def parse_dates(self, date: str) -> str:
        """
        Parses a date string and returns it in 'YYYY-MM-DD' format.

        Args:
            date (str): The date string to be parsed.

        Returns:
            str: The parsed date string.
        """
        try:
            return parser.parse(date).strftime('%Y-%m-%d') if pd.notnull(date) else date
        except:
            return None

    def remove_dots_except_last(self, value: str) -> str:
        """
        Removes all dots from a string except the last one.

        Args:
            value (str): The string value to be processed.

        Returns:
            str: The processed string with dots removed except the last one.
        """
        str_value = str(value)
        last_dot_index = str_value.rfind('.')
        if last_dot_index != -1:
            return str_value[:last_dot_index].replace('.', '') + str_value[last_dot_index:]
        else:
            return str_value
    
    def apply_cleansing(self) -> pd.DataFrame:
        """
        Applies cleansing operations to the DataFrame.

        Returns:
            pd.DataFrame: The cleansed DataFrame.
        """
        self.df['author'] = self.df['author'].apply(self.make_list)
        for col in ['publishDate', 'firstPublishDate']:
            self.df[col] = self.df[col].apply(self.parse_dates)
        self.df['price'] = self.df['price'].apply(self.remove_dots_except_last)
        self.df['pages'] = self.df['pages'].astype(str).apply(lambda x: re.sub(r'\D', '', x) if x else pd.NA)
        self.df['pages'] = self.df['pages'].replace('', pd.NA)
        return self.df
    
    def distinct_values_from_list(self, col: str) -> pd.DataFrame:
        """
        Gets distinct values from a column containing lists and returns them as a DataFrame.

        Args:
            col (str): The column name to extract distinct values from.

        Returns:
            pd.DataFrame: A DataFrame with distinct values.
        """
        self.df['pages'] = self.df['pages'].replace('', pd.NA)
        return self.df
    
    def distinct_values_from_list(self, col: str) -> pd.DataFrame:
        """
        Gets distinct values from a column containing lists and returns them as a DataFrame.

        Args:
            col (str): The column name to extract distinct values from.

        Returns:
            pd.DataFrame: A DataFrame with distinct values.
        """
        distinct_list = self.distinct_column_values(col)
        list_to_df = pd.DataFrame(distinct_list, columns=[col]).dropna()
        return list_to_df
    
    def distinct_column_values(self, col: str) -> list:
        """
        Gets distinct values from a column containing lists.

        Args:
            col (str): The column name to extract distinct values from.

        Returns:
            list: A list of distinct values.
        """
        self.df[col] = self.df[col].apply(self.make_eval)
        all_values = [item for val in self.df[col].iloc[:] for item in (val if isinstance(val, list) else [val])]
        all_values_set = set(all_values)
        return list(all_values_set)
    
    def make_eval(self, x: str) -> Any:
        """
        Safely evaluates a string to a list or returns the original string if evaluation fails.

        Args:
            x (str): The string to evaluate.

        Returns:
            Any: The evaluated list or the original string.
        """
        try:
            return literal_eval(x)
        except:
            return x

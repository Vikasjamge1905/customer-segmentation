"""
Data Loader Module
Load data from Excel or CSV files with automatic format detection
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Optional


class DataLoader:
    """Handle loading data from various formats."""
    
    EXCEL_EXTENSIONS = ['.xlsx', '.xls']
    CSV_EXTENSIONS = ['.csv']
    
    @staticmethod
    def load_file(file_path: str) -> pd.DataFrame:
        """
        Load data from Excel or CSV file.
        
        Args:
            file_path: Path to Excel or CSV file
            
        Returns:
            Loaded DataFrame
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format not supported
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        extension = file_path.suffix.lower()
        
        print(f"Loading {file_path.name}...")
        
        if extension in DataLoader.EXCEL_EXTENSIONS:
            df = pd.read_excel(file_path)
        elif extension in DataLoader.CSV_EXTENSIONS:
            df = pd.read_csv(file_path)
        else:
            raise ValueError(f"Unsupported file format: {extension}")
        
        print(f"✓ Loaded: {len(df)} rows, {len(df.columns)} columns")
        return df
    
    @staticmethod
    def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize column names for Online Retail dataset.
        
        Args:
            df: DataFrame with raw column names
            
        Returns:
            DataFrame with standardized columns
        """
        # Map various column names to standard names
        column_mapping = {
            'InvoiceNo': 'InvoiceID',
            'InvoiceNumber': 'InvoiceID',
            'Invoice': 'InvoiceID',
            'StockCode': 'ProductCode',
            'Product': 'ProductCode',
            'Description': 'ProductName',
            'ProductName': 'ProductName',
            'Quantity': 'Quantity',
            'Qty': 'Quantity',
            'InvoiceDate': 'InvoiceDate',
            'Date': 'InvoiceDate',
            'UnitPrice': 'UnitPrice',
            'Price': 'UnitPrice',
            'Unit Price': 'UnitPrice',
            'CustomerID': 'CustomerID',
            'Customer': 'CustomerID',
            'Country': 'Country',
        }
        
        # Rename columns
        new_columns = {}
        for old_col in df.columns:
            new_col = column_mapping.get(old_col, old_col)
            new_columns[old_col] = new_col
        
        df = df.rename(columns=new_columns)
        
        return df
    
    @staticmethod
    def prepare_data(file_path: str) -> pd.DataFrame:
        """
        Load and prepare data for analysis.
        
        Args:
            file_path: Path to data file
            
        Returns:
            Cleaned and standardized DataFrame
        """
        # Load file
        df = DataLoader.load_file(file_path)
        
        # Standardize columns
        df = DataLoader.standardize_columns(df)
        
        # Ensure required columns exist
        required_columns = ['InvoiceID', 'CustomerID', 'InvoiceDate', 'Quantity', 'UnitPrice']
        missing = [col for col in required_columns if col not in df.columns]
        
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        
        # Basic cleaning
        print("Cleaning data...")
        original_rows = len(df)
        
        # Remove null CustomerID
        df = df.dropna(subset=['CustomerID'])
        print(f"  Removed null CustomerID: {original_rows - len(df)} rows")
        
        original_rows = len(df)
        
        # Remove negative quantities
        df = df[df['Quantity'] > 0]
        print(f"  Removed negative quantities: {original_rows - len(df)} rows")
        
        original_rows = len(df)
        
        # Convert CustomerID to int
        df['CustomerID'] = df['CustomerID'].astype(int)
        
        # Convert InvoiceDate to datetime
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')
        df = df.dropna(subset=['InvoiceDate'])
        print(f"  Converted dates: {original_rows - len(df)} rows removed")
        
        # Remove duplicates
        original_rows = len(df)
        df = df.drop_duplicates()
        print(f"  Removed duplicates: {original_rows - len(df)} rows")
        
        print(f"✓ Final dataset: {len(df)} rows, {df['CustomerID'].nunique()} unique customers\n")
        
        return df

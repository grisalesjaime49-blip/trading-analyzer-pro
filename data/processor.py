"""
Módulo para procesar datos descargados
"""
import pandas as pd
import numpy as np
from datetime import datetime

class DataProcessor:
    """
    Procesa y limpia datos de precios
    """
    
    @staticmethod
    def clean_data(df):
        """
        Limpia datos: elimina NaN, duplicados, etc.
        
        Args:
            df: DataFrame con datos OHLCV
            
        Returns:
            DataFrame limpio
        """
        # Eliminar duplicados
        df = df[~df.index.duplicated(keep='first')]
        
        # Rellenar NaN con forward fill
        df = df.fillna(method='ffill')
        
        # Eliminar filas con NaN restantes
        df = df.dropna()
        
        return df
    
    @staticmethod
    def remove_outliers(df, column='Close', std_threshold=3):
        """
        Elimina valores atípicos basados en desviación estándar
        
        Args:
            df: DataFrame con datos
            column: Columna a analizar
            std_threshold: Número de desviaciones estándar
            
        Returns:
            DataFrame sin valores atípicos
        """
        mean = df[column].mean()
        std = df[column].std()
        
        mask = (df[column] > mean - std_threshold * std) & \
               (df[column] < mean + std_threshold * std)
        
        return df[mask]
    
    @staticmethod
    def resample_data(df, frequency='D'):
        """
        Remuestrea datos a diferente frecuencia
        
        Args:
            df: DataFrame con datos OHLCV
            frequency: Frecuencia ('D', 'W', 'M', 'H', etc.)
            
        Returns:
            DataFrame remuestreado
        """
        ohlc_dict = {
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum'
        }
        
        return df.resample(frequency).agg(ohlc_dict).dropna()
    
    @staticmethod
    def calculate_returns(df, column='Close'):
        """
        Calcula retornos diarios
        
        Args:
            df: DataFrame con datos
            column: Columna de precios
            
        Returns:
            DataFrame con retornos calculados
        """
        df['Returns'] = df[column].pct_change()
        df['Log_Returns'] = np.log(df[column] / df[column].shift(1))
        
        return df
    
    @staticmethod
    def calculate_volatility(df, window=20):
        """
        Calcula volatilidad histórica
        
        Args:
            df: DataFrame con datos
            window: Ventana para calcular
            
        Returns:
            DataFrame con volatilidad
        """
        if 'Returns' not in df.columns:
            df = DataProcessor.calculate_returns(df)
        
        df['Volatility'] = df['Returns'].rolling(window=window).std() * np.sqrt(252)
        
        return df
    
    @staticmethod
    def normalize_data(df, columns=None):
        """
        Normaliza datos (escala entre 0 y 1)
        
        Args:
            df: DataFrame con datos
            columns: Columnas a normalizar (None = todas numéricas)
            
        Returns:
            DataFrame normalizado
        """
        if columns is None:
            columns = df.select_dtypes(include=['number']).columns
        
        df_norm = df.copy()
        
        for col in columns:
            min_val = df_norm[col].min()
            max_val = df_norm[col].max()
            df_norm[col] = (df_norm[col] - min_val) / (max_val - min_val)
        
        return df_norm
    
    @staticmethod
    def add_time_features(df):
        """
        Agrega características de tiempo
        
        Args:
            df: DataFrame con índice de datetime
            
        Returns:
            DataFrame con características de tiempo
        """
        df['Year'] = df.index.year
        df['Month'] = df.index.month
        df['Day'] = df.index.day
        df['DayOfWeek'] = df.index.dayofweek
        df['Quarter'] = df.index.quarter
        df['DayOfYear'] = df.index.dayofyear
        df['WeekOfYear'] = df.index.isocalendar().week
        
        return df

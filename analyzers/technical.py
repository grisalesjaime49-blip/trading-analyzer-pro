"""
Módulo de indicadores técnicos
"""
import pandas as pd
import numpy as np
from scipy import stats

class TechnicalAnalyzer:
    """
    Calcula indicadores técnicos para análisis de precios
    """
    
    @staticmethod
    def add_sma(df, periods=[20, 50, 200]):
        """
        Agrega Media Móvil Simple (SMA)
        
        Args:
            df: DataFrame con datos OHLCV
            periods: Lista de períodos para calcular
        """
        for period in periods:
            df[f'SMA_{period}'] = df['Close'].rolling(window=period).mean()
        return df
    
    @staticmethod
    def add_ema(df, periods=[12, 26]):
        """
        Agrega Media Móvil Exponencial (EMA)
        
        Args:
            df: DataFrame con datos OHLCV
            periods: Lista de períodos para calcular
        """
        for period in periods:
            df[f'EMA_{period}'] = df['Close'].ewm(span=period, adjust=False).mean()
        return df
    
    @staticmethod
    def add_rsi(df, period=14):
        """
        Agrega Índice de Fuerza Relativa (RSI)
        
        Args:
            df: DataFrame con datos OHLCV
            period: Período para calcular RSI
        """
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        return df
    
    @staticmethod
    def add_macd(df, fast=12, slow=26, signal=9):
        """
        Agrega MACD (Moving Average Convergence Divergence)
        
        Args:
            df: DataFrame con datos OHLCV
            fast: Período rápido
            slow: Período lento
            signal: Período de señal
        """
        ema_fast = df['Close'].ewm(span=fast, adjust=False).mean()
        ema_slow = df['Close'].ewm(span=slow, adjust=False).mean()
        df['MACD'] = ema_fast - ema_slow
        df['MACD_Signal'] = df['MACD'].ewm(span=signal, adjust=False).mean()
        df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']
        return df
    
    @staticmethod
    def add_bollinger_bands(df, period=20, std_dev=2):
        """
        Agrega Bandas de Bollinger
        
        Args:
            df: DataFrame con datos OHLCV
            period: Período para calcular
            std_dev: Número de desviaciones estándar
        """
        sma = df['Close'].rolling(window=period).mean()
        std = df['Close'].rolling(window=period).std()
        df['BB_Upper'] = sma + (std_dev * std)
        df['BB_Middle'] = sma
        df['BB_Lower'] = sma - (std_dev * std)
        df['BB_Width'] = df['BB_Upper'] - df['BB_Lower']
        df['BB_Position'] = (df['Close'] - df['BB_Lower']) / (df['BB_Upper'] - df['BB_Lower'])
        return df
    
    @staticmethod
    def add_stochastic(df, period=14, smooth_k=3, smooth_d=3):
        """
        Agrega Oscilador Estocástico
        
        Args:
            df: DataFrame con datos OHLCV
            period: Período para calcular
            smooth_k: Período de suavizado K
            smooth_d: Período de suavizado D
        """
        low_min = df['Low'].rolling(window=period).min()
        high_max = df['High'].rolling(window=period).max()
        df['Stoch_K'] = 100 * ((df['Close'] - low_min) / (high_max - low_min))
        df['Stoch_D'] = df['Stoch_K'].rolling(window=smooth_d).mean()
        return df
    
    @staticmethod
    def add_atr(df, period=14):
        """
        Agrega Average True Range (ATR)
        
        Args:
            df: DataFrame con datos OHLCV
            period: Período para calcular
        """
        df['TR'] = np.maximum(
            df['High'] - df['Low'],
            np.maximum(
                abs(df['High'] - df['Close'].shift()),
                abs(df['Low'] - df['Close'].shift())
            )
        )
        df['ATR'] = df['TR'].rolling(window=period).mean()
        return df
    
    @staticmethod
    def add_adx(df, period=14):
        """
        Agrega Average Directional Index (ADX)
        
        Args:
            df: DataFrame con datos OHLCV
            period: Período para calcular
        """
        plus_dm = df['High'].diff()
        minus_dm = -df['Low'].diff()
        plus_dm[plus_dm < 0] = 0
        minus_dm[minus_dm < 0] = 0
        
        tr = np.maximum(
            df['High'] - df['Low'],
            np.maximum(
                abs(df['High'] - df['Close'].shift()),
                abs(df['Low'] - df['Close'].shift())
            )
        )
        
        plus_di = 100 * plus_dm.rolling(window=period).mean() / tr.rolling(window=period).mean()
        minus_di = 100 * minus_dm.rolling(window=period).mean() / tr.rolling(window=period).mean()
        
        dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
        df['ADX'] = dx.rolling(window=period).mean()
        
        return df
    
    @staticmethod
    def add_volume_indicators(df):
        """
        Agrega indicadores de volumen
        
        Args:
            df: DataFrame con datos OHLCV
        """
        # On-Balance Volume (OBV)
        df['OBV'] = (np.sign(df['Close'].diff()) * df['Volume']).fillna(0).cumsum()
        
        # Volume Moving Average
        df['Volume_SMA_20'] = df['Volume'].rolling(window=20).mean()
        
        return df


class IndicatorHelper:
    """
    Clase auxiliar para cálculos de indicadores
    """
    
    @staticmethod
    def calculate_all_indicators(df):
        """
        Calcula todos los indicadores técnicos en el DataFrame
        
        Args:
            df: DataFrame con datos OHLCV
            
        Returns:
            DataFrame con todos los indicadores calculados
        """
        analyzer = TechnicalAnalyzer()
        
        df = analyzer.add_sma(df, [20, 50, 200])
        df = analyzer.add_ema(df, [12, 26])
        df = analyzer.add_rsi(df, 14)
        df = analyzer.add_macd(df, 12, 26, 9)
        df = analyzer.add_bollinger_bands(df, 20, 2)
        df = analyzer.add_stochastic(df, 14, 3, 3)
        df = analyzer.add_atr(df, 14)
        df = analyzer.add_adx(df, 14)
        df = analyzer.add_volume_indicators(df)
        
        return df

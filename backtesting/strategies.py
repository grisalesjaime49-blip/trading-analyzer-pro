"""
Estrategias predefinidas de trading
"""
import pandas as pd
import numpy as np
from analyzers.technical import TechnicalAnalyzer

class StrategyBase:
    """
    Clase base para estrategias
    """
    
    def generate_signals(self, df):
        """
        Genera señales de trading
        
        Args:
            df: DataFrame con datos OHLCV
            
        Returns:
            Series con señales (1=BUY, -1=SELL, 0=HOLD)
        """
        raise NotImplementedError


class SimpleMA(StrategyBase):
    """
    Estrategia de cruce de medias móviles simples
    """
    
    def __init__(self, short_period=20, long_period=50):
        self.short_period = short_period
        self.long_period = long_period
    
    def generate_signals(self, df):
        """
        Genera señales basadas en SMA
        """
        analyzer = TechnicalAnalyzer()
        df = analyzer.add_sma(df, [self.short_period, self.long_period])
        
        signals = pd.Series(0, index=df.index)
        
        # Señal de compra: SMA corta cruza por encima de SMA larga
        for i in range(1, len(df)):
            if df[f'SMA_{self.short_period}'].iloc[i] > df[f'SMA_{self.long_period}'].iloc[i] and \
               df[f'SMA_{self.short_period}'].iloc[i-1] <= df[f'SMA_{self.long_period}'].iloc[i-1]:
                signals.iloc[i] = 1
            
            # Señal de venta: SMA corta cruza por debajo de SMA larga
            elif df[f'SMA_{self.short_period}'].iloc[i] < df[f'SMA_{self.long_period}'].iloc[i] and \
                 df[f'SMA_{self.short_period}'].iloc[i-1] >= df[f'SMA_{self.long_period}'].iloc[i-1]:
                signals.iloc[i] = -1
        
        return signals


class RSIStrategy(StrategyBase):
    """
    Estrategia basada en RSI
    """
    
    def __init__(self, period=14, oversold=30, overbought=70):
        self.period = period
        self.oversold = oversold
        self.overbought = overbought
    
    def generate_signals(self, df):
        """
        Genera señales basadas en RSI
        """
        analyzer = TechnicalAnalyzer()
        df = analyzer.add_rsi(df, self.period)
        
        signals = pd.Series(0, index=df.index)
        
        for i in range(1, len(df)):
            # Compra cuando RSI cruza por encima de nivel de sobreventa
            if df['RSI'].iloc[i] > self.oversold and df['RSI'].iloc[i-1] <= self.oversold:
                signals.iloc[i] = 1
            
            # Venta cuando RSI cruza por debajo de nivel de sobrecompra
            elif df['RSI'].iloc[i] < self.overbought and df['RSI'].iloc[i-1] >= self.overbought:
                signals.iloc[i] = -1
        
        return signals


class MACDStrategy(StrategyBase):
    """
    Estrategia basada en MACD
    """
    
    def __init__(self, fast=12, slow=26, signal=9):
        self.fast = fast
        self.slow = slow
        self.signal = signal
    
    def generate_signals(self, df):
        """
        Genera señales basadas en MACD
        """
        analyzer = TechnicalAnalyzer()
        df = analyzer.add_macd(df, self.fast, self.slow, self.signal)
        
        signals = pd.Series(0, index=df.index)
        
        for i in range(1, len(df)):
            # Compra cuando MACD cruza por encima de la línea de señal
            if df['MACD'].iloc[i] > df['MACD_Signal'].iloc[i] and \
               df['MACD'].iloc[i-1] <= df['MACD_Signal'].iloc[i-1]:
                signals.iloc[i] = 1
            
            # Venta cuando MACD cruza por debajo de la línea de señal
            elif df['MACD'].iloc[i] < df['MACD_Signal'].iloc[i] and \
                 df['MACD'].iloc[i-1] >= df['MACD_Signal'].iloc[i-1]:
                signals.iloc[i] = -1
        
        return signals


class CombinedStrategy(StrategyBase):
    """
    Estrategia que combina múltiples indicadores
    """
    
    def __init__(self):
        self.sma_strategy = SimpleMA(20, 50)
        self.rsi_strategy = RSIStrategy(14, 30, 70)
        self.macd_strategy = MACDStrategy(12, 26, 9)
    
    def generate_signals(self, df):
        """
        Genera señales combinadas
        """
        sma_signals = self.sma_strategy.generate_signals(df)
        rsi_signals = self.rsi_strategy.generate_signals(df)
        macd_signals = self.macd_strategy.generate_signals(df)
        
        # Señal si al menos 2 estrategias concuerdan
        combined = pd.Series(0, index=df.index)
        
        for i in range(len(df)):
            total = sma_signals.iloc[i] + rsi_signals.iloc[i] + macd_signals.iloc[i]
            
            if total >= 2:
                combined.iloc[i] = 1
            elif total <= -2:
                combined.iloc[i] = -1
        
        return combined

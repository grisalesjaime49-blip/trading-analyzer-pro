"""
Módulo de análisis de patrones de velas
"""
import pandas as pd
import numpy as np

class PatternAnalyzer:
    """
    Identifica patrones de velas japonesas
    """
    
    @staticmethod
    def identify_patterns(df):
        """
        Identifica patrones en el DataFrame
        
        Args:
            df: DataFrame con datos OHLCV
            
        Returns:
            dict con patrones identificados
        """
        patterns = {}
        patterns['doji'] = PatternAnalyzer.detect_doji(df)
        patterns['hammer'] = PatternAnalyzer.detect_hammer(df)
        patterns['shooting_star'] = PatternAnalyzer.detect_shooting_star(df)
        patterns['engulfing'] = PatternAnalyzer.detect_engulfing(df)
        patterns['three_line_strike'] = PatternAnalyzer.detect_three_line_strike(df)
        
        return patterns
    
    @staticmethod
    def detect_doji(df):
        """
        Detecta patrón Doji
        """
        if len(df) < 1:
            return False
        
        last = df.iloc[-1]
        body = abs(last['Close'] - last['Open'])
        total_range = last['High'] - last['Low']
        
        return body / total_range < 0.1 if total_range > 0 else False
    
    @staticmethod
    def detect_hammer(df):
        """
        Detecta patrón Martillo
        """
        if len(df) < 2:
            return False
        
        last = df.iloc[-1]
        body = abs(last['Close'] - last['Open'])
        lower_shadow = min(last['Close'], last['Open']) - last['Low']
        upper_shadow = last['High'] - max(last['Close'], last['Open'])
        total_range = last['High'] - last['Low']
        
        return (lower_shadow > 2 * body and upper_shadow < body and total_range > 0)
    
    @staticmethod
    def detect_shooting_star(df):
        """
        Detecta patrón Estrella Fugaz
        """
        if len(df) < 2:
            return False
        
        last = df.iloc[-1]
        body = abs(last['Close'] - last['Open'])
        upper_shadow = last['High'] - max(last['Close'], last['Open'])
        lower_shadow = min(last['Close'], last['Open']) - last['Low']
        total_range = last['High'] - last['Low']
        
        return (upper_shadow > 2 * body and lower_shadow < body and total_range > 0)
    
    @staticmethod
    def detect_engulfing(df):
        """
        Detecta patrón Engulfing
        """
        if len(df) < 2:
            return False
        
        curr = df.iloc[-1]
        prev = df.iloc[-2]
        
        curr_body = abs(curr['Close'] - curr['Open'])
        prev_body = abs(prev['Close'] - prev['Open'])
        
        bullish = (curr['Open'] < prev['Close'] and curr['Close'] > prev['Open'] and curr_body > prev_body)
        bearish = (curr['Open'] > prev['Close'] and curr['Close'] < prev['Open'] and curr_body > prev_body)
        
        return bullish or bearish
    
    @staticmethod
    def detect_three_line_strike(df):
        """
        Detecta patrón Three Line Strike
        """
        if len(df) < 3:
            return False
        
        # Simplificado: detecta 3 velas consecutivas en una dirección
        last_three = df.iloc[-3:]
        
        up_trend = all(last_three['Close'].iloc[i] > last_three['Close'].iloc[i-1] for i in range(1, 3))
        down_trend = all(last_three['Close'].iloc[i] < last_three['Close'].iloc[i-1] for i in range(1, 3))
        
        return up_trend or down_trend

"""
Módulo generador de señales de trading
"""
import pandas as pd
import numpy as np
from config import (
    RSI_BUY_THRESHOLD, RSI_SELL_THRESHOLD,
    CONFIDENCE_STRONG, CONFIDENCE_MODERATE, CONFIDENCE_WEAK
)

class SignalGenerator:
    """
    Genera señales de compra y venta basadas en indicadores técnicos
    """
    
    def __init__(self):
        self.signal_history = []
    
    def generate(self, df):
        """
        Genera señal basada en múltiples indicadores
        
        Args:
            df: DataFrame con indicadores calculados
            
        Returns:
            dict con señal, confianza y detalles
        """
        if len(df) < 2:
            return {'signal': 'HOLD', 'confidence': 0, 'reason': 'Datos insuficientes'}
        
        last_row = df.iloc[-1]
        prev_row = df.iloc[-2]
        
        signals = {}
        signals['sma'] = self._analyze_sma(df)
        signals['rsi'] = self._analyze_rsi(last_row)
        signals['macd'] = self._analyze_macd(df)
        signals['bollinger'] = self._analyze_bollinger(last_row)
        signals['stochastic'] = self._analyze_stochastic(last_row)
        
        # Combinar señales
        final_signal = self._combine_signals(signals)
        
        return {
            'signal': final_signal['signal'],
            'confidence': final_signal['confidence'],
            'details': signals,
            'price': last_row['Close'],
            'timestamp': str(df.index[-1])
        }
    
    def _analyze_sma(self, df):
        """
        Analiza cruce de medias móviles
        """
        last = df.iloc[-1]
        
        if last['Close'] > last.get('SMA_20', 0) > last.get('SMA_50', 0):
            return {'signal': 'BUY', 'strength': 0.8}
        elif last['Close'] < last.get('SMA_20', 0) < last.get('SMA_50', 0):
            return {'signal': 'SELL', 'strength': 0.8}
        else:
            return {'signal': 'HOLD', 'strength': 0.3}
    
    def _analyze_rsi(self, row):
        """
        Analiza RSI
        """
        rsi = row.get('RSI', 50)
        
        if rsi < RSI_BUY_THRESHOLD:
            return {'signal': 'BUY', 'strength': 0.7, 'rsi': rsi}
        elif rsi > RSI_SELL_THRESHOLD:
            return {'signal': 'SELL', 'strength': 0.7, 'rsi': rsi}
        else:
            return {'signal': 'HOLD', 'strength': 0.3, 'rsi': rsi}
    
    def _analyze_macd(self, df):
        """
        Analiza MACD
        """
        if len(df) < 2:
            return {'signal': 'HOLD', 'strength': 0.3}
        
        last = df.iloc[-1]
        prev = df.iloc[-2]
        
        if prev.get('MACD', 0) < prev.get('MACD_Signal', 0) and \
           last.get('MACD', 0) > last.get('MACD_Signal', 0):
            return {'signal': 'BUY', 'strength': 0.8}
        elif prev.get('MACD', 0) > prev.get('MACD_Signal', 0) and \
             last.get('MACD', 0) < last.get('MACD_Signal', 0):
            return {'signal': 'SELL', 'strength': 0.8}
        else:
            return {'signal': 'HOLD', 'strength': 0.3}
    
    def _analyze_bollinger(self, row):
        """
        Analiza Bandas de Bollinger
        """
        price = row.get('Close', 0)
        upper = row.get('BB_Upper', 0)
        lower = row.get('BB_Lower', 0)
        
        if price < lower:
            return {'signal': 'BUY', 'strength': 0.6}
        elif price > upper:
            return {'signal': 'SELL', 'strength': 0.6}
        else:
            return {'signal': 'HOLD', 'strength': 0.3}
    
    def _analyze_stochastic(self, row):
        """
        Analiza Oscilador Estocástico
        """
        stoch_k = row.get('Stoch_K', 50)
        
        if stoch_k < 20:
            return {'signal': 'BUY', 'strength': 0.6, 'stoch_k': stoch_k}
        elif stoch_k > 80:
            return {'signal': 'SELL', 'strength': 0.6, 'stoch_k': stoch_k}
        else:
            return {'signal': 'HOLD', 'strength': 0.3, 'stoch_k': stoch_k}
    
    def _combine_signals(self, signals):
        """
        Combina múltiples señales
        """
        buy_strength = sum(1 for s in signals.values() if s['signal'] == 'BUY')
        sell_strength = sum(1 for s in signals.values() if s['signal'] == 'SELL')
        avg_strength = sum(s['strength'] for s in signals.values()) / len(signals)
        
        if buy_strength > sell_strength:
            signal = 'BUY'
            confidence = min(100, int(buy_strength * 25 + avg_strength * 100))
        elif sell_strength > buy_strength:
            signal = 'SELL'
            confidence = min(100, int(sell_strength * 25 + avg_strength * 100))
        else:
            signal = 'HOLD'
            confidence = 50
        
        return {'signal': signal, 'confidence': confidence}
    
    def get_signal_description(self, signal):
        """
        Obtiene descripción legible de la señal
        """
        descriptions = {
            'BUY': '🟢 COMPRAR - Condiciones alcistas',
            'SELL': '🔴 VENDER - Condiciones bajistas',
            'HOLD': '⚪ MANTENER - Sin señal clara'
        }
        return descriptions.get(signal, 'Desconocido')

"""
Módulo para descargar datos de precios
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
from config import DATA_PATH, DEFAULT_PERIOD, DEFAULT_INTERVAL

class DataDownloader:
    """
    Descarga datos de precios de YFinance
    """
    
    def __init__(self):
        self.cache_dir = DATA_PATH
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def fetch(self, symbol, period='1y', interval='1d', progress=False):
        """
        Descarga datos históricos de un símbolo
        
        Args:
            symbol: Símbolo del activo (ej: 'BTC-USD')
            period: Período de datos ('1d', '5d', '1mo', '3mo', '6mo', '1y', '5y', '10y', 'max')
            interval: Intervalo de tiempo ('1m', '5m', '15m', '30m', '60m', '1d', '1wk', '1mo')
            progress: Mostrar barra de progreso
            
        Returns:
            DataFrame con datos OHLCV
        """
        try:
            print(f"📥 Descargando datos para {symbol} (período: {period})...")
            
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period, interval=interval, progress=progress)
            
            if df.empty:
                print(f"❌ No se encontraron datos para {symbol}")
                return None
            
            # Limpiar datos
            df = df.dropna()
            
            print(f"✅ Descargados {len(df)} registros para {symbol}")
            return df
            
        except Exception as e:
            print(f"❌ Error al descargar datos: {str(e)}")
            return None
    
    def fetch_multiple(self, symbols, period='1y', interval='1d'):
        """
        Descarga datos para múltiples símbolos
        
        Args:
            symbols: Lista de símbolos
            period: Período de datos
            interval: Intervalo de tiempo
            
        Returns:
            dict con DataFrames por símbolo
        """
        data = {}
        for symbol in symbols:
            data[symbol] = self.fetch(symbol, period, interval)
        return data
    
    def fetch_live_data(self, symbol):
        """
        Obtiene datos en tiempo real (última vela cerrada)
        
        Args:
            symbol: Símbolo del activo
            
        Returns:
            dict con datos actuales
        """
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period='1d', interval='1d')
            
            if data.empty:
                return None
            
            last = data.iloc[-1]
            
            return {
                'symbol': symbol,
                'open': float(last['Open']),
                'high': float(last['High']),
                'low': float(last['Low']),
                'close': float(last['Close']),
                'volume': float(last['Volume']),
                'timestamp': str(data.index[-1])
            }
            
        except Exception as e:
            print(f"❌ Error al obtener datos en vivo: {str(e)}")
            return None
    
    def get_info(self, symbol):
        """
        Obtiene información sobre un símbolo
        
        Args:
            symbol: Símbolo del activo
            
        Returns:
            dict con información
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return {
                'symbol': symbol,
                'name': info.get('longName', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'market_cap': info.get('marketCap', 'N/A'),
                'pe_ratio': info.get('trailingPE', 'N/A'),
                'dividend_yield': info.get('dividendYield', 'N/A')
            }
            
        except Exception as e:
            print(f"❌ Error al obtener información: {str(e)}")
            return None

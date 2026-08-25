"""
Ejemplo 1: Análisis Técnico Básico

Este script descarga datos y calcula indicadores técnicos.

Para ejecutar:
    python examples/basic_analysis.py
"""

from data.downloader import DataDownloader
from data.processor import DataProcessor
from analyzers.technical import IndicatorHelper
from analyzers.signals import SignalGenerator
import pandas as pd

# Configuración
SYMBOL = 'BTC-USD'  # Puedes cambiar por: ETH-USD, AAPL, GOOGL, etc.
PERIOD = '3mo'  # 1d, 5d, 1mo, 3mo, 6mo, 1y, 5y, 10y, max
INTERVAL = '1d'  # 1m, 5m, 15m, 30m, 60m, 1d, 1wk, 1mo

def main():
    print("\n" + "="*60)
    print("📊 ANÁLISIS TÉCNICO BÁSICO")
    print("="*60)
    
    # 1. Descargar datos
    print(f"\n📥 Descargando datos para {SYMBOL}...")
    downloader = DataDownloader()
    df = downloader.fetch(SYMBOL, period=PERIOD, interval=INTERVAL)
    
    if df is None or df.empty:
        print("❌ Error: No se pudieron descargar los datos")
        return
    
    # 2. Limpiar datos
    print("🚧 Limpiando datos...")
    processor = DataProcessor()
    df = processor.clean_data(df)
    
    # 3. Calcular indicadores
    print("🔨 Calculando indicadores técnicos...")
    df = IndicatorHelper.calculate_all_indicators(df)
    
    # 4. Mostrar últimos datos
    print(f"\n📋 Últimos 5 registros:")
    print("-" * 60)
    
    # Seleccionar columnas importantes
    cols_to_show = ['Open', 'High', 'Low', 'Close', 'Volume', 
                    'SMA_20', 'SMA_50', 'RSI', 'MACD']
    display_cols = [col for col in cols_to_show if col in df.columns]
    
    print(df[display_cols].tail().to_string())
    
    # 5. Mostrar últimas velas con indicadores
    print(f"\n📊 Última vela ({df.index[-1].strftime('%Y-%m-%d')}):")
    print("-" * 60)
    last = df.iloc[-1]
    
    print(f"Precio de Cierre:    ${last['Close']:.2f}")
    print(f"Máximo:              ${last['High']:.2f}")
    print(f"Mínimo:              ${last['Low']:.2f}")
    print(f"Volumen:             {int(last['Volume']):,}")
    print(f"\nIndicadores:")
    print(f"  SMA 20:            {last.get('SMA_20', 0):.2f}")
    print(f"  SMA 50:            {last.get('SMA_50', 0):.2f}")
    print(f"  SMA 200:           {last.get('SMA_200', 0):.2f}")
    print(f"  RSI:               {last.get('RSI', 0):.2f}")
    print(f"  MACD:              {last.get('MACD', 0):.4f}")
    print(f"  MACD Signal:       {last.get('MACD_Signal', 0):.4f}")
    print(f"  Bandas de Bollinger:")
    print(f"    Superior:        {last.get('BB_Upper', 0):.2f}")
    print(f"    Inferior:        {last.get('BB_Lower', 0):.2f}")
    print(f"  Estocástico K:     {last.get('Stoch_K', 0):.2f}")
    print(f"  ATR:               {last.get('ATR', 0):.2f}")
    
    # 6. Generar señales
    print(f"\n📢 Generando señales de trading...")
    signal_gen = SignalGenerator()
    signals = signal_gen.generate(df)
    
    print("-" * 60)
    print(f"Señal:               {signals['signal']}")
    print(f"Confianza:           {signals['confidence']}%")
    print(f"Descripción:        {signal_gen.get_signal_description(signals['signal'])}")
    print(f"Precio Actual:       ${signals['price']:.2f}")
    
    # 7. Detalles de señales
    print(f"\n📝 Detalles por indicador:")
    print("-" * 60)
    for indicador, dato in signals['details'].items():
        print(f"{indicador:15} | Señal: {dato['signal']:5} | Fuerza: {dato['strength']:.2f}")
    
    print("\n" + "="*60)
    print("✅ Análisis completado")
    print("="*60 + "\n")

if __name__ == '__main__':
    main()

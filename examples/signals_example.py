"""
Ejemplo 3: Generador de Señales en Tiempo Real

Este script genera señales de trading actuales.

Para ejecutar:
    python examples/signals_example.py
"""

from data.downloader import DataDownloader
from data.processor import DataProcessor
from analyzers.technical import IndicatorHelper
from analyzers.signals import SignalGenerator
import time
from datetime import datetime

# Configuración
SYMBOLS = ['BTC-USD', 'ETH-USD', 'AAPL', 'GOOGL', 'MSFT']
PERIOD = '3mo'
INTERVAL = '1d'

def analyze_symbol(symbol):
    """
    Analiza un símbolo y genera señal
    """
    try:
        # Descargar datos
        downloader = DataDownloader()
        df = downloader.fetch(symbol, period=PERIOD, interval=INTERVAL)
        
        if df is None or df.empty:
            return None
        
        # Procesar datos
        processor = DataProcessor()
        df = processor.clean_data(df)
        
        # Calcular indicadores
        df = IndicatorHelper.calculate_all_indicators(df)
        
        # Generar señales
        signal_gen = SignalGenerator()
        signals = signal_gen.generate(df)
        
        # Últimos datos
        last = df.iloc[-1]
        
        return {
            'symbol': symbol,
            'price': signals['price'],
            'signal': signals['signal'],
            'confidence': signals['confidence'],
            'rsi': last.get('RSI', 0),
            'macd': last.get('MACD', 0),
            'description': signal_gen.get_signal_description(signals['signal'])
        }
    
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        return None

def main():
    print("\n" + "="*80)
    print("📢 GENERADOR DE SEÑALES DE TRADING EN TIEMPO REAL")
    print("="*80)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Símbolos a analizar: {', '.join(SYMBOLS)}")
    print("="*80)
    
    # Analizar cada símbolo
    results = []
    
    for symbol in SYMBOLS:
        print(f"\n🔍 Analizando {symbol}...")
        result = analyze_symbol(symbol)
        
        if result:
            results.append(result)
            print(f"  ✅ Completado")
        else:
            print(f"  ❌ No se pudo analizar")
    
    # Mostrar resultados
    print("\n" + "="*80)
    print("RESULTADOS")
    print("="*80)
    
    if not results:
        print("❌ No hay resultados para mostrar")
        return
    
    # Tabla de resultados
    print(f"\n{'Símbolo':<12} {'Precio':>12} {'RSI':>8} {'Señal':>8} {'Conf.':>6} {'Descripción':<40}")
    print("-" * 80)
    
    for result in sorted(results, key=lambda x: x['confidence'], reverse=True):
        emoji = "🟢" if result['signal'] == 'BUY' else "🔴" if result['signal'] == 'SELL' else "⚪"
        
        print(f"{result['symbol']:<12} ${result['price']:>11.2f} {result['rsi']:>8.2f} "
              f"{emoji} {result['signal']:>5} {result['confidence']:>5}% {result['description']:<40}")
    
    # Señales más fuertes
    print("\n" + "="*80)
    print("🌟 MEJORES OPORTUNIDADES (Mayor confianza)")
    print("="*80)
    
    buy_signals = [r for r in results if r['signal'] == 'BUY']
    sell_signals = [r for r in results if r['signal'] == 'SELL']
    
    if buy_signals:
        print("\n🟢 SEÑALES DE COMPRA:")
        for signal in sorted(buy_signals, key=lambda x: x['confidence'], reverse=True):
            print(f"  {signal['symbol']:<10} - Confianza: {signal['confidence']}%")
    else:
        print("\n🟢 SEÑALES DE COMPRA: Ninguna")
    
    if sell_signals:
        print("\n🔴 SEÑALES DE VENTA:")
        for signal in sorted(sell_signals, key=lambda x: x['confidence'], reverse=True):
            print(f"  {signal['symbol']:<10} - Confianza: {signal['confidence']}%")
    else:
        print("\n🔴 SEÑALES DE VENTA: Ninguna")
    
    print("\n" + "="*80)
    print("✅ Análisis completado")
    print("="*80 + "\n")
    
    print("⚠️  DISCLAIMER: Estos análisis son solo educativos.")
    print("   Consulte un asesor financiero antes de tomar decisiones de trading.\n")

if __name__ == '__main__':
    main()

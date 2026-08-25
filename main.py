"""
Archivo principal del Analizador de Trading

Este es el punto de entrada principal del programa.

Usos:
  1. Para análisis básico:
     python main.py --analyze BTC-USD
  
  2. Para generar señales:
     python main.py --signals BTC-USD ETH-USD
  
  3. Para iniciar la API:
     python main.py --api
  
  4. Para ayuda:
     python main.py --help
"""

import argparse
import sys
from data.downloader import DataDownloader
from data.processor import DataProcessor
from analyzers.technical import IndicatorHelper
from analyzers.signals import SignalGenerator
from api.server import create_app
from config import API_HOST, API_PORT, API_DEBUG

def analyze_symbol(symbol, period='1y', interval='1d'):
    """
    Analiza un símbolo
    """
    print(f"\n📋 Analizando {symbol}...")
    
    try:
        downloader = DataDownloader()
        df = downloader.fetch(symbol, period=period, interval=interval)
        
        if df is None or df.empty:
            print("❌ Error: No se pudieron descargar datos")
            return
        
        processor = DataProcessor()
        df = processor.clean_data(df)
        
        df = IndicatorHelper.calculate_all_indicators(df)
        
        signal_gen = SignalGenerator()
        signals = signal_gen.generate(df)
        
        last = df.iloc[-1]
        
        print(f"\
        📊 {symbol} - Última Vela:")
        print(f"  Fecha: {df.index[-1].strftime('%Y-%m-%d')}")
        print(f"  Precio: ${last['Close']:.2f}")
        print(f"  RSI: {last.get('RSI', 0):.2f}")
        print(f"  MACD: {last.get('MACD', 0):.4f}")
        print(f"\n  Señal: {signals['signal']} ({signals['confidence']}% confianza)")
        print(f"  Descripción: {signal_gen.get_signal_description(signals['signal'])}")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def generate_signals(symbols, period='3mo', interval='1d'):
    """
    Genera señales para múltiples símbolos
    """
    print(f"\n📢 Generando señales...")
    print(f"{'Símbolo':<12} {'Señal':>8} {'Confianza':>10} {'Precio':>12}")
    print("-" * 50)
    
    downloader = DataDownloader()
    processor = DataProcessor()
    signal_gen = SignalGenerator()
    
    for symbol in symbols:
        try:
            df = downloader.fetch(symbol, period=period, interval=interval)
            if df is None or df.empty:
                continue
            
            df = processor.clean_data(df)
            df = IndicatorHelper.calculate_all_indicators(df)
            signals = signal_gen.generate(df)
            
            emoji = "🟢" if signals['signal'] == 'BUY' else "🔴" if signals['signal'] == 'SELL' else "⚪"
            
            print(f"{symbol:<12} {emoji} {signals['signal']:>6} {signals['confidence']:>9}% ${signals['price']:>11.2f}")
        
        except Exception as e:
            print(f"{symbol:<12} {'ERROR':>14}")

def start_api():
    """
    Inicia el servidor API
    """
    print(f"\n🚀 Iniciando API en http://{API_HOST}:{API_PORT}")
    print(f"Documentación: http://localhost:{API_PORT}")
    print("⚠️  Presiona Ctrl+C para detener\n")
    
    app = create_app()
    app.run(host=API_HOST, port=API_PORT, debug=API_DEBUG)

def main():
    parser = argparse.ArgumentParser(
        description='Trading Analyzer Pro - Análisis Técnico y Trading',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  # Analizar un símbolo
  python main.py --analyze BTC-USD
  
  # Generar señales para varios símbolos
  python main.py --signals BTC-USD ETH-USD AAPL GOOGL
  
  # Iniciar API REST
  python main.py --api
  
  # Con período personalizado
  python main.py --analyze BTC-USD --period 6mo --interval 1h
        """
    )
    
    parser.add_argument('--analyze', type=str, help='Analiza un símbolo')
    parser.add_argument('--signals', nargs='+', help='Genera señales para símbolos')
    parser.add_argument('--api', action='store_true', help='Inicia servidor API')
    parser.add_argument('--period', type=str, default='1y', help='Período de datos (default: 1y)')
    parser.add_argument('--interval', type=str, default='1d', help='Intervalo de tiempo (default: 1d)')
    
    args = parser.parse_args()
    
    if args.analyze:
        analyze_symbol(args.analyze, args.period, args.interval)
    
    elif args.signals:
        generate_signals(args.signals, args.period, args.interval)
    
    elif args.api:
        start_api()
    
    else:
        parser.print_help()

if __name__ == '__main__':
    main()

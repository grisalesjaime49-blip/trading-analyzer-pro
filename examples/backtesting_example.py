"""
Ejemplo 2: Backtesting de Estrategias

Este script ejecuta backtests de diferentes estrategias.

Para ejecutar:
    python examples/backtesting_example.py
"""

from data.downloader import DataDownloader
from data.processor import DataProcessor
from analyzers.technical import IndicatorHelper
from backtesting.engine import BacktestEngine
from backtesting.strategies import SimpleMA, RSIStrategy, MACDStrategy, CombinedStrategy
from backtesting.performance import PerformanceAnalyzer
import pandas as pd

# Configuración
SYMBOL = 'BTC-USD'
PERIOD = '1y'  # Período para backtesting
INTERVAL = '1d'
INITIAL_CAPITAL = 10000  # $10,000 USD

def run_backtest(symbol, strategy_name, strategy, period=PERIOD, initial_capital=INITIAL_CAPITAL):
    """
    Ejecuta un backtest para una estrategia
    """
    print(f"\n🔄 Ejecutando backtest con estrategia {strategy_name}...")
    
    try:
        # Descargar y procesar datos
        downloader = DataDownloader()
        df = downloader.fetch(symbol, period=period, interval=INTERVAL)
        
        if df is None or df.empty:
            print("❌ Error al descargar datos")
            return None
        
        processor = DataProcessor()
        df = processor.clean_data(df)
        
        # Calcular indicadores
        df = IndicatorHelper.calculate_all_indicators(df)
        
        # Generar señales
        signals = strategy.generate_signals(df)
        
        # Ejecutar backtest
        engine = BacktestEngine(initial_capital=initial_capital)
        metrics = engine.run(df, signals)
        
        # Imprimir resultados
        analyzer = PerformanceAnalyzer()
        print(f"\n✅ Resultados para {strategy_name}:")
        analyzer.print_report(metrics)
        
        return metrics, engine.get_trades()
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None, []

def main():
    print("\n" + "="*60)
    print("📈 BACKTESTING DE ESTRATEGIAS")
    print("="*60)
    print(f"Símbolo: {SYMBOL}")
    print(f"Período: {PERIOD}")
    print(f"Capital Inicial: ${INITIAL_CAPITAL:,}")
    print("="*60)
    
    # Estrategias a probar
    strategies = {
        'SMA (Medias Móviles)': SimpleMA(20, 50),
        'RSI (Fuerza Relativa)': RSIStrategy(14, 30, 70),
        'MACD': MACDStrategy(12, 26, 9),
        'COMBINADA': CombinedStrategy()
    }
    
    # Ejecutar backtests
    results = {}
    for strategy_name, strategy in strategies.items():
        metrics, trades = run_backtest(SYMBOL, strategy_name, strategy)
        if metrics:
            results[strategy_name] = metrics
    
    # Comparar resultados
    print("\n" + "="*60)
    print("📁 COMPARACIÓN DE ESTRATEGIAS")
    print("="*60)
    print(f"{'Estrategia':<25} {'Retorno %':>12} {'Win Rate':>10} {'Sharpe':>8} {'Drawdown':>10}")
    print("-"*65)
    
    for name, metrics in results.items():
        retorno = metrics.get('total_return', 0)
        win_rate = metrics.get('win_rate', 0)
        sharpe = metrics.get('sharpe_ratio', 0)
        drawdown = metrics.get('max_drawdown', 0)
        
        print(f"{name:<25} {retorno:>11.2f}% {win_rate:>9.2f}% {sharpe:>8.2f} {drawdown:>9.2f}%")
    
    print("="*60)
    print("✅ Backtesting completado")
    print("="*60 + "\n")

if __name__ == '__main__':
    main()

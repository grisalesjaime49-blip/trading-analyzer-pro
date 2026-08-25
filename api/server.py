"""
Servidor REST con Flask
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import traceback
from data.downloader import DataDownloader
from data.processor import DataProcessor
from analyzers.technical import TechnicalAnalyzer, IndicatorHelper
from analyzers.signals import SignalGenerator
from backtesting.engine import BacktestEngine
from backtesting.strategies import SimpleMA, RSIStrategy, MACDStrategy, CombinedStrategy
from backtesting.performance import PerformanceAnalyzer
from config import API_HOST, API_PORT, API_DEBUG

def create_app():
    """
    Crea la aplicación Flask
    """
    app = Flask(__name__)
    CORS(app)
    
    # Instancias globales
    downloader = DataDownloader()
    processor = DataProcessor()
    analyzer = TechnicalAnalyzer()
    signal_gen = SignalGenerator()
    
    @app.route('/', methods=['GET'])
    def index():
        """
        Endpoint principal
        """
        return jsonify({
            'name': 'Trading Analyzer Pro',
            'version': '1.0.0',
            'status': 'online',
            'endpoints': {
                'GET /analyze/<symbol>': 'Analiza un símbolo',
                'GET /signals/<symbol>': 'Obtiene señales de trading',
                'GET /info/<symbol>': 'Obtiene información del activo',
                'POST /backtest': 'Ejecuta un backtest',
                'GET /health': 'Estado del servidor'
            }
        })
    
    @app.route('/health', methods=['GET'])
    def health():
        """
        Verifica estado del servidor
        """
        return jsonify({'status': 'healthy', 'message': 'Servidor en línea'})
    
    @app.route('/analyze/<symbol>', methods=['GET'])
    def analyze(symbol):
        """
        Analiza un símbolo y retorna indicadores técnicos
        
        Query params:
            period: Período de datos (1d, 5d, 1mo, 3mo, 6mo, 1y, 5y, 10y, max)
            interval: Intervalo (1m, 5m, 15m, 30m, 60m, 1d, 1wk, 1mo)
        """
        try:
            period = request.args.get('period', '1y')
            interval = request.args.get('interval', '1d')
            
            # Descargar datos
            df = downloader.fetch(symbol, period=period, interval=interval)
            if df is None or df.empty:
                return jsonify({'error': 'No se encontraron datos'}), 404
            
            # Limpiar datos
            df = processor.clean_data(df)
            
            # Calcular indicadores
            df = IndicatorHelper.calculate_all_indicators(df)
            
            # Última fila
            last = df.iloc[-1]
            
            return jsonify({
                'symbol': symbol,
                'timestamp': str(df.index[-1]),
                'data': {
                    'open': float(last['Open']),
                    'high': float(last['High']),
                    'low': float(last['Low']),
                    'close': float(last['Close']),
                    'volume': float(last['Volume']),
                    'sma_20': float(last.get('SMA_20', 0)),
                    'sma_50': float(last.get('SMA_50', 0)),
                    'sma_200': float(last.get('SMA_200', 0)),
                    'ema_12': float(last.get('EMA_12', 0)),
                    'ema_26': float(last.get('EMA_26', 0)),
                    'rsi': float(last.get('RSI', 0)),
                    'macd': float(last.get('MACD', 0)),
                    'macd_signal': float(last.get('MACD_Signal', 0)),
                    'bb_upper': float(last.get('BB_Upper', 0)),
                    'bb_middle': float(last.get('BB_Middle', 0)),
                    'bb_lower': float(last.get('BB_Lower', 0)),
                    'stoch_k': float(last.get('Stoch_K', 0)),
                    'atr': float(last.get('ATR', 0))
                }
            })
        
        except Exception as e:
            return jsonify({'error': str(e), 'trace': traceback.format_exc()}), 500
    
    @app.route('/signals/<symbol>', methods=['GET'])
    def signals(symbol):
        """
        Genera señales de trading para un símbolo
        
        Query params:
            period: Período de datos
            interval: Intervalo
        """
        try:
            period = request.args.get('period', '3mo')
            interval = request.args.get('interval', '1d')
            
            # Descargar datos
            df = downloader.fetch(symbol, period=period, interval=interval)
            if df is None or df.empty:
                return jsonify({'error': 'No se encontraron datos'}), 404
            
            # Limpiar datos
            df = processor.clean_data(df)
            
            # Calcular indicadores
            df = IndicatorHelper.calculate_all_indicators(df)
            
            # Generar señales
            signal_result = signal_gen.generate(df)
            
            return jsonify({
                'symbol': symbol,
                'timestamp': signal_result['timestamp'],
                'signal': signal_result['signal'],
                'confidence': signal_result['confidence'],
                'price': signal_result['price'],
                'description': signal_gen.get_signal_description(signal_result['signal']),
                'details': signal_result['details']
            })
        
        except Exception as e:
            return jsonify({'error': str(e), 'trace': traceback.format_exc()}), 500
    
    @app.route('/info/<symbol>', methods=['GET'])
    def info(symbol):
        """
        Obtiene información sobre un símbolo
        """
        try:
            info = downloader.get_info(symbol)
            if info is None:
                return jsonify({'error': 'No se encontró información'}), 404
            
            return jsonify(info)
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/backtest', methods=['POST'])
    def backtest():
        """
        Ejecuta un backtest
        
        Body JSON:
        {
            "symbol": "BTC-USD",
            "strategy": "SMA",  # SMA, RSI, MACD, COMBINED
            "period": "1y",
            "interval": "1d",
            "initial_capital": 10000
        }
        """
        try:
            data = request.get_json()
            
            symbol = data.get('symbol', 'BTC-USD')
            strategy = data.get('strategy', 'SMA')
            period = data.get('period', '1y')
            interval = data.get('interval', '1d')
            initial_capital = data.get('initial_capital', 10000)
            
            # Descargar datos
            df = downloader.fetch(symbol, period=period, interval=interval)
            if df is None or df.empty:
                return jsonify({'error': 'No se encontraron datos'}), 404
            
            # Limpiar datos
            df = processor.clean_data(df)
            
            # Calcular indicadores
            df = IndicatorHelper.calculate_all_indicators(df)
            
            # Seleccionar estrategia
            strategies = {
                'SMA': SimpleMA(20, 50),
                'RSI': RSIStrategy(14, 30, 70),
                'MACD': MACDStrategy(12, 26, 9),
                'COMBINED': CombinedStrategy()
            }
            
            selected_strategy = strategies.get(strategy, SimpleMA(20, 50))
            signals = selected_strategy.generate_signals(df)
            
            # Ejecutar backtest
            engine = BacktestEngine(initial_capital=initial_capital)
            metrics = engine.run(df, signals)
            
            return jsonify({
                'symbol': symbol,
                'strategy': strategy,
                'period': period,
                'metrics': metrics,
                'trades': engine.get_trades()[:10]  # Últimos 10 trades
            })
        
        except Exception as e:
            return jsonify({'error': str(e), 'trace': traceback.format_exc()}), 500
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint no encontrado'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Error interno del servidor'}), 500
    
    return app


if __name__ == '__main__':
    app = create_app()
    print(f"\n🚀 Iniciando API en http://{API_HOST}:{API_PORT}")
    print(f"Documentación: http://localhost:{API_PORT}")
    app.run(host=API_HOST, port=API_PORT, debug=API_DEBUG)

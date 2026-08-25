"""
Archivo de configuración global para el analizador de trading
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ==================== CONFIGURACIÓN GENERAL ====================
APP_NAME = "Trading Analyzer Pro"
APP_VERSION = "1.0.0"
DEBUG = True
LOG_LEVEL = "INFO"

# ==================== SÍMBOLOS A ANALIZAR ====================
SYMBOLS = ['BTC-USD', 'ETH-USD', 'AAPL', 'GOOGL', 'MSFT']
DEFAULT_SYMBOL = 'BTC-USD'

# ==================== PERÍODOS DE DATOS ====================
DEFAULT_PERIOD = '1y'  # 1 día, 5 días, 1 mes, 3 meses, 6 meses, 1 año, 5 años, 10 años, max
DEFAULT_INTERVAL = '1d'  # 1m, 5m, 15m, 30m, 60m, 1d, 1wk, 1mo

# ==================== INDICADORES TÉCNICOS ====================
# SMA (Simple Moving Average)
SMA_PERIODS = [20, 50, 200]

# EMA (Exponential Moving Average)
EMA_PERIODS = [12, 26]

# RSI (Relative Strength Index)
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

# MACD (Moving Average Convergence Divergence)
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

# Bandas de Bollinger
BOLLINGER_PERIOD = 20
BOLLINGER_STD = 2

# Stochastic
STOCH_PERIOD = 14
STOCH_SMOOTH_K = 3
STOCH_SMOOTH_D = 3

# ==================== PARÁMETROS DE SEÑALES ====================
# Niveles de confianza para señales
CONFIDENCE_STRONG = 80
CONFIDENCE_MODERATE = 60
CONFIDENCE_WEAK = 40

# Umbrales de RSI
RSI_BUY_THRESHOLD = 30
RSI_SELL_THRESHOLD = 70

# ==================== BACKTESTING ====================
BACKTEST_INITIAL_CAPITAL = 10000  # Capital inicial en USD
BACKTEST_COMMISSION = 0.001  # 0.1% de comisión
BACKTEST_SLIPPAGE = 0.001  # 0.1% de deslizamiento

# ==================== API ====================
API_HOST = '0.0.0.0'
API_PORT = 5000
API_DEBUG = True

# ==================== ALMACENAMIENTO ====================
DATA_PATH = './data/historical'
CACHE_PATH = './cache'
REPORTS_PATH = './reports'

# Crear directorios si no existen
for path in [DATA_PATH, CACHE_PATH, REPORTS_PATH]:
    os.makedirs(path, exist_ok=True)

# ==================== VARIABLES DE ENTORNO ====================
API_KEY = os.getenv('API_KEY', '')
LOG_FILE = os.getenv('LOG_FILE', 'trading_analyzer.log')

# ==================== ESTRATEGIAS ====================
STRATEGIES = {
    'SMA': 'Simple Moving Average',
    'RSI': 'Relative Strength Index',
    'MACD': 'MACD Strategy',
    'COMBINED': 'Combined Strategy',
    'BOLLINGER': 'Bollinger Bands'
}

# ==================== TIMEFRAMES ====================
TIMEFRAMES = {
    '1m': '1 minuto',
    '5m': '5 minutos',
    '15m': '15 minutos',
    '30m': '30 minutos',
    '1h': '1 hora',
    '1d': '1 día',
    '1wk': '1 semana',
    '1mo': '1 mes'
}

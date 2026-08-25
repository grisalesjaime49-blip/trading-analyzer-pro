"""
Módulo de backtesting
"""
from .engine import BacktestEngine
from .strategies import SimpleMA, RSIStrategy, MACDStrategy, CombinedStrategy
from .performance import PerformanceAnalyzer

__all__ = ['BacktestEngine', 'SimpleMA', 'RSIStrategy', 'MACDStrategy', 'CombinedStrategy', 'PerformanceAnalyzer']

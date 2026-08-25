"""
Motor de backtesting para estrategias de trading
"""
import pandas as pd
import numpy as np
from .performance import PerformanceAnalyzer
from config import BACKTEST_INITIAL_CAPITAL, BACKTEST_COMMISSION, BACKTEST_SLIPPAGE

class BacktestEngine:
    """
    Ejecuta backtests de estrategias de trading
    """
    
    def __init__(self, initial_capital=BACKTEST_INITIAL_CAPITAL, 
                 commission=BACKTEST_COMMISSION, slippage=BACKTEST_SLIPPAGE):
        self.initial_capital = initial_capital
        self.commission = commission
        self.slippage = slippage
        self.trades = []
        self.portfolio_value = []
    
    def run(self, df, strategy_signals, stop_loss=0.02, take_profit=0.05):
        """
        Ejecuta un backtest
        
        Args:
            df: DataFrame con datos OHLCV e indicadores
            strategy_signals: Series con señales (1=BUY, -1=SELL, 0=HOLD)
            stop_loss: Porcentaje de stop loss
            take_profit: Porcentaje de take profit
            
        Returns:
            dict con resultados del backtest
        """
        self.trades = []
        self.portfolio_value = [initial_capital := self.initial_capital]
        
        position = None  # None, 'long', 'short'
        entry_price = 0
        entry_index = 0
        
        for i in range(1, len(df)):
            current_price = df['Close'].iloc[i]
            signal = strategy_signals.iloc[i]
            portfolio_val = self.portfolio_value[-1]
            
            # Verificar stop loss y take profit
            if position == 'long':
                loss_pct = (current_price - entry_price) / entry_price
                
                if loss_pct <= -stop_loss or loss_pct >= take_profit:
                    exit_price = current_price * (1 - self.slippage) if loss_pct <= -stop_loss else current_price
                    profit = (exit_price - entry_price) * (portfolio_val / entry_price)
                    profit -= abs(profit) * self.commission
                    
                    self.trades.append({
                        'entry_index': entry_index,
                        'exit_index': i,
                        'entry_price': entry_price,
                        'exit_price': exit_price,
                        'profit': profit,
                        'profit_pct': (exit_price - entry_price) / entry_price * 100
                    })
                    
                    portfolio_val = portfolio_val + profit
                    position = None
            
            # Generar señales
            if signal == 1 and position is None:
                position = 'long'
                entry_price = current_price * (1 + self.slippage)
                entry_index = i
            
            elif signal == -1 and position == 'long':
                exit_price = current_price * (1 - self.slippage)
                profit = (exit_price - entry_price) * (portfolio_val / entry_price)
                profit -= abs(profit) * self.commission
                
                self.trades.append({
                    'entry_index': entry_index,
                    'exit_index': i,
                    'entry_price': entry_price,
                    'exit_price': exit_price,
                    'profit': profit,
                    'profit_pct': (exit_price - entry_price) / entry_price * 100
                })
                
                portfolio_val = portfolio_val + profit
                position = None
            
            self.portfolio_value.append(portfolio_val)
        
        # Cerrar posición abierta
        if position == 'long':
            exit_price = df['Close'].iloc[-1]
            profit = (exit_price - entry_price) * (self.portfolio_value[-1] / entry_price)
            profit -= abs(profit) * self.commission
            
            self.trades.append({
                'entry_index': entry_index,
                'exit_index': len(df) - 1,
                'entry_price': entry_price,
                'exit_price': exit_price,
                'profit': profit,
                'profit_pct': (exit_price - entry_price) / entry_price * 100
            })
            
            self.portfolio_value.append(self.portfolio_value[-1] + profit)
        
        # Calcular métricas
        analyzer = PerformanceAnalyzer()
        metrics = analyzer.calculate_metrics(
            self.portfolio_value, 
            self.trades, 
            self.initial_capital
        )
        
        return metrics
    
    def get_trades(self):
        """
        Retorna lista de trades ejecutados
        """
        return self.trades
    
    def get_portfolio_values(self):
        """
        Retorna valores del portafolio a lo largo del tiempo
        """
        return self.portfolio_value

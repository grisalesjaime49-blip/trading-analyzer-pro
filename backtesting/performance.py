"""
Analizador de rendimiento para backtests
"""
import pandas as pd
import numpy as np
from scipy import stats

class PerformanceAnalyzer:
    """
    Calcula métricas de rendimiento de backtests
    """
    
    @staticmethod
    def calculate_metrics(portfolio_values, trades, initial_capital):
        """
        Calcula métricas de rendimiento
        
        Args:
            portfolio_values: Lista de valores del portafolio
            trades: Lista de trades ejecutados
            initial_capital: Capital inicial
            
        Returns:
            dict con métricas
        """
        if len(portfolio_values) < 2:
            return {'error': 'Datos insuficientes'}
        
        final_capital = portfolio_values[-1]
        total_return = (final_capital - initial_capital) / initial_capital * 100
        
        # Cálculo de Sharpe Ratio
        returns = np.diff(portfolio_values) / portfolio_values[:-1]
        sharpe_ratio = np.mean(returns) / np.std(returns) * np.sqrt(252) if np.std(returns) > 0 else 0
        
        # Drawdown máximo
        cummax = np.maximum.accumulate(portfolio_values)
        drawdown = (np.array(portfolio_values) - cummax) / cummax
        max_drawdown = np.min(drawdown) * 100
        
        # Estadísticas de trades
        if trades:
            winning_trades = len([t for t in trades if t['profit_pct'] > 0])
            losing_trades = len([t for t in trades if t['profit_pct'] < 0])
            win_rate = winning_trades / len(trades) * 100 if trades else 0
            
            avg_win = np.mean([t['profit'] for t in trades if t['profit'] > 0]) if winning_trades > 0 else 0
            avg_loss = np.mean([t['profit'] for t in trades if t['profit'] < 0]) if losing_trades > 0 else 0
            
            profit_factor = abs(sum([t['profit'] for t in trades if t['profit'] > 0]) / 
                              sum([t['profit'] for t in trades if t['profit'] < 0])) \
                          if losing_trades > 0 else 0
        else:
            win_rate = 0
            avg_win = 0
            avg_loss = 0
            profit_factor = 0
            winning_trades = 0
            losing_trades = 0
        
        return {
            'initial_capital': initial_capital,
            'final_capital': final_capital,
            'total_return': total_return,
            'total_trades': len(trades),
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': win_rate,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'profit_factor': profit_factor,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'daily_return_avg': np.mean(returns) * 100,
            'daily_return_std': np.std(returns) * 100
        }
    
    @staticmethod
    def print_report(metrics):
        """
        Imprime reporte de métricas
        
        Args:
            metrics: dict con métricas
        """
        print("\n" + "="*60)
        print("REPORTE DE BACKTESTING")
        print("="*60)
        print(f"Capital Inicial:        ${metrics['initial_capital']:,.2f}")
        print(f"Capital Final:          ${metrics['final_capital']:,.2f}")
        print(f"Retorno Total:          {metrics['total_return']:.2f}%")
        print(f"\nTotal de Trades:        {metrics['total_trades']}")
        print(f"Trades Ganadores:       {metrics['winning_trades']}")
        print(f"Trades Perdedores:      {metrics['losing_trades']}")
        print(f"Win Rate:               {metrics['win_rate']:.2f}%")
        print(f"\nGanancia Promedio:      ${metrics['avg_win']:.2f}")
        print(f"Pérdida Promedio:      ${metrics['avg_loss']:.2f}")
        print(f"Profit Factor:          {metrics['profit_factor']:.2f}")
        print(f"\nSharpe Ratio:           {metrics['sharpe_ratio']:.2f}")
        print(f"Max Drawdown:           {metrics['max_drawdown']:.2f}%")
        print(f"Retorno Diario Promedio: {metrics['daily_return_avg']:.4f}%")
        print(f"Desv. Estándar Diaria:  {metrics['daily_return_std']:.4f}%")
        print("="*60 + "\n")

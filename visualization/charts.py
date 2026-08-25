"""
Generador de gráficos
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
import pandas as pd
import numpy as np
import os
from config import REPORTS_PATH

class ChartGenerator:
    """
    Genera gráficos de análisis técnico
    """
    
    @staticmethod
    def plot_price_and_sma(df, symbol='Asset', save=False):
        """
        Grafica precio con medias móviles
        
        Args:
            df: DataFrame con datos
            symbol: Símbolo del activo
            save: Guardar imagen
        """
        fig, ax = plt.subplots(figsize=(14, 6))
        
        ax.plot(df.index, df['Close'], label='Precio', color='black', linewidth=2)
        
        if 'SMA_20' in df.columns:
            ax.plot(df.index, df['SMA_20'], label='SMA 20', alpha=0.7)
        if 'SMA_50' in df.columns:
            ax.plot(df.index, df['SMA_50'], label='SMA 50', alpha=0.7)
        if 'SMA_200' in df.columns:
            ax.plot(df.index, df['SMA_200'], label='SMA 200', alpha=0.7)
        
        ax.set_title(f'{symbol} - Precio y Medias Móviles', fontsize=14, fontweight='bold')
        ax.set_xlabel('Fecha')
        ax.set_ylabel('Precio (USD)')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        if save:
            filepath = os.path.join(REPORTS_PATH, f'{symbol}_sma.png')
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"✅ Gráfico guardado: {filepath}")
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_rsi(df, symbol='Asset', save=False):
        """
        Grafica RSI
        
        Args:
            df: DataFrame con datos
            symbol: Símbolo del activo
            save: Guardar imagen
        """
        fig, ax = plt.subplots(figsize=(14, 4))
        
        ax.plot(df.index, df.get('RSI', 0), label='RSI', color='blue', linewidth=2)
        ax.axhline(y=70, color='r', linestyle='--', alpha=0.7, label='Sobrecompra (70)')
        ax.axhline(y=30, color='g', linestyle='--', alpha=0.7, label='Sobreventa (30)')
        ax.fill_between(df.index, 70, 100, alpha=0.2, color='red')
        ax.fill_between(df.index, 0, 30, alpha=0.2, color='green')
        
        ax.set_title(f'{symbol} - RSI', fontsize=14, fontweight='bold')
        ax.set_xlabel('Fecha')
        ax.set_ylabel('RSI')
        ax.set_ylim([0, 100])
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        if save:
            filepath = os.path.join(REPORTS_PATH, f'{symbol}_rsi.png')
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"✅ Gráfico guardado: {filepath}")
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_macd(df, symbol='Asset', save=False):
        """
        Grafica MACD
        
        Args:
            df: DataFrame con datos
            symbol: Símbolo del activo
            save: Guardar imagen
        """
        fig, ax = plt.subplots(figsize=(14, 4))
        
        ax.plot(df.index, df.get('MACD', 0), label='MACD', color='blue', linewidth=2)
        ax.plot(df.index, df.get('MACD_Signal', 0), label='Señal', color='red', linewidth=2)
        ax.bar(df.index, df.get('MACD_Histogram', 0), label='Histograma', alpha=0.3)
        
        ax.set_title(f'{symbol} - MACD', fontsize=14, fontweight='bold')
        ax.set_xlabel('Fecha')
        ax.set_ylabel('MACD')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        if save:
            filepath = os.path.join(REPORTS_PATH, f'{symbol}_macd.png')
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"✅ Gráfico guardado: {filepath}")
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_bollinger_bands(df, symbol='Asset', save=False):
        """
        Grafica Bandas de Bollinger
        
        Args:
            df: DataFrame con datos
            symbol: Símbolo del activo
            save: Guardar imagen
        """
        fig, ax = plt.subplots(figsize=(14, 6))
        
        ax.plot(df.index, df['Close'], label='Precio', color='black', linewidth=2)
        ax.plot(df.index, df.get('BB_Upper', 0), label='Banda Superior', color='red', alpha=0.7)
        ax.plot(df.index, df.get('BB_Middle', 0), label='SMA 20', color='blue', alpha=0.7, linestyle='--')
        ax.plot(df.index, df.get('BB_Lower', 0), label='Banda Inferior', color='green', alpha=0.7)
        ax.fill_between(df.index, df.get('BB_Upper', 0), df.get('BB_Lower', 0), alpha=0.1, color='blue')
        
        ax.set_title(f'{symbol} - Bandas de Bollinger', fontsize=14, fontweight='bold')
        ax.set_xlabel('Fecha')
        ax.set_ylabel('Precio (USD)')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        if save:
            filepath = os.path.join(REPORTS_PATH, f'{symbol}_bollinger.png')
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"✅ Gráfico guardado: {filepath}")
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_backtest_results(portfolio_values, trades, symbol='Asset', save=False):
        """
        Grafica resultados de backtesting
        
        Args:
            portfolio_values: Lista de valores del portafolio
            trades: Lista de trades
            symbol: Símbolo del activo
            save: Guardar imagen
        """
        fig, ax = plt.subplots(figsize=(14, 6))
        
        ax.plot(range(len(portfolio_values)), portfolio_values, label='Valor del Portafolio', 
                color='blue', linewidth=2)
        
        for trade in trades:
            entry_idx = trade['entry_index']
            exit_idx = trade['exit_index']
            color = 'green' if trade['profit'] > 0 else 'red'
            ax.plot([entry_idx, exit_idx], 
                   [portfolio_values[entry_idx], portfolio_values[exit_idx]], 
                   color=color, alpha=0.5, linewidth=1)
        
        ax.set_title(f'{symbol} - Resultados de Backtesting', fontsize=14, fontweight='bold')
        ax.set_xlabel('Día')
        ax.set_ylabel('Valor del Portafolio (USD)')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        if save:
            filepath = os.path.join(REPORTS_PATH, f'{symbol}_backtest.png')
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"✅ Gráfico guardado: {filepath}")
        
        plt.tight_layout()
        return fig

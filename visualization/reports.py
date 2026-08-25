"""
Generador de reportes
"""
import os
from datetime import datetime
from config import REPORTS_PATH

class ReportGenerator:
    """
    Genera reportes en diferentes formatos
    """
    
    @staticmethod
    def generate_html_report(df, signals, metrics, symbol='Asset', filename=None):
        """
        Genera reporte HTML
        
        Args:
            df: DataFrame con datos
            signals: Señales de trading
            metrics: Métricas de rendimiento
            symbol: Símbolo del activo
            filename: Nombre del archivo (opcional)
        """
        if filename is None:
            filename = f"{symbol}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        filepath = os.path.join(REPORTS_PATH, filename)
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Reporte de Trading - {symbol}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    background-color: #f5f5f5;
                }}
                .header {{
                    background-color: #2c3e50;
                    color: white;
                    padding: 20px;
                    border-radius: 5px;
                    margin-bottom: 20px;
                }}
                .section {{
                    background-color: white;
                    padding: 15px;
                    margin-bottom: 15px;
                    border-radius: 5px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 10px;
                }}
                th, td {{
                    padding: 10px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                th {{
                    background-color: #3498db;
                    color: white;
                }}
                .positive {{
                    color: green;
                    font-weight: bold;
                }}
                .negative {{
                    color: red;
                    font-weight: bold;
                }}
                .metric {{
                    display: inline-block;
                    width: 23%;
                    margin: 1%;
                    padding: 10px;
                    background-color: #ecf0f1;
                    border-radius: 5px;
                    text-align: center;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Reporte de Trading - {symbol}</h1>
                <p>Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="section">
                <h2>Señal Actual</h2>
                <p><strong>Señal:</strong> {signals.get('signal', 'N/A')}</p>
                <p><strong>Confianza:</strong> {signals.get('confidence', 0)}%</p>
                <p><strong>Precio Actual:</strong> ${signals.get('price', 0):.2f}</p>
            </div>
            
            <div class="section">
                <h2>Métricas de Rendimiento</h2>
                <div class="metric">
                    <h4>Retorno Total</h4>
                    <p class="{'positive' if metrics.get('total_return', 0) > 0 else 'negative'}">
                    {metrics.get('total_return', 0):.2f}%</p>
                </div>
                <div class="metric">
                    <h4>Win Rate</h4>
                    <p>{metrics.get('win_rate', 0):.2f}%</p>
                </div>
                <div class="metric">
                    <h4>Sharpe Ratio</h4>
                    <p>{metrics.get('sharpe_ratio', 0):.2f}</p>
                </div>
                <div class="metric">
                    <h4>Max Drawdown</h4>
                    <p class="negative">{metrics.get('max_drawdown', 0):.2f}%</p>
                </div>
            </div>
            
            <div class="section">
                <h2>Últimos Datos</h2>
                <table>
                    <tr>
                        <th>Fecha</th>
                        <th>Apertura</th>
                        <th>Máximo</th>
                        <th>Mínimo</th>
                        <th>Cierre</th>
                        <th>Volumen</th>
                    </tr>
        """
        
        # Últimas 10 filas
        for idx, row in df.tail(10).iterrows():
            html_content += f"""
                    <tr>
                        <td>{idx.strftime('%Y-%m-%d')}</td>
                        <td>${row['Open']:.2f}</td>
                        <td>${row['High']:.2f}</td>
                        <td>${row['Low']:.2f}</td>
                        <td>${row['Close']:.2f}</td>
                        <td>{int(row['Volume']):,}</td>
                    </tr>
            """
        
        html_content += """
                </table>
            </div>
        </body>
        </html>
        """
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Reporte HTML guardado: {filepath}")
        return filepath
    
    @staticmethod
    def generate_csv_report(trades, symbol='Asset', filename=None):
        """
        Genera reporte CSV de trades
        
        Args:
            trades: Lista de trades
            symbol: Símbolo del activo
            filename: Nombre del archivo (opcional)
        """
        import csv
        
        if filename is None:
            filename = f"{symbol}_trades_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = os.path.join(REPORTS_PATH, filename)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['entry_index', 'exit_index', 'entry_price', 
                                                     'exit_price', 'profit', 'profit_pct'])
            writer.writeheader()
            writer.writerows(trades)
        
        print(f"✅ Reporte CSV guardado: {filepath}")
        return filepath

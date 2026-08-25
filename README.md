# 📈 Trading Analyzer Pro

Un analizador de trading profesional con análisis técnico, backtesting y generación de señales de compra/venta en tiempo real.

## 🎯 Características

- ✅ Análisis técnico avanzado (SMA, EMA, RSI, MACD, Bandas de Bollinger)
- ✅ Descarga automática de datos de precios
- ✅ Motor de backtesting para estrategias
- ✅ Generador de señales de trading
- ✅ Visualización de gráficos
- ✅ API REST para consultas
- ✅ Alertas en tiempo real
- ✅ Exportación de reportes

## 📋 Requisitos Previos

- Python 3.9+
- pip (gestor de paquetes)

## 🚀 Instalación Rápida

### 1. Clonar el repositorio

```bash
git clone https://github.com/grisalesjaime49-blip/trading-analyzer-pro.git
cd trading-analyzer-pro
```

### 2. Crear entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 📁 Estructura del Proyecto

```
trading-analyzer-pro/
│
├── main.py                 # Punto de entrada principal
├── requirements.txt        # Dependencias del proyecto
├── config.py              # Configuración global
│
├── analyzers/
│   ├── __init__.py
│   ├── technical.py       # Indicadores técnicos
│   ├── signals.py         # Generador de señales
│   └── patterns.py        # Patrones de velas
│
├── data/
│   ├── __init__.py
│   ├── downloader.py      # Descarga de datos
│   ├── processor.py       # Procesamiento de datos
│   └── storage.py         # Almacenamiento de datos
│
├── backtesting/
│   ├── __init__.py
│   ├── engine.py          # Motor de backtesting
│   ├── strategies.py      # Estrategias predefinidas
│   └── performance.py     # Análisis de rendimiento
│
├── visualization/
│   ├── __init__.py
│   ├── charts.py          # Generación de gráficos
│   └── reports.py         # Reportes
│
├── api/
│   ├── __init__.py
│   └── server.py          # Servidor REST
│
└── examples/
    ├── basic_analysis.py
    ├── backtesting_example.py
    └── signals_example.py
```

## 💻 Primeros Pasos

### Opción 1: Análisis Técnico Básico

```bash
python examples/basic_analysis.py
```

Esto descargará datos de Bitcoin, calculará indicadores técnicos y mostrará los resultados.

### Opción 2: Ejecutar Backtesting

```bash
python examples/backtesting_example.py
```

Prueba una estrategia en datos históricos.

### Opción 3: Generar Señales

```bash
python examples/signals_example.py
```

Genera señales de compra/venta actuales.

### Opción 4: Iniciar API REST

```bash
python api/server.py
```

La API estará en `http://localhost:5000`

## 📊 Ejemplos de Uso

### Descargar datos y analizar

```python
from data.downloader import DataDownloader
from analyzers.technical import TechnicalAnalyzer

# Descargar datos
downloader = DataDownloader()
df = downloader.fetch('BTC-USD', period='3mo')

# Analizar
analyzer = TechnicalAnalyzer()
analyzer.add_sma(df, periods=[20, 50])
analyzer.add_rsi(df)
analyzer.add_macd(df)

print(df.tail())
```

### Usar señales de trading

```python
from analyzers.signals import SignalGenerator

generator = SignalGenerator()
signals = generator.generate(df)

print(f"Señal actual: {signals['signal']}")
print(f"Confianza: {signals['confidence']}%")
```

### Ejecutar backtesting

```python
from backtesting.engine import BacktestEngine
from backtesting.strategies import SimpleMA

engine = BacktestEngine()
results = engine.run(
    symbol='BTC-USD',
    strategy=SimpleMA,
    start_date='2023-01-01',
    end_date='2024-01-01'
)

print(f"Retorno: {results['total_return']}%")
print(f"Sharpe Ratio: {results['sharpe_ratio']}")
```

## 🔧 Configuración

Edita `config.py` para personalizar:

```python
# Símbolos a analizar
SYMBOLS = ['BTC-USD', 'ETH-USD', 'AAPL']

# Períodos de análisis
SMA_PERIODS = [20, 50, 200]

# Parámetros RSI
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

# Parámetros MACD
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
```

## 📡 Endpoints de la API

### GET /analyze/:symbol
Analiza un símbolo y retorna indicadores técnicos

```bash
curl http://localhost:5000/analyze/BTC-USD
```

**Respuesta:**
```json
{
  "symbol": "BTC-USD",
  "price": 45000,
  "sma_20": 44500,
  "sma_50": 43000,
  "rsi": 65,
  "macd": 200,
  "signal": "BUY",
  "confidence": 78
}
```

### GET /signals/:symbol
Obtiene señales de trading actuales

```bash
curl http://localhost:5000/signals/BTC-USD
```

### POST /backtest
Ejecuta un backtest con parámetros personalizados

```bash
curl -X POST http://localhost:5000/backtest \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "BTC-USD",
    "strategy": "SMA",
    "start_date": "2023-01-01",
    "end_date": "2024-01-01"
  }'
```

## 📈 Indicadores Disponibles

| Indicador | Descripción | Uso |
|-----------|-------------|-----|
| **SMA** | Media Móvil Simple | Tendencia a largo plazo |
| **EMA** | Media Móvil Exponencial | Tendencia con peso reciente |
| **RSI** | Índice de Fuerza Relativa | Condiciones de sobrecompra/sobreventa |
| **MACD** | Convergencia/Divergencia de Medias Móviles | Cambios de momento |
| **Bollinger Bands** | Bandas de volatilidad | Niveles de soporte/resistencia |
| **Stochastic** | Oscilador Estocástico | Momentum |

## 🧪 Estrategias de Trading

### SMA (Simple Moving Average)
- Compra cuando SMA corta cruza SMA larga hacia arriba
- Vende cuando SMA corta cruza SMA larga hacia abajo

### RSI
- Compra cuando RSI < 30 (oversold)
- Vende cuando RSI > 70 (overbought)

### MACD
- Compra cuando MACD cruza por encima de la línea de señal
- Vende cuando MACD cruza por debajo de la línea de señal

### Combinada
- Usa múltiples indicadores para confirmar señales

## 📊 Entender los Resultados

### Señales
- 🟢 **BUY**: Compra recomendada
- 🔴 **SELL**: Venta recomendada
- ⚪ **HOLD**: Mantener posición

### Confianza
- 80-100%: Señal muy fuerte
- 60-80%: Señal moderada
- 40-60%: Señal débil
- <40%: Ignorar

### Métricas de Backtesting
- **Total Return**: Ganancia/pérdida total
- **Sharpe Ratio**: Riesgo ajustado (>1 es bueno)
- **Win Rate**: Porcentaje de operaciones ganadoras
- **Max Drawdown**: Máxima caída desde pico

## 🔐 Variables de Entorno

Crea un archivo `.env`:

```bash
API_KEY=your_api_key_here
SYMBOLS=BTC-USD,ETH-USD
DATA_PATH=./data/historical
LOG_LEVEL=INFO
```

## 🐛 Troubleshooting

### Error: "No module named 'yfinance'"
```bash
pip install yfinance
```

### Error: "Connection timeout"
Verifica tu conexión a internet

### Error: "No data available"
El símbolo no es válido o no hay datos para ese período

## 📚 Recursos Adicionales

- [Documentación de Pandas](https://pandas.pydata.org/)
- [Documentación de yfinance](https://github.com/ranaroussi/yfinance)
- [Análisis Técnico 101](https://www.investopedia.com/terms/t/technicalanalysis.asp)

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT.

## ⚠️ Disclaimer

**Este software es solo para propósitos educativos. No es un asesor financiero. El trading implica riesgo. Nunca inviertas dinero que no puedas perder. Realiza tu propia investigación y consulta con un asesor financiero antes de tomar decisiones de inversión.**

---

**Última actualización**: 2024
**Versión**: 1.0.0

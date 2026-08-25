"""
Módulo para almacenar y cargar datos
"""
import pandas as pd
import os
from config import DATA_PATH
import pickle
import json
from datetime import datetime

class DataStorage:
    """
    Almacena y carga datos de precios
    """
    
    @staticmethod
    def save_csv(df, symbol, data_dir=DATA_PATH):
        """
        Guarda datos en CSV
        
        Args:
            df: DataFrame a guardar
            symbol: Símbolo del activo
            data_dir: Directorio de almacenamiento
        """
        filepath = os.path.join(data_dir, f'{symbol}_data.csv')
        df.to_csv(filepath)
        print(f"✅ Datos guardados en {filepath}")
    
    @staticmethod
    def load_csv(symbol, data_dir=DATA_PATH):
        """
        Carga datos de CSV
        
        Args:
            symbol: Símbolo del activo
            data_dir: Directorio de almacenamiento
            
        Returns:
            DataFrame con datos
        """
        filepath = os.path.join(data_dir, f'{symbol}_data.csv')
        
        if not os.path.exists(filepath):
            return None
        
        df = pd.read_csv(filepath, index_col=0, parse_dates=True)
        return df
    
    @staticmethod
    def save_pickle(obj, filename, data_dir=DATA_PATH):
        """
        Guarda objeto en pickle
        
        Args:
            obj: Objeto a guardar
            filename: Nombre del archivo
            data_dir: Directorio de almacenamiento
        """
        filepath = os.path.join(data_dir, filename)
        with open(filepath, 'wb') as f:
            pickle.dump(obj, f)
        print(f"✅ Objeto guardado en {filepath}")
    
    @staticmethod
    def load_pickle(filename, data_dir=DATA_PATH):
        """
        Carga objeto de pickle
        
        Args:
            filename: Nombre del archivo
            data_dir: Directorio de almacenamiento
            
        Returns:
            Objeto cargado
        """
        filepath = os.path.join(data_dir, filename)
        
        if not os.path.exists(filepath):
            return None
        
        with open(filepath, 'rb') as f:
            return pickle.load(f)
    
    @staticmethod
    def save_json(data, filename, data_dir=DATA_PATH):
        """
        Guarda datos en JSON
        
        Args:
            data: Datos a guardar
            filename: Nombre del archivo
            data_dir: Directorio de almacenamiento
        """
        filepath = os.path.join(data_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        print(f"✅ Datos guardados en {filepath}")
    
    @staticmethod
    def load_json(filename, data_dir=DATA_PATH):
        """
        Carga datos de JSON
        
        Args:
            filename: Nombre del archivo
            data_dir: Directorio de almacenamiento
            
        Returns:
            Datos cargados
        """
        filepath = os.path.join(data_dir, filename)
        
        if not os.path.exists(filepath):
            return None
        
        with open(filepath, 'r') as f:
            return json.load(f)

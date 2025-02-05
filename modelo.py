import pandas as pd
import sqlite3
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

def entrenar_modelo_arima(serie_temporal, orden=(1, 1, 1)):
     
    modelo = ARIMA(serie_temporal, order=orden)
    resultado = modelo.fit()
    return resultado

def hacer_predicciones_arima(modelo, pasos_futuros=6):
     
    predicciones = modelo.forecast(steps=pasos_futuros)
    return predicciones
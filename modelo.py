from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd

def entrenar_modelo(df, columna_objetivo, test_size=0.2, random_state=42, n_estimators=100):
    # Convertir los nombres de las columnas a minúsculas para uniformidad
    df.columns = [col.lower() for col in df.columns]
    columna_objetivo = columna_objetivo.lower()
    
    # Verificar que la columna objetivo esté en el DataFrame
    if columna_objetivo not in df.columns:
        raise ValueError(f"La columna '{columna_objetivo}' no existe en el DataFrame.")
    
    # Si existe la columna "dias", la usaremos como única característica (para pronosticar a partir del tiempo)
    if "dias" in df.columns:
        X = df[["dias"]]
    else:
        # Si no, se usan todas las columnas excepto la objetivo, fecha e id.
        X = df.drop(columns=[columna_objetivo, "fecha", "id"], errors="ignore")
    
    y = df[columna_objetivo]
    
    # Dividir datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    
    # Entrenar el modelo Random Forest
    modelo = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state)
    modelo.fit(X_train, y_train)
    
    # Predecir en el conjunto de prueba
    y_pred = modelo.predict(X_test)
    
    # Evaluar el modelo
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"Error cuadrático medio (MSE): {mse}")
    print(f"Coeficiente de determinación (R²): {r2}")
    
    return modelo, mse, r2
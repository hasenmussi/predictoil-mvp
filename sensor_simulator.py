import time
import pandas as pd
import numpy as np
from datetime import datetime

# Crear archivo CSV inicial si no existe
try:
    df = pd.read_csv("sensor_data.csv")
except FileNotFoundError:
    df = pd.DataFrame(columns=["timestamp", "temperature", "vibration", "pressure"])
    df.to_csv("sensor_data.csv", index=False)

while True:
    # Simular nueva lectura de sensores
    new_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": np.random.normal(70, 2),    # promedio 70°C
        "vibration": np.random.normal(5, 0.5),     # promedio 5 mm/s
        "pressure": np.random.normal(30, 1)        # promedio 30 bar
    }

    # Leer el archivo existente y agregar nueva fila
    df = pd.read_csv("sensor_data.csv")
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    
    # Guardar los datos actualizados
    df.to_csv("sensor_data.csv", index=False)

    # Esperar 10 segundos para la siguiente lectura
    time.sleep(10)

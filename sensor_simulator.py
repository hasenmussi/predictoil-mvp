import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np
from datetime import datetime

# Autenticación con Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", scope)
client = gspread.authorize(creds)

# Abrir la hoja de cálculo y seleccionar la primera hoja
spreadsheet = client.open("PredictOil_Data")  # Nombre exacto de tu hoja
sheet = spreadsheet.sheet1

# Bucle de simulación
while True:
    # Simular datos
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    temperature = round(np.random.normal(70, 2), 2)
    vibration = round(np.random.normal(5, 0.5), 2)
    pressure = round(np.random.normal(30, 1), 2)

    # Agregar fila
    sheet.append_row([timestamp, temperature, vibration, pressure])
    print(f"📡 Enviado: {timestamp}, {temperature}, {vibration}, {pressure}")

    time.sleep(10)  # Espera de 10 segundos

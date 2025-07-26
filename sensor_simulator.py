import gspread
import random
import time
import json
import os
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

# --- Autenticación con Google Sheets desde secretos ---
creds_json = os.getenv("GOOGLE_CREDENTIALS")
creds_dict = json.loads(creds_json)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

sheet = client.open("PredictOil_Data").sheet1

# --- Simulación de datos ---
while True:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    temperatura = round(random.uniform(60, 90), 2)
    vibracion = round(random.uniform(3, 8), 2)
    presion = round(random.uniform(20, 40), 2)

    row = [timestamp, temperatura, vibracion, presion]
    sheet.append_row(row)
    print(f"📡 Enviado: {row}")

    time.sleep(10)

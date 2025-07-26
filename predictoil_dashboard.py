import streamlit as st
import pandas as pd
import gspread
import json
import os
from oauth2client.service_account import ServiceAccountCredentials
import time

st.set_page_config(page_title="PredictOil Dashboard", layout="wide")
st.title("📊 PredictOil - Monitoreo en Tiempo Real")

# --- Autenticación con Google Sheets desde secretos ---
creds_json = os.getenv("GOOGLE_CREDENTIALS")
creds_dict = json.loads(creds_json)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# --- Leer los datos desde Google Sheets ---
sheet = client.open("PredictOil_Data").sheet1
data = sheet.get_all_records()
df = pd.DataFrame(data)

# --- Visualización ---
if df.empty:
    st.warning("No hay datos disponibles todavía.")
else:
    st.subheader("📈 Datos Recientes")
    st.dataframe(df.tail(10), use_container_width=True)

    st.line_chart(df.set_index("timestamp")["temperatura"], use_container_width=True)
    st.line_chart(df.set_index("timestamp")["vibracion"], use_container_width=True)
    st.line_chart(df.set_index("timestamp")["presion"], use_container_width=True)

# --- Actualizar cada 10 segundos ---
time.sleep(10)
st.experimental_rerun()


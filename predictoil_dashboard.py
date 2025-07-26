import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from sklearn.ensemble import IsolationForest
import altair as alt
from datetime import datetime

st.set_page_config(page_title="PredictOil Dashboard", layout="wide")
st.title("🛢️ PredictOil - Dashboard en Tiempo Real")

# Autenticación
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
import os
import json
from oauth2client.service_account import ServiceAccountCredentials
import gspread

# Leer credenciales desde el secreto
creds_json = os.getenv("GOOGLE_CREDENTIALS")
creds_dict = json.loads(creds_json)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Leer la hoja
spreadsheet = client.open("PredictOil_Data")
sheet = spreadsheet.sheet1
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Procesar
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.tail(100)  # Mostrar solo las últimas 100 filas

# Modelo
if len(df) >= 50:
    model = IsolationForest(contamination=0.02, random_state=42)
    df["anomaly"] = model.fit_predict(df[["temperature", "vibration", "pressure"]])
else:
    df["anomaly"] = 1

# Visualización
st.altair_chart(alt.Chart(df).mark_line().encode(x="timestamp", y="temperature"), use_container_width=True)
st.altair_chart(alt.Chart(df).mark_line(color="orange").encode(x="timestamp", y="vibration"), use_container_width=True)
st.altair_chart(alt.Chart(df).mark_line(color="green").encode(x="timestamp", y="pressure"), use_container_width=True)

st.subheader("🚨 Anomalías")
st.dataframe(df[df["anomaly"] == -1][["timestamp", "temperature", "vibration", "pressure"]])

# Actualización automática
st.experimental_rerun()


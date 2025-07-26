import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
import streamlit as st
import altair as alt
import time

# Simular datos
np.random.seed(42)
n = 1000
temperature = np.random.normal(70, 2, n)
vibration = np.random.normal(5, 0.5, n)
pressure = np.random.normal(30, 1, n)
anomaly_indices = np.random.choice(n, 20, replace=False)
temperature[anomaly_indices] += np.random.normal(15, 5, 20)
vibration[anomaly_indices] += np.random.normal(3, 1, 20)
pressure[anomaly_indices] -= np.random.normal(5, 2, 20)

df = pd.DataFrame({
    "temperature": temperature,
    "vibration": vibration,
    "pressure": pressure
})

model = IsolationForest(contamination=0.02, random_state=42)
df["anomaly_score"] = model.fit_predict(df)

# Streamlit Dashboard
st.set_page_config(page_title="PredictOil Dashboard", layout="wide")
st.title("🔧 PredictOil - Monitor de Equipos Críticos")
st.markdown("Visualización de sensores y detección de anomalías en bombas industriales.")

st.subheader("📈 Sensores (últimos 100 registros)")
latest_df = df.tail(100).reset_index()

# Temperatura + Anomalías
temp_chart = alt.Chart(latest_df).mark_line().encode(
    x="index", y="temperature", tooltip=["index", "temperature"]
).properties(title="Temperatura (°C)")

anomalies = latest_df[latest_df["anomaly_score"] == -1]
anomaly_chart = alt.Chart(anomalies).mark_point(color="red", size=60).encode(
    x="index", y="temperature", tooltip=["index", "temperature"]
)

st.altair_chart(temp_chart + anomaly_chart, use_container_width=True)

# Vibration
vib_chart = alt.Chart(latest_df).mark_line(color="orange").encode(
    x="index", y="vibration", tooltip=["index", "vibration"]
).properties(title="Vibración (mm/s)")
st.altair_chart(vib_chart, use_container_width=True)

# Pressure
press_chart = alt.Chart(latest_df).mark_line(color="green").encode(
    x="index", y="pressure", tooltip=["index", "pressure"]
).properties(title="Presión (psi)")
st.altair_chart(press_chart, use_container_width=True)

# Tabla de anomalías
st.subheader("🚨 Anomalías Detectadas")
st.dataframe(anomalies[["index", "temperature", "vibration", "pressure"]], height=200)

# Simular actualización cada 10 segundos
st.markdown("🔄 Este panel se actualiza cada 10 segundos automáticamente.")

# Esperar 10 segundos y recargar
time.sleep(10)
st.rerun()

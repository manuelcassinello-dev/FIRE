import streamlit as st
from pymongo import MongoClient
import pandas as pd
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA PROFESIONAL
st.set_page_config(page_title="FIRE PRO", page_icon="🔥", layout="wide")

# 2. CONEXIÓN DIRECTA A TU MONGODB (De tu imagen image_0fa941.jpg)
# Asegúrate de usar la contraseña que definiste para este usuario
MONGO_URL = "mongodb://manuelcassinello_db_user:dn57lqnN25ZvE0J5@cluster0-shard-00-00.vygh6s.mongodb.net:27017,cluster0-shard-00-01.vygh6s.mongodb.net:27017,cluster0-shard-00-02.vygh6s.mongodb.net:27017/fuego_db?ssl=true&replicaSet=atlas-v6z6z1-shard-0&authSource=admin&retryWrites=true&w=majority"

@st.cache_resource
def init_connection():
    # Establecemos un tiempo de espera de 10 segundos para la conexión inicial
    return MongoClient(MONGO_URL, serverSelectionTimeoutMS=10000)

try:
    client = init_connection()
    db = client.fuego_db
    items = db.transacciones
    # Prueba de conexión rápida
    client.admin.command('ping')
except Exception as e:
    st.error(f"Error de infraestructura: {e}")

st.title("🔥 SISTEMA FUEGO v3.0 (MongoDB Edition)")

# 3. INTERFAZ DE REGISTRO
with st.form("registro", clear_on_submit=True):
    st.subheader("Registrar Movimiento")
    col1, col2 = st.columns(2)
    with col1:
        concepto = st.text_input("¿En qué se ha ido el dinero?")
    with col2:
        monto = st.number_input("Importe (€)", min_value=0.0, step=0.01)
    
    if st.form_submit_button("REGISTRAR AHORA"):
        if concepto and monto > 0:
            try:
                items.insert_one({
                    "concepto": concepto,
                    "importe": monto,
                    "fecha": datetime.now()
                })
                st.success(f"✅ ¡Guardado!: {concepto}")
                st.balloons()
            except Exception as e:
                st.error(f"No se pudo guardar: {e}")

# 4. DASHBOARD DE CONTROL
st.divider()
st.subheader("📊 Historial de Gastos e Ingresos")

try:
    # Traemos los datos ordenados por fecha (del más nuevo al más viejo)
    cursor = items.find().sort("fecha", -1)
    df = pd.DataFrame(list(cursor))
    
    if not df.empty:
        # Quitamos el ID interno de MongoDB para que la tabla quede limpia
        df = df.drop(columns=['_id'])
        
        # Formateamos la fecha para que sea legible
        df['fecha'] = pd.to_datetime(df['fecha']).dt.strftime('%d/%m/%Y %H:%M')
        
        # Mostramos métricas y tabla
        st.metric("Total Acumulado", f"{df['importe'].sum():,.2f} €")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("La base de datos está vacía. Registra tu primer movimiento arriba.")
except Exception as e:
    st.info("Esperando los primeros datos...")

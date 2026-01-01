import streamlit as st
from pymongo import MongoClient
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="FIRE PRO", page_icon="🔥", layout="wide")

# URL DEFINITIVA (Sin DNS abreviado para saltar el error de tu captura image_0fb86a.png)
MONGO_URL = "mongodb://manuelcassinello_db_user:dn57lqnN25ZvE0J5@cluster0-shard-00-00.vygh6s.mongodb.net:27017,cluster0-shard-00-01.vygh6s.mongodb.net:27017,cluster0-shard-00-02.vygh6s.mongodb.net:27017/fuego_db?ssl=true&replicaSet=atlas-v6z6z1-shard-0&authSource=admin&retryWrites=true&w=majority"

st.title("🔥 SISTEMA FUEGO v3.0")

# Formulario de Registro
with st.form("registro", clear_on_submit=True):
    concepto = st.text_input("Concepto")
    monto = st.number_input("Importe (€)", min_value=0.0)
    
    if st.form_submit_button("REGISTRAR AHORA"):
        try:
            # Conexión directa al pulsar el botón
            client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
            db = client.fuego_db
            # Definimos 'items' aquí para evitar el error 'not defined'
            items = db.transacciones
            
            items.insert_one({
                "concepto": concepto,
                "importe": monto,
                "fecha": datetime.now()
            })
            st.success("✅ ¡POR FIN GUARDADO!")
            st.balloons()
        except Exception as e:
            st.error(f"Fallo de conexión: {e}")

# Panel de Visualización
st.divider()
try:
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=2000)
    cursor = client.fuego_db.transacciones.find().sort("fecha", -1)
    df = pd.DataFrame(list(cursor))
    if not df.empty:
        st.dataframe(df.drop(columns=['_id']), use_container_width=True)
except:
    st.info("Esperando los primeros datos en la base de datos...")

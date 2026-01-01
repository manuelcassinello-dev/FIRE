import streamlit as st
from pymongo import MongoClient
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="FIRE PRO", page_icon="🔥", layout="wide")

# URL LARGA PARA SALTAR EL ERROR DE DNS
MONGO_URL = "mongodb://manuelcassinello_db_user:dn57lqnN25ZvE0J5@cluster0-shard-00-00.vygh6s.mongodb.net:27017,cluster0-shard-00-01.vygh6s.mongodb.net:27017,cluster0-shard-00-02.vygh6s.mongodb.net:27017/fuego_db?ssl=true&replicaSet=atlas-v6z6z1-shard-0&authSource=admin&retryWrites=true&w=majority"

st.title("🔥 SISTEMA FUEGO v3.0")

with st.form("registro", clear_on_submit=True):
    concepto = st.text_input("Concepto")
    monto = st.number_input("Importe (€)", min_value=0.0)
    
    if st.form_submit_button("REGISTRAR AHORA"):
        try:
            # Conexión directa aquí mismo para que no falle 'items'
            client = MongoClient(MONGO_URL)
            db = client.fuego_db
            items = db.transacciones
            
            items.insert_one({
                "concepto": concepto,
                "importe": monto,
                "fecha": datetime.now()
            })
            st.success("✅ ¡GUARDADO POR FIN!")
            st.balloons()
        except Exception as e:
            st.error(f"Error: {e}")

# Tabla de visualización
try:
    client = MongoClient(MONGO_URL)
    df = pd.DataFrame(list(client.fuego_db.transacciones.find().sort("fecha", -1)))
    if not df.empty:
        st.dataframe(df.drop(columns=['_id']), use_container_width=True)
except:
    st.info("Esperando datos...")

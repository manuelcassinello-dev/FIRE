import streamlit as st
import pandas as pd
from supabase import create_client

# 1. Credenciales verificadas de tu proyecto
URL = "https://104.21.50.231"
KEY = "sb_publishable_QCP0k-76xEiT10812eTpeQ_KbqiXwX81"
supabase = create_client(URL, KEY)

st.title("🔥 PROYECTO FIRE")

# 2. Interfaz de Usuario
tab1, tab2 = st.tabs(["📊 Dashboard", "➕ Registro"])

with tab2:
    with st.form("registro", clear_on_submit=True):
        st.subheader("Añadir Movimiento")
        concepto = st.text_input("Concepto")
        monto = st.number_input("Importe (€)", min_value=0.0)
        feliz = st.toggle("¿Te hace feliz?", value=True)
        
        if st.form_submit_button("REGISTRAR"):
            try:
                # Inserción con los nombres de tus columnas
                supabase.table("transacciones").insert({
                    "texto_de_descripción": concepto, 
                    "cantidad": monto, 
                    "me_hace_feliz": feliz
                }).execute()
                st.success(f"Guardado: {concepto}")
            except Exception as e:
                st.error(f"Error de red: {e}. Reintentando...")

with tab1:
    if st.button("Actualizar"):
        try:
            res = supabase.table("transacciones").select("*").execute()
            st.dataframe(pd.DataFrame(res.data))
        except Exception as e:
            st.error("No se pudo conectar con la base de datos.")

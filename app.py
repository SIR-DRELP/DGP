import streamlit as st
import gspread
import json
from google.oauth2.service_account import Credentials
from datetime import datetime

# --- 1. Conexión con Google Sheets ---
SHEET_ID = "19U5yr-iDoSlCqzujspUA9O14mTAFuaiMYBiaHTfriGQ"
SHEET_NAME = "profes"

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Cargar credenciales desde st.secrets
creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)

client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)

# --- 2. Interfaz Streamlit ---
st.title("Formulario: Registro de Profesores")

with st.form("form_profes"):
    dni = st.text_input("DNI", max_chars=8)
    apellidos = st.text_input("Apellidos")
    nombres = st.text_input("Nombres")
    celular = st.text_input("Celular", max_chars=9)
    enviar = st.form_submit_button("Guardar")

    if enviar:
        if dni and apellidos and nombres and celular:
            sheet.append_row([dni, apellidos, nombres, celular, datetime.now().strftime("%d/%m/%Y %H:%M:%S")])
            st.success("✅ Datos guardados correctamente en la hoja 'profes'")
        else:
            st.error("❌ Por favor, completa todos los campos.")

# --- 3. Mostrar registros actuales ---
st.markdown("### Registros actuales:")
datos = sheet.get_all_records()
if datos:
    st.dataframe(datos)
else:
    st.info("No hay registros aún.")

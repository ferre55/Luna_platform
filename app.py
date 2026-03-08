import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_lottie import st_lottie
import pandas as pd
import plotly.express as px
import requests
import os
from dotenv import load_dotenv

# --- CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="Luna | Safe Space", layout="wide", initial_sidebar_state="collapsed")

# Función para cargar animaciones Lottie
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Cargamos la animación de la Luna
lottie_moon = load_lottieurl("https://lottie.host/838f7a61-1234-4567-8901-23456789abcd/your_json.json") # Nota: Asegúrate de usar un link válido de LottieFiles

# CSS para Efecto "Glassmorphism" y Colores de Luna
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at top right, #0B1026, #000000);
    }
    div[data-testid="stMetricValue"] {
        color: #F9D423 !important; /* Amarillo Luna */
    }
    .stMarkdown p {
        color: #E0E0E0;
    }
    /* Estilo para el input de chat */
    .stChatInputContainer {
        padding-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER PROFESIONAL CON LOTTIE ---
col_l, col_r = st.columns([1, 4])
with col_l:
    if lottie_moon:
        st_lottie(lottie_moon, height=100, key="moon_logo")
    else:
        # Círculo de respaldo si falla el link de Lottie
        st.markdown("<div style='width:80px; height:80px; background:#F9D423; border-radius:50%; box-shadow: 0 0 30px #F9D423;'></div>", unsafe_allow_html=True)

with col_r:
    st.title("LUNA: Safe Space")
    st.caption("AI-Powered Emotional Support Platform")

add_vertical_space(2) # Espaciado elegante

# --- DASHBOARD CON STYLE CARDS ---
st.subheader("📊 Your Emotional Insights")
c1, c2, c3 = st.columns(3)

with c1:
    st.metric(label="Current Stress", value="8/15", delta="-2 (Improving)")
with c2:
    st.metric(label="Weekly Avg", value="7.2", delta="Stable")
with c3:
    st.metric(label="Peak Stress", value="12", delta="High Alert", delta_color="inverse")

# Aplicamos el estilo de tarjetas modernas
style_metric_cards(background_color="rgba(255, 255, 255, 0.05)", border_left_color="#F9D423")

add_vertical_space(2)

# --- GRÁFICA INTERACTIVA (Corregida) ---
df = pd.DataFrame({'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], 'Stress': [4, 6, 5, 9, 12]})
fig = px.line(df, x='Day', y='Stress', template="plotly_dark", markers=True)
fig.update_traces(line_color='#F9D423', line_width=3) # Color amarillo Luna
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig, use_container_width=True)

# --- CHAT INTERFACE ---
st.divider()
st.subheader("💬 Chat with Shelly")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial de mensajes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de chat
if prompt := st.chat_input("How are you feeling today?"):
    # Mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Simulación de respuesta (Aquí conectarás la API de Google AI Studio después)
    with st.chat_message("assistant"):
        response = "I'm here to listen. You can tell me anything about your day. ✨"
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
import streamlit as st
import pandas as pd
import plotly.express as px

# --- MOON-STYLE INTERFACE DESIGN ---
st.set_page_config(page_title="Luna Safe Space", layout="wide")

# Inject CSS for a dark, modern look
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at center, #1a2a6c, #000000);
        color: white;
    }
    .stMetric {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 15px;
        border: 1px solid #f9d423;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("🌙 LUNA: Your Safe Space")
st.write("Welcome back! Let's check your emotional balance today.")

# --- MAIN BODY (FRONTEND) ---
col1, col2, col3 = st.columns(3)

# These are dummy (fake) data; we will replace them when you have your friend's code
with col1:
    st.metric(label="Current Stress", value="8/15", delta="-2")
with col2:
    st.metric(label="Weekly Average", value="7.2", delta="Normal")
with col3:
    st.metric(label="Peak Stress", value="12", delta="High", delta_color="inverse")

# --- TREND GRAPH ---
st.subheader("📈 Stress Trend")
# Create sample data so you can see how the chart looks
data = pd.DataFrame({
    'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
    'Level': [4, 6, 5, 9, 12]
})
fig = px.line(data, x='Day', y='Level', title="Emotional Journey", template="plotly_dark")
fig.update_traces(line_color='#f9d423')  # Luna yellow color
st.plotly_chart(fig, use_container_width=True)

# --- CHAT INTERFACE ---
st.subheader("💬 Chat with Shelly")
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Text input
if prompt := st.chat_input("How are you feeling?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # This is where your friend's AI code will go
    response = "I am a placeholder. When your friend shares the code, I will be a real AI!"
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

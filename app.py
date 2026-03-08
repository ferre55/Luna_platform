import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.metric_cards import style_metric_cards
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Luna | Safe Space",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# HEADER (NO INDENTAR NADA)
# ---------------------------------------------------------
st.markdown("""
<style>

.stApp {
    background: radial-gradient(circle at 20% 30%, #1a1f3b, #0b0e1f 70%, #000000);
    color: white;
    font-family: 'Poppins', sans-serif;
}

.luna-container {
    width: 100%;
    height: 430px;
    position: relative;
    overflow: hidden;
}

.moon {
    width: 200px;
    height: 200px;
    background: #f9d423;
    border-radius: 50%;
    margin: 0 auto;
    margin-top: 20px;
    box-shadow: 0 0 60px #f9d423aa;
    z-index: 5;
}

.star {
    position: absolute;
    width: 10px;
    height: 10px;
    background: #f9d423;
    border-radius: 50%;
    box-shadow: 0 0 12px #f9d423;
}

.star1 { top: 40px; left: 18%; }
.star2 { top: 120px; right: 22%; }
.star3 { top: 200px; left: 12%; }
.star4 { top: 260px; right: 18%; }

.luna-title {
    position: absolute;
    top: 240px;
    width: 100%;
    text-align: center;
    font-size: 95px;
    font-weight: 900;
    letter-spacing: 10px;
    color: white;
    text-shadow: 0px 0px 25px rgba(255,255,255,0.5);
    z-index: 10;
}

.x-mark {
    position: absolute;
    font-size: 45px;
    color: #ff5fa2;
    font-weight: bold;
    z-index: 10;
}

.x1 { top: 310px; left: 20%; transform: rotate(15deg); }
.x2 { top: 330px; right: 20%; transform: rotate(-10deg); }

.arrow {
    position: absolute;
    font-size: 60px;
    color: #ff5fa2;
    top: 360px;
    left: 15%;
    transform: rotate(-20deg);
    z-index: 10;
}

</style>

<div class="luna-container">

<div class="moon"></div>

<div class="star star1"></div>
<div class="star star2"></div>
<div class="star star3"></div>
<div class="star star4"></div>

<div class="luna-title">LUNA</div>

<div class="x-mark x1">X</div>
<div class="x-mark x2">X</div>

<div class="arrow">↘</div>

</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# METRICS
# ---------------------------------------------------------
st.subheader("📊 Your Emotional Insights")

col1, col2, col3 = st.columns(3)

col1.metric("Current Stress", "8/15", "-2 (Improving)")
col2.metric("Weekly Avg", "7.2", "Stable")
col3.metric("Peak Stress", "12", "High Alert", delta_color="inverse")

style_metric_cards(
    background_color="rgba(255, 255, 255, 0.05)",
    border_left_color="#F9D423"
)

add_vertical_space(2)

# ---------------------------------------------------------
# GRAPH
# ---------------------------------------------------------
df = pd.DataFrame({
    'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
    'Stress': [4, 6, 5, 9, 12]
})

fig = px.line(
    df,
    x='Day',
    y='Stress',
    title="Your Emotional Journey",
    template="plotly_dark",
    markers=True
)

fig.update_traces(line_color='#F9D423', line_width=3)
fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# CHAT
# ---------------------------------------------------------
st.divider()
st.subheader("💬 Chat with Shelly")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("How are you feeling today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    response = "I'm here to listen. You can tell me anything about your day. ✨"
    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.markdown(response)

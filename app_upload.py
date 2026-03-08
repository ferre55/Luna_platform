import streamlit as st
import pandas as pd
import os
import google.generativeai as genai
from dotenv import load_dotenv
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.metric_cards import style_metric_cards
import plotly.express as px

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Luna | Safe Space",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# LUNA HEADER DESIGN
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
    background: #f0e279;
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

/* Extra UI styling from your friend */
.stButton>button {
    width: 100%;
    border-radius: 20px;
    border: 1px solid #A8E6CF;
    color: #2F4F4F;
    height: 3em;
    font-weight: bold;
}
.stProgress > div > div > div > div {
    background-color: #A8E6CF;
}
div.row-widget.stRadio > div {
    flex-direction: row;
    justify-content: center;
    gap: 20px;
    padding: 10px;
}
div.row-widget.stRadio [data-testid="stWidgetLabel"] {
    font-size: 1.2rem;
    font-weight: bold;
    margin-bottom: 10px;
}
div[data-testid="stMarkdownContainer"] p {
    font-size: 1.1rem;
}
.stChatMessage {
    border-radius: 15px;
    margin-bottom: 10px;
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
# GEMINI CONFIG
# ---------------------------------------------------------
load_dotenv()
api_key_from_env = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key_from_env)
MODEL_NAME = "gemini-1.5-flash"

# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------
def trigger_emergency_email(user_name, contact_name, contact_email):
    return f"💌 Notification: Emergency email sent to {contact_name} ({contact_email})"

# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {
        "name": "", "gender": "Other", "password": "",
        "family_name": "", "family_phone": "", "family_email": "",
        "friend_name": "", "friend_phone": "", "friend_email": ""
    }
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'total_score' not in st.session_state:
    st.session_state.total_score = 0
if 'chat_mode' not in st.session_state:
    st.session_state.chat_mode = False
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'history' not in st.session_state:
    st.session_state.history = [4, 7, 5, 8]

# ---------------------------------------------------------
# QUESTIONS
# ---------------------------------------------------------
questions = [
    {"q": "1. Less joy right now?", "options": ["🙂 No", "😐 A little", "😟 Yes", "😞 A lot"]},
    {"q": "2. Feeling low right now?", "options": ["🙂 No", "😐 A little", "😟 Yes", "😞 A lot"]},
    {"q": "3. Feeling anxious right now?", "options": ["🙂 No", "😐 A little", "😟 Yes", "😣 A lot"]},
    {"q": "4. Racing thoughts right now?", "options": ["🙂 No", "😐 A little", "😟 Yes", "😣 A lot"]},
    {"q": "5. Need support right now?", "options": ["🌱 No", "🤍 Maybe", "🆘 Yes", "🚨 Need help now"]}
]

# ---------------------------------------------------------
# AUTH / NAVIGATION
# ---------------------------------------------------------
if not st.session_state.logged_in:
    st.title("🌿 Safe Space")
    tab1, tab2 = st.tabs(["🔒 Login", "📝 Register"])
    
    with tab1:
        l_user = st.text_input("Username", key="l_user_in")
        l_pwd = st.text_input("Password", type="password", key="l_pwd_in")
        if st.button("Login"):
            if l_user == st.session_state.user_profile['name'] and l_pwd == st.session_state.user_profile['password']:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid credentials. Please register first.")
                
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            new_name = st.text_input("Username", key="reg_name")
        with col2:
            new_pwd = st.text_input("Create Password", type="password", key="reg_pwd")
        new_gender = st.selectbox("Gender", ["Female", "Male", "Non-binary", "Other"], key="reg_gender")
        
        st.subheader("👨‍👩‍👧 Emergency Contacts")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Family**")
            f_n = st.text_input("Name", key="reg_f_n")
            f_p = st.text_input("Phone", key="reg_f_p")
            f_e = st.text_input("Email", key="reg_f_e")
        with c2:
            st.markdown("**Friend**")
            fr_n = st.text_input("Name", key="reg_fr_n")
            fr_p = st.text_input("Phone", key="reg_fr_p")
            fr_e = st.text_input("Email", key="reg_fr_e")
            
        if st.button("Complete Registration"):
            st.session_state.user_profile.update({
                "name": new_name,
                "password": new_pwd,
                "gender": new_gender,
                "family_name": f_n,
                "family_phone": f_p,
                "family_email": f_e,
                "friend_name": fr_n,
                "friend_phone": fr_p,
                "friend_email": fr_e
            })
            st.success("Registered! You can login now.")

else:
    st.sidebar.title(f"Hi, {st.session_state.user_profile['name']}! 🌿")
    page = st.sidebar.radio("Navigation", ["Check-in", "My Profile"])
    if st.sidebar.button("Sign Out"):
        st.session_state.logged_in = False
        st.rerun()

    # -----------------------------------------------------
    # CHECK-IN FLOW
    # -----------------------------------------------------
    if page == "Check-in":
        if not st.session_state.chat_mode:
            st.title("🌿 Daily Check-in")
            st.progress(st.session_state.step / len(questions))
            if st.session_state.step < len(questions):
                q_item = questions[st.session_state.step]
                st.subheader(q_item["q"])
                choice = st.radio(
                    "Choose your current state:",
                    q_item["options"],
                    index=None,
                    horizontal=True,
                    key=f"q{st.session_state.step}"
                )
                if st.button("Confirm and Next ➔"):
                    if choice:
                        st.session_state.total_score += {
                            opt: i for i, opt in enumerate(q_item["options"])
                        }[choice]
                        st.session_state.step += 1
                        st.rerun()
            else:
                st.session_state.history.append(st.session_state.total_score)
                st.session_state.chat_mode = True
                st.rerun()
        else:
            st.title("💬 Your Support Space")
            
            # --- Tracking Dashboard (with your style) ---
            with st.expander("📊 Detailed Emotional Tracking", expanded=True):
                avg_score = sum(st.session_state.history) / len(st.session_state.history)
                max_score = max(st.session_state.history)
                
                m1, m2, m3 = st.columns(3)
                m1.metric("Current Score", f"{st.session_state.total_score}/15")
                m2.metric("Average Stress", f"{avg_score:.1f}")
                m3.metric("Peak Stress", f"{max_score}")
                
                style_metric_cards(
                    background_color="rgba(255, 255, 255, 0.05)",
                    border_left_color="#F9D423"
                )

                st.divider()

                col_chart1, col_chart2 = st.columns([2, 1])
                
                with col_chart1:
                    st.write("📈 **Stress Trend (History)**")
                    df_line = pd.DataFrame({
                        "Record": [f"Day {i+1}" for i in range(len(st.session_state.history))],
                        "Stress Level": st.session_state.history
                    }).set_index("Record")
                    st.line_chart(df_line)
                
                with col_chart2:
                    st.write("🌟 **Quick Summary**")
                    def classify_mood(s):
                        if s <= 4:
                            return "You're all good 🙂", "You're doing great! Keep it up."
                        elif s <= 8:
                            return "You're too Tired 😐", "It's been a bit long. Remember to rest."
                        else:
                            return "Heavy 😞", "You've been through a lot. Be kind to yourself."
                    
                    status_label, tip = classify_mood(avg_score)
                    
                    if "good" in status_label:
                        st.success(f"Overall: {status_label}")
                    elif " Tired" in status_label:
                        st.warning(f"Overall: {status_label}")
                    else:
                        st.error(f"Overall: {status_label}")
                    
                    st.write(tip)

                st.caption("✨ Tips: Higher scores indicate times you might need more self-care or support.")
            
            # Chat history
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

            # Chat input
            if prompt := st.chat_input("Talk to me..."):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)
                
                with st.spinner("Processing..."):
                    risk_keywords = ["suicide", "sucide", "dead", "die", "kill", "自殺", "想死"]
                    if any(word in prompt.lower() for word in risk_keywords):
                        p = st.session_state.user_profile
                        status_f = trigger_emergency_email(p['name'], p['family_name'], p['family_email'])
                        status_fr = trigger_emergency_email(p['name'], p['friend_name'], p['friend_email'])
                        ai_text = (
                            f"🚨 **{p['name']}, I am deeply concerned about what you just shared.** \n\n"
                            f"Your life matters immensely, and it takes so much courage to speak your pain. "
                            f"Because I care about your safety, I've sent a notification to your support system: "
                            f"**{p['family_name']}** and **{p['friend_name']}**.\n\n"
                            f"Please reach out to them now, or call a local crisis hotline. You don't have to carry this alone.\n\n"
                            f"{status_f}\n{status_fr}"
                        )
                    else:
                        persona = (
                            f"Counselor. User: {st.session_state.user_profile['name']}, "
                            f"Score: {st.session_state.total_score}/15. "
                            f"Be warm and supportive but concise."
                        )
                        try:
                            model = genai.GenerativeModel(MODEL_NAME)
                            response = model.generate_content(f"{persona}\n\nUser: {prompt}")
                            ai_text = response.text
                        except Exception:
                            ai_text = "I'm here for you, but I'm having trouble connecting. Let's try again."
                
                st.session_state.messages.append({"role": "assistant", "content": ai_text})
                with st.chat_message("assistant"):
                    st.markdown(ai_text)
            
            if st.button("Restart Test"):
                st.session_state.step = 0
                st.session_state.total_score = 0
                st.session_state.chat_mode = False
                st.session_state.messages = []
                st.rerun()

    # -----------------------------------------------------
    # PROFILE PAGE
    # -----------------------------------------------------
    elif page == "My Profile":
        st.title("👤 Your Safety Profile")
        with st.form("profile_form"):
            u_name = st.text_input("Your Name", value=st.session_state.user_profile['name'], key="pf_name")
            u_pwd = st.text_input("Password", value=st.session_state.user_profile['password'], type="password", key="pf_pwd")
            u_gender = st.selectbox(
                "Gender",
                ["Female", "Male", "Non-binary", "Other"],
                index=["Female", "Male", "Non-binary", "Other"].index(st.session_state.user_profile['gender']),
                key="pf_gender"
            )
            
            st.divider()
            colA, colB = st.columns(2)
            with colA:
                st.markdown("**Family Member**")
                f_name = st.text_input("Family Name", value=st.session_state.user_profile['family_name'], key="pf_f_n")
                f_phone = st.text_input("Family Phone", value=st.session_state.user_profile['family_phone'], key="pf_f_p")
                f_email = st.text_input("Family Email", value=st.session_state.user_profile['family_email'], key="pf_f_e")
            with colB:
                st.markdown("**Trusted Friend**")
                fr_name = st.text_input("Friend Name", value=st.session_state.user_profile['friend_name'], key="pf_fr_n")
                fr_phone = st.text_input("Friend Phone", value=st.session_state.user_profile['friend_phone'], key="pf_fr_p")
                fr_email = st.text_input("Friend Email", value=st.session_state.user_profile['friend_email'], key="pf_fr_e")
            
            if st.form_submit_button("Save All Changes"):
                st.session_state.user_profile.update({
                    "name": u_name,
                    "password": u_pwd,
                    "gender": u_gender,
                    "family_name": f_name,
                    "family_phone": f_phone,
                    "family_email": f_email,
                    "friend_name": fr_name,
                    "friend_phone": fr_phone,
                    "friend_email": fr_email
                })
                st.success("Profile updated! 🌿")

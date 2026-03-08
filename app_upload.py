import streamlit as st
import pandas as pd
import os # for github
from google import genai
from google.genai import types
from dotenv import load_dotenv # for github reading .env file

# 1. API Configuration---
load_dotenv()

api_key_from_env = os.getenv("GOOGLE_API_KEY")

client = genai.Client(
    api_key=api_key_from_env,
    http_options=types.HttpOptions(api_version="v1")
)

#2. Function Definitions ---
def trigger_emergency_email(user_name, contact_name, contact_email):
    return f"💌 Notification: Emergency email sent to {contact_name} ({contact_email})"

st.set_page_config(page_title="Safe Space", page_icon="🌿", layout="centered")

#  UI Styling (進階美化：放大選項框框) ---
st.markdown("""
    <style>
    /* 讓按鈕跟輸入框更有質感 */
    .stButton>button { width: 100%; border-radius: 20px; border: 1px solid #A8E6CF; color: #2F4F4F; height: 3em; font-weight: bold; }
    .stProgress > div > div > div > div { background-color: #A8E6CF; }
    
    /* 重點：放大 Radio Button 的選項，讓它像大框框 */
    div.row-widget.stRadio > div { flex-direction:row; justify-content: center; gap: 20px; padding: 10px; }
    div.row-widget.stRadio [data-testid="stWidgetLabel"] { font-size: 1.2rem; font-weight: bold; margin-bottom: 10px; }
    
    /* 讓選項文字變大 */
    div[data-testid="stMarkdownContainer"] p { font-size: 1.1rem; }
    
    /* 聊天氣泡微調 */
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Initialize Session State ---
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
# 初始歷史紀錄
if 'history' not in st.session_state:
    st.session_state.history = [4, 7, 5, 8] 

# Dynamic Model Detection
if 'usable_model' not in st.session_state:
    try:
        for m in client.models.list():
            actions = getattr(m, "supported_actions", []) or getattr(m, "supported_generation_methods", [])
            if "generateContent" in actions:
                st.session_state.usable_model = m.name.split("/")[-1]
                break
    except:
        st.session_state.usable_model = "gemini-1.5-flash"

# 4. Question Definitions ---
questions = [
    {"q": "1. Less joy right now?", "options": ["🙂 No", "😐 A little", "😟 Yes", "😞 A lot"]},
    {"q": "2. Feeling low right now?", "options": ["🙂 No", "😐 A little", "😟 Yes", "😞 A lot"]},
    {"q": "3. Feeling anxious right now?", "options": ["🙂 No", "😐 A little", "😟 Yes", "😣 A lot"]},
    {"q": "4. Racing thoughts right now?", "options": ["🙂 No", "😐 A little", "😟 Yes", "😣 A lot"]},
    {"q": "5. Need support right now?", "options": ["🌱 No", "🤍 Maybe", "🆘 Yes", "🚨 Need help now"]}
]

# 5. Navigation Logic ---
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
            f_n = st.text_input("Name", key="reg_f_n"); f_p = st.text_input("Phone", key="reg_f_p"); f_e = st.text_input("Email", key="reg_f_e")
        with c2:
            st.markdown("**Friend**")
            fr_n = st.text_input("Name", key="reg_fr_n"); fr_p = st.text_input("Phone", key="reg_fr_p"); fr_e = st.text_input("Email", key="reg_fr_e")
            
        if st.button("Complete Registration"):
            st.session_state.user_profile.update({"name": new_name, "password": new_pwd, "gender": new_gender, "family_name": f_n, "family_phone": f_p, "family_email": f_e, "friend_name": fr_n, "friend_phone": fr_p, "friend_email": fr_e})
            st.success("Registered! You can login now.")

else:
    st.sidebar.title(f"Hi, {st.session_state.user_profile['name']}! 🌿")
    page = st.sidebar.radio("Navigation", ["Check-in", "My Profile"])
    if st.sidebar.button("Sign Out"):
        st.session_state.logged_in = False
        st.rerun()

    if page == "Check-in":
        if not st.session_state.chat_mode:
            st.title("🌿 Daily Check-in")
            st.progress(st.session_state.step / len(questions))
            if st.session_state.step < len(questions):
                q_item = questions[st.session_state.step]
                st.subheader(q_item["q"])
                # 這裡選項會因為上面的 CSS 變大
                choice = st.radio("Choose your current state:", q_item["options"], index=None, horizontal=True, key=f"q{st.session_state.step}")
                if st.button("Confirm and Next ➔"):
                    if choice:
                        st.session_state.total_score += {opt: i for i, opt in enumerate(q_item["options"])}[choice]
                        st.session_state.step += 1
                        st.rerun()
            else:
                st.session_state.history.append(st.session_state.total_score)
                st.session_state.chat_mode = True
                st.rerun()
        else:
            st.title("💬 Your Support Space")
            
            # --- 強化版 Tracking Dashboard (Shelly 優化版) ---
            with st.expander("📊 Detailed Emotional Tracking", expanded=True):
                # 第一行：使用 Metric 顯示重點數據 (這部分很棒，我們保留)
                avg_score = sum(st.session_state.history) / len(st.session_state.history)
                max_score = max(st.session_state.history)
                
                m1, m2, m3 = st.columns(3)
                m1.metric("Current Score", f"{st.session_state.total_score}/15")
                m2.metric("Average Stress", f"{avg_score:.1f}")
                m3.metric("Peak Stress", f"{max_score}")
                
                st.divider()

                # 第二行：趨勢圖 與 文字總結 並排
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
                    # 將分數分類為標籤，並直接顯示文字卡片
                    def classify_mood(s):
                        if s <= 4: return "You're all good 🙂", "You're doing great! Keep it up."
                        elif s <= 8: return "You're too Tired 😐", "It's been a bit long. Remember to rest."
                        else: return "Heavy 😞", "You've been through a lot. Be kind to yourself."
                    
                    status_label, tip = classify_mood(avg_score)
                    
                    # 根據狀態顯示不同顏色的小卡片
                    if "good" in status_label:
                        st.success(f"Overall: {status_label}")
                    elif " Tired" in status_label:
                        st.warning(f"Overall: {status_label}")
                    else:
                        st.error(f"Overall: {status_label}")
                    
                    st.write(tip)

                st.caption("✨ Tips: Higher scores indicate times you might need more self-care or support.")
            
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]): st.markdown(msg["content"])

            if prompt := st.chat_input("Talk to me..."):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"): st.markdown(prompt)
                
                with st.spinner("Processing..."):
                    risk_keywords = ["suicide", "sucide", "dead", "die", "kill", "自殺", "想死"]
                    if any(word in prompt.lower() for word in risk_keywords):
                        # --- 恢復溫暖的敏感字回覆 ---
                        p = st.session_state.user_profile
                        status_f = trigger_emergency_email(p['name'], p['family_name'], p['family_email'])
                        status_fr = trigger_emergency_email(p['name'], p['friend_name'], p['friend_email'])
                        ai_text = (f"🚨 **{p['name']}, I am deeply concerned about what you just shared.** \n\n"
                                   f"Your life matters immensely, and it takes so much courage to speak your pain. "
                                   f"Because I care about your safety, I've sent a notification to your support system: "
                                   f"**{p['family_name']}** and **{p['friend_name']}**.\n\n"
                                   f"Please reach out to them now, or call a local crisis hotline. You don't have to carry this alone.\n\n"
                                   f"{status_f}\n{status_fr}")
                    else:
                        persona = f"Counselor. User: {st.session_state.user_profile['name']}, Score: {st.session_state.total_score}/15. Be warm and supportive but concise."
                        try:
                            response = client.models.generate_content(model=st.session_state.usable_model, contents=f"{persona}\n\nUser: {prompt}")
                            ai_text = response.text
                        except: ai_text = "I'm here for you, but I'm having trouble connecting. Let's try again."
                
                st.session_state.messages.append({"role": "assistant", "content": ai_text})
                with st.chat_message("assistant"): st.markdown(ai_text)
            
            if st.button("Restart Test"):
                st.session_state.step = 0; st.session_state.total_score = 0; st.session_state.chat_mode = False; st.session_state.messages = []
                st.rerun()

    elif page == "My Profile":
        st.title("👤 Your Safety Profile")
        with st.form("profile_form"):
            u_name = st.text_input("Your Name", value=st.session_state.user_profile['name'], key="pf_name")
            u_pwd = st.text_input("Password", value=st.session_state.user_profile['password'], type="password", key="pf_pwd")
            u_gender = st.selectbox("Gender", ["Female", "Male", "Non-binary", "Other"], 
                                    index=["Female", "Male", "Non-binary", "Other"].index(st.session_state.user_profile['gender']), key="pf_gender")
            
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
                    "name": u_name, "password": u_pwd, "gender": u_gender,
                    "family_name": f_name, "family_phone": f_phone, "family_email": f_email,
                    "friend_name": fr_name, "friend_phone": fr_phone, "friend_email": fr_email
                })
                st.success("Profile updated! 🌿")
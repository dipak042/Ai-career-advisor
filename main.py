import streamlit as st
import requests
import time

# ---- Dummy user database ----
users = {
    "dipak": "hackathon",
    "test": "1234"
}

# ---- Session State ----
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---- AI Response (HuggingFace) ----
def get_ai_response(user_input):
    API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-small"
    headers = {"Authorization": "Bearer YOUR_HUGGINGFACE_API_KEY"}
    payload = {"inputs": user_input}
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=5)
        if response.status_code == 200:
            return response.json()[0]["generated_text"]
        else:
            return get_offline_ai_response(user_input)
    except:
        return get_offline_ai_response(user_input)

# ---- Offline Rule-Based AI (Improved) ----
def get_offline_ai_response(user_input):
    user_input = user_input.lower()
    if "internship" in user_input:
        return "💼 Focus on building projects, updating your resume, and networking online."
    elif "google" in user_input:
        return "🚀 Strengthen DSA, system design, and build real-world projects."
    elif "skill" in user_input:
        return "🛠️ Prioritize skills like Python, C++, AI, IoT, and cloud computing."
    elif "career" in user_input:
        return "🎯 Explore options based on your interests, strengths, and market trends."
    elif "resume" in user_input:
        return "📄 Keep it concise, highlight achievements, projects, internships, and skills."
    elif "job" in user_input:
        return "💼 Look for openings on LinkedIn, Internshala, and apply with a strong resume."
    elif "projects" in user_input:
        return "🛠️ Build real-world projects to showcase your skills on GitHub."
    else:
        return "🤖 Ask me about internships, skills, career paths, Google prep, or resume tips!"

# ---- CSS for colorful chat bubbles ----
st.markdown("""
<style>
.user-msg {
    background-color: #90EE90;
    padding: 10px;
    border-radius: 10px;
    margin: 5px;
    color: #000000;
}
.ai-msg {
    background-color: #ADD8E6;
    padding: 10px;
    border-radius: 10px;
    margin: 5px;
    color: #000000;
}
</style>
""", unsafe_allow_html=True)

# ---- Login / Sign-up Tabs ----
if not st.session_state.logged_in:
    st.title("🔐 AI Career Advisor Login")
    tab1, tab2 = st.tabs(["Login 🔑", "Sign Up 📝"])

    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login", key="login_btn"):
            if username in users and users[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Login Successful! Welcome {username} 👋")
                st.experimental_rerun()
            else:
                st.error("Invalid username or password ❌")

    with tab2:
        new_user = st.text_input("Choose a username", key="signup_user")
        new_pass = st.text_input("Choose a password", type="password", key="signup_pass")
        if st.button("Sign Up", key="signup_btn"):
            if new_user in users:
                st.error("Username already exists ❌")
            else:
                users[new_user] = new_pass
                st.success("Account created! Please login 🔑")

# ---- Main Chatbot App ----
else:
    st.title("🤖 AI Career & Skill Advisor")
    st.write(f"Welcome, **{st.session_state.username}** 👋")

    user_input = st.text_area("Ask your career/skill question:", key="user_input")

    if st.button("Get AI Advice"):
        if user_input.strip():
            # Add user message
            st.session_state.chat_history.append({"role": "user", "msg": user_input})

            # Typing animation
            with st.spinner("AI is thinking... 🤔"):
                time.sleep(1)  # simulate typing
                answer = get_ai_response(user_input)

            # Add AI response
            st.session_state.chat_history.append({"role": "ai", "msg": answer})
        else:
            st.warning("Please type a question.")

    # ---- Display Chat History with colorful bubbles ----
    if st.session_state.chat_history:
        st.markdown("---")
        for chat in st.session_state.chat_history[::-1]:
            if chat["role"] == "user":
                st.markdown(f'<div class="user-msg">You: {chat["msg"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="ai-msg">AI: {chat["msg"]}</div>', unsafe_allow_html=True)

    if st.button("Logout 🔒"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.chat_history = []
        st.experimental_rerun()

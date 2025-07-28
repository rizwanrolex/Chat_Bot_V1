import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai

# ✅ Load API key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# ✅ Setup Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# ✅ Load agency data once
with open("agency_data.txt", "r", encoding="utf-8") as file:
    agency_info = file.read()

# ✅ System instructions (used for every reply)
SYSTEM_PROMPT = f"""
You are a short, polite assistant working at an AI agency. 
You ONLY answer questions about AI, automation, chatbot development, and agency services.
If a question is outside this topic, reply:
"Sorry, I can only answer questions related to our AI services."

Agency Info:
{agency_info}
"""

def get_bot_response(user_input):
    """Generate a short response in 1-2 lines"""
    try:
        response = model.generate_content(f"{SYSTEM_PROMPT}\nUser: {user_input}\nBot:")
        return response.text.strip()
    except Exception as e:
        return f"❌ Error: {e}"


# ---------------- STREAMLIT UI ----------------
st.set_page_config(page_title="AI Agency Chatbot", page_icon="🤖")
st.title("🤖 AI Agency Chatbot")

st.markdown("💬 **Ask me anything about our AI services!**")

# ✅ Chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ✅ User input box
user_input = st.text_input("You:", placeholder="Type your message...")

if st.button("Send"):
    if user_input.strip() != "":
        with st.spinner("🤖 Thinking..."):
            reply = get_bot_response(user_input)
            # ✅ Save to chat history
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Bot", reply))

# ✅ Display chat history
for sender, message in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"**🧑 You:** {message}")
    else:
        st.markdown(f"**🤖 Bot:** {message}")

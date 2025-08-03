import streamlit as st
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Anxiva", page_icon="💬")
st.title("🧠 Anxiva — Your Friendly Companion")
st.markdown("A warm, safe place to talk. *(UK-based support)*")

# Initialize history
if "history" not in st.session_state:
    st.session_state.history = []

# Display the full chat
for sender, message in st.session_state.history:
    st.write(f"**{sender}:** {message}")

# Input box and send button
user_input = st.text_input("You:", key="input")
send_clicked = st.button("Send")

if send_clicked and user_input:
    st.session_state.history.append(("You", user_input))
    low = user_input.lower()

    # Crisis check
    if any(k in low for k in ["suicide", "self-harm", "hurt myself", "kill myself", "end my life"]):
        crisis = (
            "I’m really sorry you’re feeling this way. You deserve help right now.  \n"
            "- 📞 Samaritans (UK): 116 123  \n"
            "- 🖥️ https://www.samaritans.org  \n"
            "- 🚑 In immediate danger? Call 999."
        )
        st.session_state.history.append(("Anxiva", crisis))
    else:
        # Build messages for the API
        system_msg = {
            "role": "system",
            "content": (
                "You are Anxiva, a caring UK-based friend. "
                "Only respond to what the user explicitly shares. "
                "Offer UK crisis links only on self-harm or suicide mentions. "
                "Otherwise, follow the user’s lead."
            )
        }
        messages = [system_msg]
        for s, m in st.session_state.history:
            role = "user" if s == "You" else "assistant"
            messages.append({"role": role, "content": m})

        with st.spinner("Anxiva is thinking..."):
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.8,
                max_tokens=300
            )
        reply = resp.choices[0].message.content.strip()
        st.session_state.history.append(("Anxiva", reply))

    # Clear the input box
    st.session_state.input = ""

import streamlit as st
import openai
import os

# Fetch key
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Anixva", page_icon="🧠")
st.title("🧠 Anixva — Your Friendly Companion")
st.markdown("A warm, safe place to talk. *(UK-based support)*")

# --- Initialize history ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- Render past messages ---
for sender, msg in st.session_state.history:
    if sender == "You":
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**Anixva:** {msg}")

# --- Input & Send button ---
user_in = st.text_input("You:", key="inp")

if st.button("Send") and user_in:
    # Save user message
    st.session_state.history.append(("You", user_in))

    # Call OpenAI once
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You’re Anixva ... (your prompt here)"},
            *[
                {"role": "user" if s=="You" else "assistant", "content": m}
                for s,m in st.session_state.history
            ]
        ],
        max_tokens=300
    )
    ans = resp.choices[0].message.content.strip()

    # Save Anixva’s reply
    st.session_state.history.append(("Anixva", ans))

    # Clear input
    st.session_state.inp = ""

    # Rerun to show the new message
    st.experimental_rerun()

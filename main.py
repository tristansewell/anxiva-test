import streamlit as st
import openai
import os

# 🔐 Fetch your OpenAI key from the environment
openai.api_key = os.getenv("OPENAI_API_KEY")

# ─── Page setup ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Anixva", page_icon="🧠")
st.title("🧠 Anixva — Your Friendly Companion")
st.markdown("A warm, safe place to talk. *(UK-based support)*")

# ─── Persistence ────────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

# ─── Render past chat ─────────────────────────────────────────────────────────
for sender, message in st.session_state.history:
    if sender == "You":
        st.markdown(f"**You:** {message}")
    else:
        st.markdown(f"**Anixva:** {message}")

# ─── Input area ────────────────────────────────────────────────────────────────
user_input = st.text_input("You:", key="input")
send_clicked = st.button("Send")

# ─── On send ───────────────────────────────────────────────────────────────────
if send_clicked and user_input:
    # 1) Save user message
    st.session_state.history.append(("You", user_input))
    low = user_input.lower()

    # 2) Crisis keyword check (only now we give helplines)
    crisis_terms = ["suicide", "self-harm", "hurt myself", "kill myself", "end my life"]
    if any(term in low for term in crisis_terms):
        reply = (
            "I’m really sorry you’re feeling this way. You deserve help right now.\n\n"
            "If you ever feel you might harm yourself or are in crisis, please reach out immediately:\n"
            "- **Samaritans (UK & ROI):** call 116 123 or email jo@samaritans.org\n"
            "- **NHS 111 (option 2):** for urgent mental health support\n\n"
            "You don’t have to face this alone."
        )
        st.session_state.history.append(("Anixva", reply))

    else:
        # 3) Build the full message list, including system prompt + history
        system_msg = {
            "role": "system",
            "content": (
                "You are Anixva, a warm and emotionally supportive AI friend based in the UK. "
                "Validate the user’s feelings, ask open-ended questions, and gently guide the "
                "conversation without assuming. Only when the user mentions self-harm or suicide "
                "should you offer emergency helpline information. Use UK English spelling."
            )
        }
        messages = [system_msg]
        for sender, msg in st.session_state.history:
            role = "user" if sender == "You" else "assistant"
            messages.append({"role": role, "content": msg})

        # 4) Insert a placeholder and stream the completion in real-time
        placeholder = st.empty()
        full_reply = ""
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.8,
            stream=True,
        )
        for chunk in resp:
            delta = chunk["choices"][0]["delta"].get("content", "")
            full_reply += delta
            placeholder.markdown(f"**Anixva:** {full_reply}")

        # 5) Save the final assistant reply
        st.session_state.history.append(("Anixva", full_reply))

    # No need to manually reset st.session_state.input
    st.experimental_rerun()

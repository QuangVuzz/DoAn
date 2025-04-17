import streamlit as st

# Page setup
st.set_page_config(page_title="Parent Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 Kindergarten Parent Chatbot")
st.write("Hello dear parents! I'm the virtual assistant of the kindergarten. You can ask me anything related to class schedules, meals, learning hours, and more!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Rule-based response generator
def get_bot_response(message):
    message = message.lower()

    if "hello" in message or "hi" in message or "greetings" in message:
        return "Hello dear parent! How can I assist you today?"
    elif "meal" in message or "eat" in message or "lunch" in message:
        return "Today the children had rice, vegetable soup, and fresh fruit for dessert."
    elif "schedule" in message or "time" in message or "class time" in message:
        return "Classes start at 7:30 AM and end at 4:30 PM from Monday to Friday."
    elif "nap" in message or "sleep" in message:
        return "Children take a nap from 11:30 AM to 1:30 PM to recharge their energy."
    elif "play" in message or "activities" in message:
        return "Children enjoy activities like building blocks, drawing, storytelling, and outdoor games."
    elif "learn" in message or "curriculum" in message or "what do they learn":
        return "Our curriculum is designed to develop physical, intellectual, emotional, and language skills appropriate for preschool age."
    elif "thank you" in message or "thanks" in message:
        return "You're very welcome! I'm always here to help."
    elif "bye" in message or "goodbye" in message:
        return "Goodbye! Wishing you a lovely day ahead!"
    else:
        return "Sorry, I didn't quite understand that. Could you please rephrase your question?"

# Chat input form
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("✏️ Please enter your question:")
    submit = st.form_submit_button("Send")

# Process input
if submit and user_input:
    st.session_state.messages.append({"sender": "user", "text": user_input})
    bot_response = get_bot_response(user_input)
    st.session_state.messages.append({"sender": "bot", "text": bot_response})

# Display chat messages
for msg in st.session_state.messages:
    if msg["sender"] == "user":
        st.markdown(
            f"<div style='text-align:right; color:#155724; background-color:#d4edda; padding:8px; border-radius:10px; margin:4px 0;'>👨‍👩‍👧 {msg['text']}</div>",
            unsafe_allow_html=True)
    else:
        st.markdown(
            f"<div style='text-align:left; color:#0c5460; background-color:#cce5ff; padding:8px; border-radius:10px; margin:4px 0;'>🤖 {msg['text']}</div>",
            unsafe_allow_html=True)

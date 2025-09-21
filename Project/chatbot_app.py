"""import streamlit as st
import random
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load intents from JSON file
with open("intents.json", "r") as file:
    intents_data = json.load(file)

# Prepare data
all_phrases = []
all_intents = []

for intent in intents_data["intents"]:
    for phrase in intent["text"]:
        all_phrases.append(phrase)
        all_intents.append(intent["intent"])

# Vectorize user inputs
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(all_phrases)

# Chatbot logic
def get_bot_response(user_input):
    user_vec = vectorizer.transform([user_input])
    similarities = cosine_similarity(user_vec, X)
    best_match_index = similarities.argmax()
    matched_intent = all_intents[best_match_index]
    
    for intent in intents_data["intents"]:
        if intent["intent"] == matched_intent:
            return random.choice(intent["responses"])
    
    return "Sorry, I didn't understand that."

# Streamlit UI
st.set_page_config(page_title="DeKUT Chatbot", page_icon="🎓")
st.title("🎓 Ask Dedan - Chatbot")
st.markdown("Ask me anything about university services!")

user_input = st.text_input("You:", "")

if user_input:
    response = get_bot_response(user_input)
    st.markdown(f"**Bot 🤖:** {response}",unsafe_allow_html=True)
"""

import gradio as gr
import random
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load intents from JSON file
with open("intents.json", "r") as file:
    intents_data = json.load(file)

# Prepare data
all_phrases = []
all_intents = []

for intent in intents_data["intents"]:
    for phrase in intent["text"]:
        all_phrases.append(phrase)
        all_intents.append(intent["intent"])

# Vectorize user inputs
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(all_phrases)

# Chatbot logic
def get_bot_response(user_input, history):
    user_vec = vectorizer.transform([user_input])
    similarities = cosine_similarity(user_vec, X)
    best_match_index = similarities.argmax()
    matched_intent = all_intents[best_match_index]
    
    for intent in intents_data["intents"]:
        if intent["intent"] == matched_intent:
            return random.choice(intent["responses"])
    
    return "Sorry, I didn't understand that."

# Create Gradio interface
with gr.Blocks(title="🎓 Ask Dedan - Chatbot", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎓 Ask Dedan - Chatbot")
    gr.Markdown("Ask me anything about university services!")
    
    chatbot = gr.Chatbot(label="Conversation")
    msg = gr.Textbox(label="Your message")
    clear = gr.Button("Clear")
    
    def respond(message, chat_history):
        bot_message = get_bot_response(message, chat_history)
        chat_history.append((message, bot_message))
        return "", chat_history
    
    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)

# Launch the app
if __name__ == "__main__":
    demo.launch()

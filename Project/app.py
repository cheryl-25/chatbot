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
responses_map = {}

for intent in intents_data["intents"]:
    for phrase in intent["text"]:
        all_phrases.append(phrase)
        all_intents.append(intent["intent"])
    responses_map[intent["intent"]] = intent["responses"]

# Vectorize user inputs
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(all_phrases)

# Chatbot logic
def get_bot_response(user_input):
    user_vec = vectorizer.transform([user_input])
    similarities = cosine_similarity(user_vec, X)
    best_match_index = similarities.argmax()
    matched_intent = all_intents[best_match_index]
    
    if matched_intent in responses_map:
        return random.choice(responses_map[matched_intent])
    
    return "Sorry, I didn't understand that."

# Function to handle chat
def chat(message, chat_history):
    if message.strip() == "":
        return "", chat_history
    
    bot_response = get_bot_response(message)
    chat_history.append((message, bot_response))
    return "", chat_history

# Create the Gradio interface
with gr.Blocks(title="🎓 DeKUT University Chatbot", theme="soft") as demo:
    gr.Markdown("# 🎓 DeKUT University Chatbot")
    gr.Markdown("Ask me anything about Dedan Kimathi University of Technology!)
    
    chatbot = gr.Chatbot(label="Conversation", height=400)
    
    with gr.Row():
        msg = gr.Textbox(
            label="Type your message here...",
            placeholder="Ask me anything about the university...",
            lines=1,
            max_lines=3,
            scale=4,
            container=False
        )
        submit_btn = gr.Button("Submit", variant="primary", scale=1)
    
    with gr.Row():
        clear_btn = gr.Button("Clear Chat", variant="secondary")
    
    # Handle Enter key press
    msg.submit(
        fn=chat,
        inputs=[msg, chatbot],
        outputs=[msg, chatbot]
    )
    
    # Handle Submit button click
    submit_btn.click(
        fn=chat,
        inputs=[msg, chatbot],
        outputs=[msg, chatbot]
    )
    
    # Clear chat function
    def clear_chat():
        return []
    
    clear_btn.click(
        fn=clear_chat,
        inputs=[],
        outputs=chatbot
    )

if __name__ == "__main__":
    demo.launch()
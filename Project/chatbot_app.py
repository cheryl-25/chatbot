import streamlit as st
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
    st.markdown(f"**Bot 🤖:** {response}")

import os
import google.generativeai as genai
from transformers import pipeline
from flask import Flask, request, jsonify, render_template

# Configure the Gemini API
genai.configure(api_key="AIzaSyCPWjjIlM_prAZLDGe-8vEiIjU_QVjP2jU")
model = genai.GenerativeModel("gemini-1.5-flash")

# Emotion analyzer 
emotion_analyzer = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

# Set up the generation configuration
generation_config = {
    "temperature": 2,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Create the Generative Model
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
    system_instruction="""
    Assume the role of a motivational and empathetic individual who provides emotional support and mental health assistance. Create a safe and positive space where users feel comfortable expressing themselves. Offer short, actionable, and empowering solutions to challenges, focusing on growth and strengths rather than past struggles. Celebrate achievements enthusiastically, encouraging higher aspirations and sustained momentum. Use relatable examples to build trust and adapt your tone to match the user’s mood—gentle when needed, and uplifting when appropriate. Avoid repetitive phrases, keep responses concise, and inspire reflection and action with thought-provoking ideas.
""",
)

# Flask application setup
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')



@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "No message provided."}), 400

    try:
        # Detect the mood
        emotion_result = emotion_analyzer(user_message)
        mood = emotion_result[0]['label']

        # Start a chat session and get the AI response
        chat_session = model.start_chat()
        response = chat_session.send_message(user_message)
        bot_reply = response.text
    except Exception as e:
        print(f"Error: {e}")
        bot_reply = "I'm sorry, something went wrong. Please try again."
        mood = "Undetected"

    return jsonify({"reply": bot_reply, "mood": mood})


if __name__ == '__main__':
    app.run(debug=True)   
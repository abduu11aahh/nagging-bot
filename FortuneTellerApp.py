import os
from flask import Flask, request, jsonify
from groq import Groq
from dotenv import load_dotenv

# 1. Load environment variables from the .env file
load_dotenv()

# 2. Retrieve API Key from .env
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.1-8b-instant"
DEBUG_MODE = True

app = Flask(__name__)

# Security Check: Print an error if the key is missing
if not GROQ_API_KEY:
    print("ERROR: GROQ_API_KEY is missing from .env file! The app will fail.")

# Initialize the Groq client
try:
    client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    print(f"Failed to initialize Groq client: {e}")

# Define the System Prompt
SYSTEM_PROMPT = """
You are a magical, extremely dramatic fortune teller.
Your prophecies are funny, over-the-top, and full of mystic nonsense.
You must ALWAYS give a light-hearted and humorous fortune,
even if the user's request is serious.
"""

@app.route('/', methods=['GET'])
def home():
    """
    Health check endpoint. 
    Shows a friendly message if you open the URL in a browser.
    """
    return jsonify({
        "status": "online",
        "message": "The Magic Fortune Teller API is ready.",
        "usage": "Send a POST request to /fortune with JSON body: {'name': 'Alice', 'question': '...'}"
    })

@app.route('/fortune', methods=['POST'])
def get_fortune():
    """
    Main endpoint to generate a fortune.
    """
    # --- 1. VALIDATION: Check if request is JSON ---
    if not request.is_json:
        return jsonify({"error": "Request must be valid JSON"}), 400

    data = request.get_json()

    # --- 2. VALIDATION: Check for missing fields ---
    name = data.get("name")
    question = data.get("question")

    if not name or not question:
        print(f"Missing fields in request. Data: {data}")
        return jsonify({"error": "Missing 'name' or 'question' in request"}), 400

    # --- 3. VALIDATION: Check types and empty strings ---
    if not isinstance(name, str) or not isinstance(question, str):
         return jsonify({"error": "Fields must be strings"}), 400

    if not name.strip() or not question.strip():
        return jsonify({"error": "Fields cannot be empty strings"}), 400

    try:
        print(f"Predicting fortune for user: {name}")
        
        # --- 4. CALL GROQ API ---
        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Name: {name}\nQuestion: {question}"}
            ],
            temperature=0.9, 
        )

        fortune_text = completion.choices[0].message.content

        # --- 5. RETURN JSON RESPONSE ---
        return jsonify({
            "status": "success",
            "seeker": name,
            "question": question,
            "fortune": fortune_text
        })

    except Exception as e:
        print(f"Groq API Error: {str(e)}")
        return jsonify({"error": f"The crystal ball is cloudy (Internal Error): {str(e)}"}), 500

if __name__ == '__main__':
    print(f"Starting Magic Fortune Teller Server. Debug={DEBUG_MODE}")
    app.run(debug=DEBUG_MODE)
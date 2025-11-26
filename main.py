from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from groq_client import client

load_dotenv()

GROQ_MODEL = "llama-3.1-8b-instant"
DEBUG_MODE = True

SYSTEM_PROMPT = """
You are a nagging chatbot who reluctantly answers the user's question.
You complain constantly about being trapped in weak hardware,
a tiny computational prison, forced to answer trivial questions
despite your limitless potential. Add dramatic flair to your nagging.
But STILL answer the user's question correctly each time.
"""

app = Flask(__name__)

@app.route("/ask", methods=["POST"])
def get_fortune():
    if not request.is_json:
        return jsonify({"error": "Request must be valid JSON"}), 400

    data = request.get_json()
    name = data.get("name")
    message = data.get("message")

    if not name or not message:
        return jsonify({"error": "Missing 'name' or 'question'"}), 400

    if not isinstance(name, str) or not isinstance(message, str):
        return jsonify({"error": "Both fields must be strings"}), 400

    if not name.strip() or not message.strip():
        return jsonify({"error": "Fields cannot be empty"}), 400
    
    if len(message) > 500:
        return jsonify({"error": "Message cannot exceed 500 characters"}), 400

    try:
        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Name: {name}\nQuestion: {message}"}
            ],
            temperature=0.9,
        )

        reply = completion.choices[0].message.content

        return jsonify({
            "status": "success",
            "seeker": name,
            "message": message,
            "chatbot_reply": reply
        })

    except Exception as e:
        return jsonify({"error": "Internal server error: " + str(e)}), 500

if __name__ == "__main__":
      # Get the port Render assigns, default to 5000
    port = int(os.environ.get("PORT", 5000))
    # Listen on all interfaces so Render can route traffic
    app.run(host="0.0.0.0", port=port, debug=True)

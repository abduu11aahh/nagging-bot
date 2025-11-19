Magic Fortune Teller API 

A Flask-based API that uses the Groq AI Cloud to generate humorous, dramatic fortunes.

Setup

Install dependencies: pip install -r requirements.txt

Create a .env file with your GROQ_API_KEY.

Run the app: python app.py

Usage

POST to /fortune with JSON:

{
  "name": "Alice",
  "question": "Will I be rich?"
}

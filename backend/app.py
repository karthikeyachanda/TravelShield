from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mail import Mail
from database import db
from routes import register_routes
import google.generativeai as genai
import os

# create flask app
app = Flask(__name__)

# enable CORS
CORS(app)

# 🔑 GEMINI API KEY (Hardcoded for guaranteed access)
genai.configure(api_key="")


# database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///travelshield.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# EMAIL CONFIGURATION (FOR SOS ALERTS)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "karthikeya201620@gmail.com"
app.config['MAIL_PASSWORD'] = ""
app.config['MAIL_DEFAULT_SENDER'] = "24211a0593@bvrit.ac.in"


# initialize mail
mail = Mail(app)

# connect database with app
db.init_app(app)

# register routes
register_routes(app)

# ✅ CHATBOT ROUTE (STRICTLY GEMINI ONLY)
@app.route("/ai-chat", methods=["POST"])
def ai_chat():
    data = request.json
    question = data.get("question")

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        prompt = f"You are a travel safety assistant. Answer safely and helpfully:\n\n{question}"
        response = model.generate_content(prompt)
        return jsonify({"answer": response.text})
    except Exception as e:
        return jsonify({"answer": f"Gemini API Error: {str(e)}"})
@app.route("/")
def home():
    return {
        "status": "success",
        "message": "Travel Shield Backend Running"
    }


# create database tables
with app.app_context():
    db.create_all()


# ✅ RUN SERVER (ONLY ONE BLOCK)
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
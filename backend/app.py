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

# 🔑 GEMINI API KEY
# 🔑 GEMINI API KEY (Safely loaded from Environment)
genai.configure(api_key=os.getenv("GEMINI_API_KEY", "YOUR_KEY_HERE"))


# database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///travelshield.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# EMAIL CONFIGURATION (FOR SOS ALERTS)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "karthikeya201620@gmail.com"
app.config['MAIL_PASSWORD'] = "ftisuqvkuxtehzkm"
app.config['MAIL_DEFAULT_SENDER'] = "24211a0593@bvrit.ac.in"


# initialize mail
mail = Mail(app)

# connect database with app
db.init_app(app)

# register routes
register_routes(app)


# ✅ CHATBOT ROUTE (NEW)
@app.route("/ai-chat", methods=["POST"])
def ai_chat():
    data = request.json
    question = data.get("question")

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        prompt = f"You are a travel safety assistant. Answer the following question safely and helpfully:\n\n{question}"
        response = model.generate_content(prompt)

        answer = response.text

        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"answer": str(e)})



# test route
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
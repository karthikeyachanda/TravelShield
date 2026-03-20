from flask import request, jsonify
from models import User, Incident
from database import db
import google.generativeai as genai
genai.configure(api_key="")



def register_routes(app):

    # REGISTER API
    @app.route("/register", methods=["POST"])
    def register():

        data = request.get_json()

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        new_user = User(
            name=name,
            email=email,
            password=password
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "message": "User registered successfully"
        })


    # LOGIN API
    @app.route("/login", methods=["POST"])
    def login():

        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            return jsonify({
                "message": "Login successful",
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email
                }
            })

        return jsonify({
            "message": "Invalid email or password"
        }), 401


    # SOS EMERGENCY API (EMAIL ALERT)
    @app.route("/sos", methods=["POST"])
    def sos():

        from app import mail
        from flask_mail import Message

        data = request.get_json()

        user_id = data.get("user_id")
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        user = User.query.get(user_id)

        msg = Message(
            subject="TRAVEL SHIELD SOS ALERT",
            sender="karthikeya201620@gmail.com",
            recipients=["24211a0593@bvrit.ac.in"],
            reply_to=user.email
        )

        msg.body = f"""
Emergency SOS Alert!

User Name: {user.name}
User Email: {user.email}

Live Location:
Latitude: {latitude}
Longitude: {longitude}

Google Maps Link:
https://www.google.com/maps?q={latitude},{longitude}
"""

        mail.send(msg)

        return jsonify({
            "status": "SOS alert sent with live location"
        })


    # INCIDENT REPORTING API
    @app.route("/report-incident", methods=["POST"])
    def report_incident():

        data = request.get_json()

        user_id = data.get("user_id")
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        description = data.get("description")

        incident = Incident(
            user_id=user_id,
            latitude=latitude,
            longitude=longitude,
            description=description
        )

        db.session.add(incident)
        db.session.commit()

        return jsonify({
            "message": "Incident reported successfully"
        })


    # RISK SCORE API
    @app.route("/risk-score", methods=["POST"])
    def risk_score():

        data = request.get_json()

        latitude = data.get("latitude")
        longitude = data.get("longitude")

        import random
        risk_score = random.randint(1, 100)

        if risk_score < 30:
            status = "Safe Area"
        elif risk_score < 70:
            status = "Moderate Risk"
        else:
            status = "High Risk"

        return jsonify({
            "latitude": latitude,
            "longitude": longitude,
            "risk_score": risk_score,
            "status": status
        })


    # GET ALL INCIDENTS
    @app.route("/incidents", methods=["GET"])
    def get_incidents():

        incidents = Incident.query.all()

        incident_list = []

        for incident in incidents:
            incident_list.append({
                "id": incident.id,
                "user_id": incident.user_id,
                "latitude": incident.latitude,
                "longitude": incident.longitude,
                "description": incident.description
            })

        return jsonify(incident_list)
    
    @app.route("/ai-chat", methods=["POST"])
    def ai_chat():

        data = request.get_json()
        question = data.get("question")

        try:
            model = genai.GenerativeModel("gemini-1.5-flash-latest")

            response = model.generate_content(question)

            return jsonify({
                "answer": response.text
            })

        except Exception as e:
            return jsonify({
                "answer": str(e)
            })


 

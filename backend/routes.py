from flask import request, jsonify
from models import User, Incident
from database import db
import openai
import os
import requests


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

        # validation
        if not latitude or not longitude or not description:
            return jsonify({"message": "Missing data"}), 400

        new_incident = Incident(
            user_id=user_id,
            latitude=latitude,
            longitude=longitude,
            description=description
        )

        db.session.add(new_incident)
        db.session.commit()

        return jsonify({"message": "Incident reported successfully"})


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
    
    

    @app.route("/translate", methods=["POST"])
    def translate():
        import urllib.request
        import urllib.parse
        import urllib.error
        import json

        data = request.get_json()

        text = data.get("text")
        source_lang = data.get("source_lang")
        target_lang = data.get("target_lang")

        if not text:
            return jsonify({"error": "No text provided"})

        # Free Google Translate API (client=gtx)
        encoded_text = urllib.parse.quote(text)
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={source_lang}&tl={target_lang}&dt=t&q={encoded_text}"
        
        try:
            # We add a User-Agent header so it doesn't get blocked
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                
            # The response format is deeply nested, e.g. [[["Hola", "Hello", null, null, 1]], null, "en"]
            # To handle long text properly, we loop through sentences
            translated_text = ""
            if result and len(result) > 0 and result[0]:
                for sentence in result[0]:
                    if sentence and len(sentence) > 0 and sentence[0]:
                        translated_text += sentence[0]
                
            return jsonify({
                "translated_text": translated_text
            })

        except urllib.error.HTTPError as e:
            return jsonify({"error": f"HTTP Translation Error: {e.code}"})
        except Exception as e:
            print("ERROR:", e)
            return jsonify({
                "error": str(e)
            }) 


    @app.route("/convert", methods=["POST"])
    def convert_currency():

        data = request.get_json()

        amount = float(data.get("amount"))
        from_currency = data.get("from")
        to_currency = data.get("to")

        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"

        response = requests.get(url)
        data = response.json()

        rate = data["rates"][to_currency]

        converted = amount * rate

        return jsonify({
            "result": f"{amount} {from_currency} = {round(converted,2)} {to_currency}"
        })
    
    

    @app.route("/safe-route", methods=["POST"])
    def safe_route():

        data = request.get_json()

        start = [data["start_lon"], data["start_lat"]]
        end = [data["end_lon"], data["end_lat"]]

        API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6Ijc2OTVkNWM0MWExZjRiZjliODQxMDRlYzliZDZmNmNlIiwiaCI6Im11cm11cjY0In0="   # 🔥 PUT YOUR KEY

        url = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"

        headers = {
            "Authorization": API_KEY,
            "Content-Type": "application/json"
        }

        body = {
            "coordinates": [start, end]
        }

        try:
            response = requests.post(url, json=body, headers=headers)
            data = response.json()

            print("API RESPONSE:", data)

            # ✅ CHECK ROUTES
            if "features" not in data or len(data["features"]) == 0:
                return jsonify({
                    "score": 0,
                    "route": [],
                    "error": "Route API failed"
                })

            route_coords = data["features"][0]["geometry"]["coordinates"]

            return jsonify({
                "score": 85,
                "route": route_coords
            })

        except Exception as e:
            print("ERROR:", e)
            return jsonify({
                "score": 0,
                "route": [],
                "error": str(e)
            })

    @app.route("/trip-budget", methods=["POST"])
    def trip_budget():
        import google.generativeai as genai
        
        data = request.get_json()
        origin = data.get("origin")
        destination = data.get("destination")
        people = data.get("people", 1)
        
        prompt = f"Act as a Trip Budget Estimator (Trip Buddy Matching). I want to travel from {origin} to {destination} for {people} people.\nEstimate the total budget in INR. \nProvide a short breakdown per person (Train/Travel charges, Food, Hotel stay, Taxis, Other expenses). \nAt the end, provide the 'Total Cost per Person' and the 'Final Whole Trip Cost for {people} people'.\nKeep the response clear, concise, and in plain text."
        
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt)
            return jsonify({"budget_plan": response.text})
        except Exception as e:
            return jsonify({"error": str(e)})
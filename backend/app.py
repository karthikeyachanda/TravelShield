from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from backend.database import db
from backend.routes import register_routes

# create flask app
app = Flask(__name__)

# enable CORS
CORS(app)

# database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///travelshield.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# EMAIL CONFIGURATION (FOR SOS ALERTS)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "karthikeya201620@gmail.com"
app.config['MAIL_PASSWORD'] = "ftisuqvkuxtehzkm"
app.config['MAIL_DEFAULT_SENDER'] = "praharshacheela2006@gmail.com"

# initialize mail
mail = Mail(app)


# connect database with app
db.init_app(app)

# register routes
register_routes(app)


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


# run server
if __name__ == "__main__":
    app.run(debug=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
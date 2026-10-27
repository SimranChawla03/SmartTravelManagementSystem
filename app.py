import os

import re

import secrets

from datetime import datetime, timezone, date

from functools import wraps

from dotenv import load_dotenv

from flask import (

    Flask, render_template, request,

    redirect, url_for, flash, session

)

from pymongo import MongoClient

from pymongo.errors import DuplicateKeyError, PyMongoError, ConfigurationError

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("smart_travel")

from werkzeug.security import generate_password_hash, check_password_hash

# ==========================================

# CONFIGURATION

# ==========================================

load_dotenv()

app = Flask(__name__, template_folder="templates", static_folder="static")

app.secret_key = os.getenv("SECRET_KEY")

if not app.secret_key:

    app.secret_key = secrets.token_hex(32)

app.config.update(

    SESSION_COOKIE_HTTPONLY=True,

    SESSION_COOKIE_SAMESITE="Lax",

)

mongo_uri = os.getenv("MONGODB_URI")

database_name = os.getenv("DATABASE_NAME", "smart_travel_db")

client = None
db = None
users_collection = None
bookings_collection = None

def get_db():
    global client, db, users_collection, bookings_collection
    if db is not None:
        return db
    if not mongo_uri:
        logger.warning("MONGODB_URI is not set in environment.")
        return None
    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        db = client[database_name]
        users_collection = db["users"]
        bookings_collection = db["bookings"]
        return db
    except (PyMongoError, ConfigurationError) as e:
        logger.warning("Could not establish immediate MongoDB connection: %s", type(e).__name__)
        return None

def init_db_indexes():
    global users_collection, bookings_collection
    database = get_db()
    if database is not None and users_collection is not None and bookings_collection is not None:
        try:
            users_collection.create_index("email", unique=True)
            bookings_collection.create_index("booking_ref", unique=True)
        except PyMongoError as e:
            logger.warning("Could not create database indexes: %s", type(e).__name__)

# Initial attempt to connect and create indexes
get_db()
init_db_indexes()

# ==========================================
# DEMO AIRLINE CATALOGUE
# Sample flight schedules and fares for the college project.
# These are not live airline schedules or prices.
# ==========================================

AIRLINE_TEMPLATES = [
    {"airline": "British Airways", "code": "BA", "flight_no": "BA", "departure": "10:25", "arrival": "16:40", "duration": "9h 45m", "stops": "Non-stop", "baggage": "23 kg checked", "price_factor": 1.00, "fare_type": "Standard Economy", "description": "A direct international service with included checked baggage."},
    {"airline": "Air India", "code": "AI", "flight_no": "AI", "departure": "14:10", "arrival": "20:35", "duration": "10h 05m", "stops": "Non-stop", "baggage": "23 kg checked", "price_factor": 0.91, "fare_type": "Economy Flex", "description": "Flexible economy fare with checked baggage included."},
    {"airline": "Emirates", "code": "EK", "flight_no": "EK", "departure": "04:30", "arrival": "13:20", "duration": "12h 20m", "stops": "1 stop · Dubai", "baggage": "25 kg checked", "price_factor": 1.08, "fare_type": "Economy Saver", "description": "Connect through Dubai with generous baggage allowance."},
    {"airline": "IndiGo", "code": "6E", "flight_no": "6E", "departure": "06:15", "arrival": "15:05", "duration": "11h 50m", "stops": "1 stop", "baggage": "15 kg checked", "price_factor": 0.82, "fare_type": "Economy Lite", "description": "A value-focused option for budget-conscious travellers."},
]

DESTINATION_BASE_PRICES = {
    "london": ("United Kingdom", 650),
    "paris": ("France", 600),
    "italy": ("Italy", 680),
    "tokyo": ("Japan", 750),
    "singapore": ("Singapore", 450),
    "dubai": ("United Arab Emirates", 400),
    "bangkok": ("Thailand", 350),
    "new york": ("United States", 800),
    "switzerland": ("Switzerland", 700),
}

DESTINATIONS = {}
for destination_name, (country_name, base_price) in DESTINATION_BASE_PRICES.items():
    flight_options = []
    for airline in AIRLINE_TEMPLATES:
        flight_options.append({
            "id": f"{destination_name.replace(' ', '-')}-{airline['code'].lower()}",
            "name": airline["airline"],
            "airline": airline["airline"],
            "airline_code": airline["code"],
            "flight_number": f"{airline['flight_no']} {100 + len(flight_options) * 27 + len(destination_name) * 3}",
            "type": "Flight",
            "fare_type": airline["fare_type"],
            "price": round(base_price * airline["price_factor"]),
            "departure": airline["departure"],
            "arrival": airline["arrival"],
            "duration": airline["duration"],
            "stops": airline["stops"],
            "baggage": airline["baggage"],
            "description": airline["description"],
        })
    DESTINATIONS[destination_name] = {"country": country_name, "options": flight_options}

COUNTRY_ALIASES = {
    "united kingdom": "london",
    "uk": "london",
    "great britain": "london",
    "england": "london",
    "france": "paris",
    "japan": "tokyo",
    "singapore": "singapore",
    "thailand": "bangkok",
    "united arab emirates": "dubai",
    "uae": "dubai",
    "emirates": "dubai",
    "united states": "new york",
    "united states of america": "new york",
    "usa": "new york",
    "us": "new york",
    "america": "new york",
    "italy": "italy",
    "switzerland": "switzerland",
    "swiss": "switzerland",
}

def find_destination(destination_query):
    """Match a supported destination by city or country, ignoring letter case."""
    if not destination_query:
        return None
    normalized = destination_query.strip().casefold()
    if normalized in DESTINATIONS:
        return DESTINATIONS[normalized]
    target_city = COUNTRY_ALIASES.get(normalized)
    if target_city and target_city in DESTINATIONS:
        return DESTINATIONS[target_city]
    for city_key, dest_data in DESTINATIONS.items():
        if dest_data["country"].casefold() == normalized:
            return dest_data
    return None

def get_travelers(value):

    """Accept traveler counts from 1 through 5."""

    try:

        count = int(value)

    except (ValueError, TypeError):

        return None

    return count if 1 <= count <= 5 else None

def parse_travel_date(value):

    """Reject invalid dates and dates in the past."""

    try:

        parsed = date.fromisoformat(value)

    except (ValueError, TypeError):

        return None

    if parsed.isoformat() != value or parsed < date.today():

        return None

    return parsed

# ==========================================

# LOGIN PROTECTION

# ==========================================

def login_required(view):

    @wraps(view)

    def wrapped_view(*args, **kwargs):

        if "user_id" not in session:

            flash("Please sign in to continue.", "error")

            return redirect(url_for("login", next=request.full_path if request.query_string else request.path))

        return view(*args, **kwargs)

    return wrapped_view

# ==========================================

# HOME

# ==========================================

@app.route("/")

def home():

    return render_template("index.html")

# ==========================================

# REGISTRATION

# ==========================================

@app.route("/register", methods=["GET", "POST"])

def register():

    if request.method == "GET":

        return render_template("register.html")

    name = request.form.get("name", "").strip()

    email = request.form.get("email", "").strip().lower()

    password = request.form.get("password", "")

    if len(name) < 2 or len(name) > 80:

        flash("Name must contain between 2 and 80 characters.", "error")

        return redirect(url_for("register"))

    if (

        not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email)

        or len(email) > 254

    ):

        flash("Please enter a valid email address.", "error")

        return redirect(url_for("register"))

    if len(password) < 8:

        flash("Password must contain at least 8 characters.", "error")

        return redirect(url_for("register"))

    if len(password) > 128:

        flash("Password must not exceed 128 characters.", "error")

        return redirect(url_for("register"))

    user = {

        "name": name,

        "email": email,

        "password_hash": generate_password_hash(password),

        "created_at": datetime.now(timezone.utc),

    }

    try:
        col = users_collection if users_collection is not None else (get_db()["users"] if get_db() is not None else None)
        if col is None:
            flash("Database service is currently unavailable. Please try again shortly.", "error")
            return redirect(url_for("register"))
        col.insert_one(user)

    except DuplicateKeyError:

        flash("An account with this email already exists.", "error")

        return redirect(url_for("register"))
    except PyMongoError as e:
        logger.error("Registration database error: %s", type(e).__name__)
        flash("Database service is currently unavailable. Please try again shortly.", "error")
        return redirect(url_for("register"))

    flash("Account created successfully! You can now sign in.", "success")

    return redirect(url_for("login"))

# ==========================================

# LOGIN

# ==========================================

@app.route("/login", methods=["GET", "POST"])

def login():

    if request.method == "GET":
        next_url = request.args.get("next", "")
        if next_url.startswith("/") and not next_url.startswith("//"):
            session["login_next_url"] = next_url
        return render_template("login.html")

    email = request.form.get("email", "").strip().lower()

    password = request.form.get("password", "")

    try:
        col = users_collection if users_collection is not None else (get_db()["users"] if get_db() is not None else None)
        if col is None:
            flash("Database service is currently unavailable. Please try again shortly.", "error")
            return redirect(url_for("login"))
        user = col.find_one({"email": email})
    except PyMongoError as e:
        logger.error("Login database error: %s", type(e).__name__)
        flash("Database service is currently unavailable. Please try again shortly.", "error")
        return redirect(url_for("login"))

    if not user or not check_password_hash(

        user.get("password_hash", ""), password

    ):

        flash("Invalid email or password. Please try again.", "error")

        return redirect(url_for("login"))

    next_url = session.get("login_next_url", "") or request.args.get("next", "")

    session.clear()

    session["user_id"] = str(user["_id"])

    session["user_name"] = user["name"]

    session["user_email"] = user["email"]

    flash(f"Welcome back, {user['name']}!", "success")

    if next_url.startswith("/") and not next_url.startswith("//"):
        return redirect(next_url)
    return redirect(url_for("home"))

# ==========================================

# LOGOUT

# ==========================================

@app.route("/logout", methods=["POST"])

def logout():

    session.clear()

    flash("You have been signed out successfully.", "success")

    return redirect(url_for("home"))

# ==========================================

# ACCOUNT

# ==========================================

@app.route("/account")

@login_required

def account():

    return render_template("account.html")

# ==========================================

# DESTINATION SEARCH

# ==========================================

@app.route("/destinations")
@login_required
def destinations():

    destination_query = request.args.get("destination", "").strip()[:100]

    travel_date = request.args.get("travel_date", "").strip()

    travelers_value = request.args.get("travelers", "2").strip()

    travelers = get_travelers(travelers_value)

    if travelers is None:

        travelers = 2

    today = date.today().isoformat()

    destination_info = find_destination(destination_query)

    travel_options = destination_info["options"] if destination_info else []

    if travel_date:
        if not parse_travel_date(travel_date):
            flash("Please choose a valid date that is not in the past.", "error")
            travel_date = today
    elif destination_info:
        travel_date = today

    return render_template(

        "destinations.html",

        destination_query=destination_query,

        travel_date=travel_date,

        travelers=str(travelers),

        today=today,

        destination_info=destination_info,

        travel_options=travel_options,

    )

# ==========================================

# CREATE BOOKING

# ==========================================

@app.route("/book", methods=["POST"])

@login_required

def book():

    destination = request.form.get("destination", "").strip()[:100]

    travel_date = request.form.get("travel_date", "").strip()

    travelers = get_travelers(request.form.get("travelers", ""))

    option_id = request.form.get("option_id", "").strip()

    destination_info = find_destination(destination)

    if not destination_info:

        flash(

            "Please choose a supported destination from our flight catalogue.",

            "error",

        )

        return redirect(url_for("destinations"))

    if travelers is None:

        flash("Please select between 1 and 5 travelers.", "error")

        return redirect(url_for("destinations", destination=destination))

    if not parse_travel_date(travel_date):

        flash("Please select a valid travel date that is not in the past.", "error")

        return redirect(

            url_for(

                "destinations",

                destination=destination,

                travelers=travelers,

            )

        )

    option = next(

        (

            item for item in destination_info["options"]

            if item["id"] == option_id

        ),

        None,

    )

    if not option:

        flash(

            "That flight class is not available for this destination.",

            "error",

        )

        return redirect(

            url_for(

                "destinations",

                destination=destination,

                travel_date=travel_date,

                travelers=travelers,

            )

        )

    total_price = option["price"] * travelers

    booking_ref = "ST-" + secrets.token_hex(4).upper()

    booking_record = {

        "booking_ref": booking_ref,

        "user_id": session["user_id"],

        "user_email": session["user_email"],

        "user_name": session["user_name"],

        "destination": destination.title(),

        "country": destination_info["country"],

        "travel_date": travel_date,

        "travelers": travelers,

        "option_id": option["id"],

        "travel_name": option["name"],

        "airline": option.get("airline", option["name"]),

        "flight_number": option.get("flight_number", "Demo flight"),

        "departure": option.get("departure", "To be confirmed"),

        "arrival": option.get("arrival", "To be confirmed"),

        "duration": option.get("duration", "To be confirmed"),

        "stops": option.get("stops", "To be confirmed"),

        "baggage": option.get("baggage", "Check fare details"),

        "fare_type": option.get("fare_type", "Economy"),

        "travel_type": "Flight",

        "price_per_traveler": option["price"],

        "total_price": total_price,

        "currency": "USD",

        "status": "Confirmed",

        "created_at": datetime.now(timezone.utc),

    }

    try:
        col = bookings_collection if bookings_collection is not None else (get_db()["bookings"] if get_db() is not None else None)
        if col is None:
            flash("Database service is currently unavailable. Please try again shortly.", "error")
            return redirect(url_for("destinations", destination=destination, travel_date=travel_date, travelers=travelers))
        col.insert_one(booking_record)

    except DuplicateKeyError:

        flash("Please try booking again.", "error")

        return redirect(

            url_for(

                "destinations",

                destination=destination,

                travel_date=travel_date,

                travelers=travelers,

            )

        )
    except PyMongoError as e:
        logger.error("Booking creation database error: %s", type(e).__name__)
        flash("Database service is currently unavailable. Please try again shortly.", "error")
        return redirect(url_for("destinations", destination=destination, travel_date=travel_date, travelers=travelers))

    return redirect(

        url_for("booking_confirmation", booking_ref=booking_ref)

    )

# ==========================================

# BOOKING CONFIRMATION

# ==========================================

@app.route("/booking/<booking_ref>")

@login_required

def booking_confirmation(booking_ref):

    try:
        col = bookings_collection if bookings_collection is not None else (get_db()["bookings"] if get_db() is not None else None)
        if col is None:
            flash("Database service is currently unavailable.", "error")
            return redirect(url_for("my_bookings"))
        booking_record = col.find_one(
            {
                "booking_ref": booking_ref,
                "user_id": session["user_id"],
            },
            {"_id": 0},
        )
    except PyMongoError as e:
        logger.error("Booking confirmation database error: %s", type(e).__name__)
        flash("Database service is currently unavailable.", "error")
        return redirect(url_for("my_bookings"))

    if not booking_record:

        flash("Booking not found.", "error")

        return redirect(url_for("my_bookings"))

    return render_template(

        "booking_confirmation.html",

        booking=booking_record,

    )

# ==========================================

# MY BOOKINGS

# ==========================================

@app.route("/my-bookings")

@login_required

def my_bookings():

    try:
        col = bookings_collection if bookings_collection is not None else (get_db()["bookings"] if get_db() is not None else None)
        if col is None:
            flash("Database service is currently unavailable.", "error")
            user_bookings = []
        else:
            user_bookings = list(
                col.find(
                    {"user_id": session["user_id"]}
                ).sort("created_at", -1)
            )
    except PyMongoError as e:
        logger.error("My bookings fetch database error: %s", type(e).__name__)
        flash("Database service is currently unavailable.", "error")
        user_bookings = []

    return render_template(

        "my_bookings.html",

        bookings=user_bookings,

    )

# ==========================================

# RUN APPLICATION

# ==========================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

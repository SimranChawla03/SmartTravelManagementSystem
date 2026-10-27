import os
import pytest
from mongomock import MongoClient as MockMongoClient
from werkzeug.security import generate_password_hash
import app as travel_app


@pytest.fixture
def mock_db():
    """Provides an isolated in-memory MongoDB mock for unit testing."""
    client = MockMongoClient()
    db = client["test_smart_travel_db"]
    users_col = db["users"]
    bookings_col = db["bookings"]
    users_col.create_index("email", unique=True)
    bookings_col.create_index("booking_ref", unique=True)

    # Patch module collections
    original_users = travel_app.users_collection
    original_bookings = travel_app.bookings_collection
    travel_app.users_collection = users_col
    travel_app.bookings_collection = bookings_col

    yield {
        "client": client,
        "db": db,
        "users": users_col,
        "bookings": bookings_col,
    }

    # Restore
    travel_app.users_collection = original_users
    travel_app.bookings_collection = original_bookings


@pytest.fixture
def client(mock_db):
    """Provides a Flask test client configured with the mock database."""
    travel_app.app.config["TESTING"] = True
    travel_app.app.config["WTF_CSRF_ENABLED"] = False
    with travel_app.app.test_client() as test_client:
        yield test_client


@pytest.fixture
def sample_user(mock_db):
    """Seeds a verified test user into the mock database."""
    user = {
        "name": "Jane Traveler",
        "email": "jane@example.com",
        "password_hash": generate_password_hash("ValidPass123!"),
    }
    result = mock_db["users"].insert_one(user)
    user["_id"] = result.inserted_id
    return user


@pytest.fixture
def authenticated_client(client, sample_user):
    """Provides a test client pre-authenticated with sample_user."""
    with client.session_transaction() as sess:
        sess["user_id"] = str(sample_user["_id"])
        sess["user_name"] = sample_user["name"]
        sess["user_email"] = sample_user["email"]
    return client

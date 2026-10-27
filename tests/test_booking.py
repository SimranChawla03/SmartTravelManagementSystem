import pytest
from datetime import date, timedelta
from pymongo.errors import PyMongoError
import app as travel_app


# ============================================================================
# BOOKING, CONFIRMATION & E-TICKET TESTS
# ============================================================================

class TestBookingFlow:
    """Test suite for booking flight selections, calculations, e-tickets, and user isolation."""

    def test_tc_book_01_valid_flight_booking(self, authenticated_client, mock_db):
        """TC-BOOK-01: Book flight option successfully and store in database."""
        travel_date = (date.today() + timedelta(days=10)).isoformat()
        response = authenticated_client.post(
            "/book",
            data={
                "destination": "London",
                "travel_date": travel_date,
                "travelers": "2",
                "option_id": "london-ba",
            },
            follow_redirects=False,
        )
        assert response.status_code == 302
        assert "/booking/ST-" in response.headers["Location"]

        # Verify DB entry
        booking = mock_db["bookings"].find_one({"destination": "London"})
        assert booking is not None
        assert booking["travelers"] == 2
        assert booking["airline"] == "British Airways"
        assert booking["travel_date"] == travel_date
        assert booking["booking_ref"].startswith("ST-")
        assert len(booking["booking_ref"]) == 11  # ST- + 8 hex chars
        assert booking["status"] == "Confirmed"

    def test_tc_book_02_total_price_calculation(self, authenticated_client, mock_db):
        """TC-BOOK-02: Total price accurately computes base option price * traveler count."""
        travel_date = (date.today() + timedelta(days=5)).isoformat()
        authenticated_client.post(
            "/book",
            data={
                "destination": "Tokyo",
                "travel_date": travel_date,
                "travelers": "3",
                "option_id": "tokyo-ba",
            },
            follow_redirects=True,
        )
        booking = mock_db["bookings"].find_one({"destination": "Tokyo"})
        assert booking is not None
        expected_total = booking["price_per_traveler"] * 3
        assert booking["total_price"] == expected_total

    def test_tc_book_03_invalid_destination_rejected(self, authenticated_client):
        """TC-BOOK-03: Booking rejected when destination is unsupported."""
        travel_date = (date.today() + timedelta(days=5)).isoformat()
        response = authenticated_client.post(
            "/book",
            data={
                "destination": "Narnia",
                "travel_date": travel_date,
                "travelers": "2",
                "option_id": "narnia-ba",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Please choose a supported destination from our flight catalogue." in response.data

    def test_tc_book_04_invalid_flight_option_rejected(self, authenticated_client):
        """TC-BOOK-04: Booking rejected when flight option ID does not exist."""
        travel_date = (date.today() + timedelta(days=5)).isoformat()
        response = authenticated_client.post(
            "/book",
            data={
                "destination": "Paris",
                "travel_date": travel_date,
                "travelers": "2",
                "option_id": "nonexistent-flight-id",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"That flight class is not available for this destination." in response.data

    def test_tc_book_05_past_date_booking_rejected(self, authenticated_client):
        """TC-BOOK-05: Booking rejected when travel date is in the past."""
        past_date = (date.today() - timedelta(days=3)).isoformat()
        response = authenticated_client.post(
            "/book",
            data={
                "destination": "Paris",
                "travel_date": past_date,
                "travelers": "2",
                "option_id": "paris-ba",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Please select a valid travel date that is not in the past." in response.data

    def test_tc_book_06_e_ticket_confirmation_view(self, authenticated_client, mock_db):
        """TC-BOOK-06: Booking confirmation page displays full e-ticket details."""
        travel_date = (date.today() + timedelta(days=7)).isoformat()
        response = authenticated_client.post(
            "/book",
            data={
                "destination": "Dubai",
                "travel_date": travel_date,
                "travelers": "1",
                "option_id": "dubai-ek",
            },
            follow_redirects=False,
        )
        booking_ref = response.headers["Location"].split("/booking/")[1]

        ticket_response = authenticated_client.get(f"/booking/{booking_ref}")
        assert ticket_response.status_code == 200
        assert b"BOOKING CONFIRMED" in ticket_response.data
        assert booking_ref.encode() in ticket_response.data
        assert b"Dubai" in ticket_response.data
        assert b"Emirates" in ticket_response.data

    def test_tc_book_07_e_ticket_user_isolation(self, client, mock_db, sample_user):
        """TC-BOOK-07: User cannot access another user's e-ticket."""
        # Create booking for sample_user
        mock_db["bookings"].insert_one({
            "booking_ref": "ST-PRIVATE1",
            "user_id": str(sample_user["_id"]),
            "user_email": sample_user["email"],
            "destination": "Rome",
            "country": "Italy",
            "travel_date": "2026-11-01",
            "travelers": 1,
            "status": "Confirmed",
        })

        # Create another user and authenticate as them
        another_user_id = "other_user_12345"
        with client.session_transaction() as sess:
            sess["user_id"] = another_user_id
            sess["user_name"] = "Other Traveler"
            sess["user_email"] = "other@example.com"

        response = client.get("/booking/ST-PRIVATE1", follow_redirects=True)
        assert response.status_code == 200
        assert b"Booking not found." in response.data

    def test_tc_book_08_my_bookings_listing(self, authenticated_client, mock_db, sample_user):
        """TC-BOOK-08: /my-bookings displays list of all bookings for authenticated user."""
        mock_db["bookings"].insert_one({
            "booking_ref": "ST-LISTTEST1",
            "user_id": str(sample_user["_id"]),
            "user_email": sample_user["email"],
            "destination": "London",
            "travel_name": "British Airways",
            "travel_type": "Flight",
            "travel_date": "2026-11-15",
            "travelers": 2,
            "price_per_traveler": 650,
            "total_price": 1300,
            "currency": "USD",
            "status": "Confirmed",
        })

        response = authenticated_client.get("/my-bookings")
        assert response.status_code == 200
        assert b"ST-LISTTEST1" in response.data
        assert b"London" in response.data
        assert b"1 BOOKING" in response.data

    def test_tc_book_09_my_bookings_empty_state(self, authenticated_client):
        """TC-BOOK-09: /my-bookings renders empty state graphic when no bookings exist."""
        response = authenticated_client.get("/my-bookings")
        assert response.status_code == 200
        assert b"0 BOOKINGS" in response.data
        assert b"Your travel story is waiting to begin" in response.data

    def test_tc_book_10_database_failure_during_booking(self, authenticated_client, monkeypatch):
        """TC-BOOK-10: Booking handles database write outage safely."""
        def mock_broken_insert(*args, **kwargs):
            raise PyMongoError("Database cluster write timeout")

        monkeypatch.setattr(travel_app.bookings_collection, "insert_one", mock_broken_insert)

        travel_date = (date.today() + timedelta(days=7)).isoformat()
        response = authenticated_client.post(
            "/book",
            data={
                "destination": "Paris",
                "travel_date": travel_date,
                "travelers": "2",
                "option_id": "paris-ba",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Database service is currently unavailable." in response.data

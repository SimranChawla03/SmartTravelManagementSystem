import os
import pytest
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
LIVE_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DATABASE_NAME", "smart_travel_db")


class TestLiveMongoDBAtlas:
    """Integration test suite executed against live MongoDB Atlas cluster."""

    @pytest.fixture(autouse=True)
    def check_connection(self):
        """Skip live tests if MongoDB Atlas cluster cannot be reached."""
        if not LIVE_URI:
            pytest.skip("MONGODB_URI not configured in .env")
        try:
            client = MongoClient(LIVE_URI, serverSelectionTimeoutMS=4000)
            client.admin.command("ping")
            self.client = client
            self.db = client[DB_NAME]
            yield
            client.close()
        except Exception as e:
            pytest.skip(f"Live MongoDB Atlas unreachable: {e}")

    def test_tc_live_01_atlas_ping(self):
        """TC-LIVE-01: Verify genuine TLS handshake and ping response against MongoDB Atlas."""
        pong = self.client.admin.command("ping")
        assert pong.get("ok") == 1.0

    def test_tc_live_02_collections_exist(self):
        """TC-LIVE-02: Verify that expected production collections exist on Atlas."""
        collections = self.db.list_collection_names()
        assert "users" in collections
        assert "bookings" in collections

    def test_tc_live_03_indexes_configured(self):
        """TC-LIVE-03: Verify unique indexes are active on live users and bookings collections."""
        user_indexes = self.db["users"].index_information()
        booking_indexes = self.db["bookings"].index_information()

        assert "email_1" in user_indexes
        assert user_indexes["email_1"].get("unique") is True

        assert "booking_ref_1" in booking_indexes
        assert booking_indexes["booking_ref_1"].get("unique") is True

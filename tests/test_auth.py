import pytest
from werkzeug.security import check_password_hash
from pymongo.errors import PyMongoError
import app as travel_app


# ============================================================================
# MODULE 1: USER REGISTRATION & AUTHENTICATION TESTS
# ============================================================================

class TestUserRegistration:
    """Test suite for user registration, input validation, and boundary conditions."""

    def test_tc_auth_01_valid_registration(self, client, mock_db):
        """TC-AUTH-01: Register user with valid credentials."""
        response = client.post(
            "/register",
            data={
                "name": "Alex Mercer",
                "email": "alex@example.com",
                "password": "Password123!",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Account created successfully" in response.data

        # Verify DB storage
        user = mock_db["users"].find_one({"email": "alex@example.com"})
        assert user is not None
        assert user["name"] == "Alex Mercer"
        assert check_password_hash(user["password_hash"], "Password123!")
        assert user["password_hash"] != "Password123!"

    def test_tc_auth_02_name_min_boundary_2_chars(self, client, mock_db):
        """TC-AUTH-02: Boundary Value Analysis - Name exactly 2 characters (valid min)."""
        response = client.post(
            "/register",
            data={"name": "Al", "email": "al@example.com", "password": "Password123!"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Account created successfully" in response.data
        assert mock_db["users"].find_one({"email": "al@example.com"}) is not None

    def test_tc_auth_03_name_max_boundary_80_chars(self, client, mock_db):
        """TC-AUTH-03: Boundary Value Analysis - Name exactly 80 characters (valid max)."""
        name_80 = "A" * 80
        response = client.post(
            "/register",
            data={"name": name_80, "email": "a80@example.com", "password": "Password123!"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Account created successfully" in response.data

    def test_tc_auth_04_name_below_min_1_char(self, client):
        """TC-AUTH-04: Boundary Value Analysis - Name 1 character (invalid, below min)."""
        response = client.post(
            "/register",
            data={"name": "A", "email": "a1@example.com", "password": "Password123!"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Name must contain between 2 and 80 characters." in response.data

    def test_tc_auth_05_name_above_max_81_chars(self, client):
        """TC-AUTH-05: Boundary Value Analysis - Name 81 characters (invalid, above max)."""
        name_81 = "A" * 81
        response = client.post(
            "/register",
            data={"name": name_81, "email": "a81@example.com", "password": "Password123!"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Name must contain between 2 and 80 characters." in response.data

    @pytest.mark.parametrize("invalid_email", [
        "notanemail",
        "missingatsign.com",
        "@nodomain.com",
        "user@.com",
        "user@domain",
        "spaces in@domain.com",
    ])
    def test_tc_auth_06_invalid_email_formats(self, client, invalid_email):
        """TC-AUTH-06: Equivalence Partitioning - Malformed email inputs."""
        response = client.post(
            "/register",
            data={"name": "Test User", "email": invalid_email, "password": "Password123!"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Please enter a valid email address." in response.data

    def test_tc_auth_07_password_below_min_7_chars(self, client):
        """TC-AUTH-07: Boundary Value Analysis - Password 7 characters (invalid, below min)."""
        response = client.post(
            "/register",
            data={"name": "Test User", "email": "p7@example.com", "password": "Pass12!"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Password must contain at least 8 characters." in response.data

    def test_tc_auth_08_password_min_boundary_8_chars(self, client, mock_db):
        """TC-AUTH-08: Boundary Value Analysis - Password exactly 8 characters (valid min)."""
        response = client.post(
            "/register",
            data={"name": "Test User", "email": "p8@example.com", "password": "Pass123!"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Account created successfully" in response.data

    def test_tc_auth_09_password_max_boundary_128_chars(self, client, mock_db):
        """TC-AUTH-09: Boundary Value Analysis - Password exactly 128 characters (valid max)."""
        pass_128 = "P" * 128
        response = client.post(
            "/register",
            data={"name": "Test User", "email": "p128@example.com", "password": pass_128},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Account created successfully" in response.data

    def test_tc_auth_10_password_above_max_129_chars(self, client):
        """TC-AUTH-10: Boundary Value Analysis - Password 129 characters (invalid, above max)."""
        pass_129 = "P" * 129
        response = client.post(
            "/register",
            data={"name": "Test User", "email": "p129@example.com", "password": pass_129},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Password must not exceed 128 characters." in response.data

    def test_tc_auth_11_duplicate_email_registration(self, client, sample_user):
        """TC-AUTH-11: Attempt to register with an existing email address."""
        response = client.post(
            "/register",
            data={
                "name": "Jane Imposter",
                "email": sample_user["email"],
                "password": "NewPassword123!",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"An account with this email already exists." in response.data


class TestUserAuthentication:
    """Test suite for login, logout, sessions, access control, and edge cases."""

    def test_tc_auth_12_valid_login(self, client, sample_user):
        """TC-AUTH-12: Sign in with valid email and password."""
        response = client.post(
            "/login",
            data={"email": sample_user["email"], "password": "ValidPass123!"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Welcome back, Jane Traveler!" in response.data

        # Verify session state
        with client.session_transaction() as sess:
            assert sess["user_id"] == str(sample_user["_id"])
            assert sess["user_email"] == sample_user["email"]
            assert sess["user_name"] == sample_user["name"]

    def test_tc_auth_13_login_wrong_password(self, client, sample_user):
        """TC-AUTH-13: Sign in with incorrect password."""
        response = client.post(
            "/login",
            data={"email": sample_user["email"], "password": "WrongPassword!"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Invalid email or password. Please try again." in response.data

        with client.session_transaction() as sess:
            assert "user_id" not in sess

    def test_tc_auth_14_login_nonexistent_user(self, client):
        """TC-AUTH-14: Sign in with an unregistered email address."""
        response = client.post(
            "/login",
            data={"email": "nobody@example.com", "password": "AnyPassword123!"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Invalid email or password. Please try again." in response.data

    def test_tc_auth_15_logout_flow(self, authenticated_client):
        """TC-AUTH-15: Sign out clears session and notifies user."""
        response = authenticated_client.post("/logout", follow_redirects=True)
        assert response.status_code == 200
        assert b"You have been signed out successfully." in response.data

        with authenticated_client.session_transaction() as sess:
            assert "user_id" not in sess

    @pytest.mark.parametrize("protected_url", [
        "/account",
        "/destinations",
        "/my-bookings",
    ])
    def test_tc_auth_16_unauthenticated_protected_route_access(self, client, protected_url):
        """TC-AUTH-16: Unauthenticated user accessing protected routes redirected to login."""
        response = client.get(protected_url, follow_redirects=False)
        assert response.status_code == 302
        assert "/login" in response.headers["Location"]

        # Follow redirect and verify flash message
        redirected_response = client.get(protected_url, follow_redirects=True)
        assert b"Please sign in to continue." in redirected_response.data

    def test_tc_auth_17_safe_login_redirect(self, client, sample_user):
        """TC-AUTH-17: Safe redirection after login using internal relative path."""
        response = client.get("/login?next=/destinations")
        assert response.status_code == 200

        login_response = client.post(
            "/login",
            data={"email": sample_user["email"], "password": "ValidPass123!"},
            follow_redirects=False,
        )
        assert login_response.status_code == 302
        assert login_response.headers["Location"] == "/destinations"

    def test_tc_auth_18_open_redirect_prevention(self, client, sample_user):
        """TC-AUTH-18: Malicious external redirect URLs rejected on login."""
        response = client.get("/login?next=https://malicious-site.com")
        assert response.status_code == 200

        login_response = client.post(
            "/login",
            data={"email": sample_user["email"], "password": "ValidPass123!"},
            follow_redirects=False,
        )
        assert login_response.status_code == 302
        assert login_response.headers["Location"] != "https://malicious-site.com"
        assert login_response.headers["Location"] == "/"

    def test_tc_auth_19_database_unavailable_registration(self, client, monkeypatch):
        """TC-AUTH-19: Registration handles database failure gracefully with user notice."""
        def mock_broken_insert(*args, **kwargs):
            raise PyMongoError("Connection timeout to cluster")

        monkeypatch.setattr(travel_app.users_collection, "insert_one", mock_broken_insert)

        response = client.post(
            "/register",
            data={"name": "Fault User", "email": "fault@example.com", "password": "Password123!"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Database service is currently unavailable." in response.data

    def test_tc_auth_20_database_unavailable_login(self, client, monkeypatch):
        """TC-AUTH-20: Login handles database failure gracefully with user notice."""
        def mock_broken_find(*args, **kwargs):
            raise PyMongoError("Cluster unreachable")

        monkeypatch.setattr(travel_app.users_collection, "find_one", mock_broken_find)

        response = client.post(
            "/login",
            data={"email": "fault@example.com", "password": "Password123!"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Database service is currently unavailable." in response.data

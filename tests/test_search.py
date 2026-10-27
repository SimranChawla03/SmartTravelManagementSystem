import pytest
from datetime import date, timedelta
import app as travel_app


# ============================================================================
# MODULE 2: DESTINATION SEARCH & SELECTION TESTS
# ============================================================================

class TestDestinationSearch:
    """Test suite for destination search, country aliases, flight options, and date/traveler validation."""

    def test_tc_srch_01_search_valid_city(self, authenticated_client):
        """TC-SRCH-01: Search destination by city name (London)."""
        response = authenticated_client.get("/destinations?destination=London")
        assert response.status_code == 200
        assert b"London" in response.data
        assert b"British Airways" in response.data
        assert b"Air India" in response.data
        assert b"Emirates" in response.data
        assert b"IndiGo" in response.data

    @pytest.mark.parametrize("query,expected_keyword", [
        ("lOnDoN", b"London"),
        ("PARIS", b"Paris"),
        ("ToKyO", b"Tokyo"),
        ("   singapore   ", b"Singapore"),
    ])
    def test_tc_srch_02_case_insensitivity_and_whitespace(self, authenticated_client, query, expected_keyword):
        """TC-SRCH-02: Equivalence Partitioning - Search queries ignore casing and whitespace."""
        response = authenticated_client.get(f"/destinations?destination={query}")
        assert response.status_code == 200
        assert expected_keyword in response.data

    @pytest.mark.parametrize("country_query,expected_city", [
        ("France", b"Paris"),
        ("United Kingdom", b"London"),
        ("UK", b"London"),
        ("Japan", b"Tokyo"),
        ("United States", b"New York"),
        ("USA", b"New York"),
        ("Thailand", b"Bangkok"),
        ("United Arab Emirates", b"Dubai"),
        ("UAE", b"Dubai"),
    ])
    def test_tc_srch_03_country_alias_search(self, authenticated_client, country_query, expected_city):
        """TC-SRCH-03: Search destinations by country name or country abbreviation."""
        response = authenticated_client.get(f"/destinations?destination={country_query}")
        assert response.status_code == 200
        assert expected_city in response.data

    def test_tc_srch_04_unmatched_destination_query(self, authenticated_client):
        """TC-SRCH-04: Search for an unsupported destination displays proper notice."""
        response = authenticated_client.get("/destinations?destination=Atlantis")
        assert response.status_code == 200
        assert b"No demo flights found for" in response.data
        assert b"Atlantis" in response.data

    def test_tc_srch_05_empty_destination_query(self, authenticated_client):
        """TC-SRCH-05: Empty destination displays prompt to search."""
        response = authenticated_client.get("/destinations")
        assert response.status_code == 200
        assert b"Ready to find your flight?" in response.data

    def test_tc_srch_06_valid_future_travel_date(self, authenticated_client):
        """TC-SRCH-06: Search with valid future travel date (today + 14 days)."""
        future_date = (date.today() + timedelta(days=14)).isoformat()
        response = authenticated_client.get(f"/destinations?destination=Paris&travel_date={future_date}")
        assert response.status_code == 200
        assert future_date.encode() in response.data
        assert b"Paris" in response.data

    def test_tc_srch_07_past_travel_date_rejected(self, authenticated_client):
        """TC-SRCH-07: Past date rejected with error message and reset to today."""
        past_date = (date.today() - timedelta(days=5)).isoformat()
        response = authenticated_client.get(f"/destinations?destination=Paris&travel_date={past_date}")
        assert response.status_code == 200
        assert b"Please choose a valid date that is not in the past." in response.data

    def test_tc_srch_08_malformed_travel_date_rejected(self, authenticated_client):
        """TC-SRCH-08: Malformed travel date strings rejected gracefully."""
        response = authenticated_client.get("/destinations?destination=Paris&travel_date=invalid-date")
        assert response.status_code == 200
        assert b"Please choose a valid date that is not in the past." in response.data

    def test_tc_srch_09_traveler_count_min_boundary_1(self, authenticated_client):
        """TC-SRCH-09: Boundary Value Analysis - Minimum valid traveler count (1)."""
        response = authenticated_client.get("/destinations?destination=Tokyo&travelers=1")
        assert response.status_code == 200
        assert b"1 traveler" in response.data

    def test_tc_srch_10_traveler_count_max_boundary_5(self, authenticated_client):
        """TC-SRCH-10: Boundary Value Analysis - Maximum valid traveler count (5)."""
        response = authenticated_client.get("/destinations?destination=Tokyo&travelers=5")
        assert response.status_code == 200
        assert b"5 travelers" in response.data

    @pytest.mark.parametrize("invalid_traveler", ["0", "6", "-1", "abc", "100"])
    def test_tc_srch_11_invalid_traveler_count_defaults_to_2(self, authenticated_client, invalid_traveler):
        """TC-SRCH-11: Invalid traveler counts fall back safely to default 2 travelers."""
        response = authenticated_client.get(f"/destinations?destination=Tokyo&travelers={invalid_traveler}")
        assert response.status_code == 200
        assert b"2 travelers" in response.data

    def test_tc_srch_12_flight_card_details_rendered(self, authenticated_client):
        """TC-SRCH-12: Verify full airline schedule details rendered in response."""
        response = authenticated_client.get("/destinations?destination=London")
        assert response.status_code == 200
        html = response.data.decode("utf-8")
        assert "BA" in html
        assert "checked" in html
        assert "Non-stop" in html
        assert "$" in html

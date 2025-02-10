from typing import Any

from collections.abc import Generator
from unittest.mock import Mock, patch

import pytest

from faker import Faker
from fastapi.testclient import TestClient
from main import app

from schemas.url import UrlStatsInfo, UrlVisibility

fake = Faker()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, Any, None]:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def random_user_data() -> dict[str, str]:
    return {
        "username": fake.user_name() + str(fake.random_int()),
        "hashed_password": fake.password(length=12, special_chars=True),
    }


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_user_and_url_flow(client: TestClient, mocker, random_user_data) -> None:  # type: ignore[no-untyped-def]
    mock_client = Mock()
    mock_client.host = "127.0.0.4"
    mocker.patch("starlette.requests.Request.client", new_callable=lambda: mock_client)

    signup_response = client.post("/api/v1/user/signup", json=random_user_data)
    assert signup_response.status_code == 200, "Signup failed"

    create_response = client.post(
        "/api/v1/url/create", json={"original_url": "https://example.com", "visibility": "public"}
    )
    assert create_response.status_code == 201, "URL creation failed"
    short_id = create_response.json()

    assert "short_id" in short_id, "short_id not found in response"
    short_id = short_id["short_id"]

    get_response = client.get("/api/v1/url/", params={"short_id": short_id})
    assert get_response.status_code == 200, "URL not found"

    list_response = client.get("/api/v1/url/list")
    assert list_response.status_code == 200, "URL list not found"

    update_response = client.post(
        "/api/v1/url/visibility", json={"short_id": short_id, "visibility": UrlVisibility.private}
    )
    assert update_response.status_code == 200, "URL visibility update failed"

    stats_response = client.get("/api/v1/url/stats", params={"short_id": short_id, "full_info": UrlStatsInfo.full})
    assert stats_response.status_code == 200, "URL stats not found"

from app import app


def test_delete_url():
    client = app.test_client()

    # Create a short URL
    response = client.post(
        "/shorten",
        json={
            "url": "https://www.google.com"
        }
    )

    assert response.status_code == 201

    data = response.get_json()
    short_code = data["short_code"]

    # Delete the short URL
    response = client.delete(
        f"/delete/{short_code}"
    )

    assert response.status_code == 200

    result = response.get_json()

    assert result["message"] == "Short URL deleted successfully"
    assert result["short_code"] == short_code

    # Confirm URL no longer exists
    response = client.get(
        f"/info/{short_code}"
    )

    assert response.status_code == 404
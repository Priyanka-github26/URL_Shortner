from app import app


def test_redirect_and_click_count(client):

    # 1. Create a short URL
    response = client.post(
        "/shorten",
        json={
            "url": "https://www.google.com"
        }
    )

    assert response.status_code == 201

    data = response.get_json()
    short_code = data["short_code"]

    # 2. Check initial click count
    response = client.get(f"/info/{short_code}")

    assert response.status_code == 200

    info = response.get_json()

    assert info["clicks"] == 0

    # 3. Visit short URL
    response = client.get(
        f"/{short_code}",
        follow_redirects=False
    )

    assert response.status_code == 302

    # 4. Check click count after first visit
    response = client.get(f"/info/{short_code}")

    info = response.get_json()

    assert info["clicks"] == 1

    # 5. Visit short URL again
    response = client.get(
        f"/{short_code}",
        follow_redirects=False
    )

    assert response.status_code == 302

    # 6. Check click count again
    response = client.get(f"/info/{short_code}")

    info = response.get_json()

    assert info["clicks"] == 2
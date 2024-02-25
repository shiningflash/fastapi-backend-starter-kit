def test_get_users(client) -> None:
    response = client.get("api/user")
    _ = response.json()
    assert 200 <= response.status_code < 300

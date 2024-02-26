from app.tests.factories.user import UserFactory


def test_login_logout_successful(client, test_db):
    # Setup: Create a test user
    test_user = UserFactory()

    # Action: Make a request to the login endpoint
    response = client.post(
        "api/login",
        json={"email": test_user.email, 'password': 'password'}
    )

    # Assertions
    assert response.status_code == 200
    assert response.json()["message"] == "login successful"
    assert "authorization" in response.cookies

    logout_response = client.post("api/logout")

    # Assertions
    assert logout_response.status_code == 200
    assert logout_response.json()["message"] == "logout successful"
    assert "authorization" not in logout_response.cookies

    # Teardown: Delete the test user, not working
    # test_db.delete(test_user)
    # test_db.commit()


def test_login_with_invalid_credentials_raises_error(client):
    # Action: Make a request to the login endpoint
    response = client.post(
        "api/login",
        json={'email': 'unknown@test.com', 'password': 'wrong_password'}
    )

    # Action & Assertion: Invalid password
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect email or password"
    assert "authorization" not in response.cookies


def test_oauth_login_successful(client):
    test_user = UserFactory()

    # Action: Make a request to the oauth-login endpoint
    response = client.post(
        "api/oauth-login",
        data={'username': test_user.email, 'password': 'password'}
    )

    # Assertions
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_oauth_login_invalid_credentials_raises_error(client):
    # Action & Assertion: Invalid email
    response = client.post(
        "api/oauth-login",
        data={"username": "unknown@test.com", 'password': 'any'}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Invalid Credentials"


def test_logout(client):
    # Action: Make a request to the logout endpoint
    response = client.post("api/logout")

    # Assertions
    assert response.status_code == 200
    assert response.json()["message"] == "logout successful"
    assert "authorization" not in response.cookies

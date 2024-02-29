import pytest

from app.tests.factories import UserFactory, CasbinRuleFactory

from core.logger import logger


def test_login_logout_successful(client, test_db):
    # Setup 1: Create a test user
    test_user = UserFactory(session=test_db)

    # Setup 2: Define role permission for the user
    _ = CasbinRuleFactory(
        v0=test_user.email,
        v1=test_user.role,
        v2=test_user.organization_name
    )

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


def test_oauth_login_successful(client, test_db):
    # Setup 1: Create a test user
    test_user = UserFactory(session=test_db)
    
    logger.info(f'\n\n\n\n test_user: {test_user.email} \n\n\n')

    # Setup 2: Define role permission for the user
    _ = CasbinRuleFactory(
        v0=test_user.email,
        v1=test_user.role,
        v2=test_user.organization_name
    )

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


# .... More Testing .......
# !!!!!!!!!!!!!!!!!!!!!!!!!

# Parameterized Testing for Input Variations
@pytest.mark.parametrize("email, password, status_code, detail", [
    ("valid@test.com", "wrongpassword", 400, "Incorrect email or password"),  # Incorrect email or password
    ("not-an-email", "password", 422, None),  # Assuming 422 Unprocessable Entity for invalid email format
    ("", "password", 422, None),  # Empty email
    ("valid@test.com", "", 400, None),  # Empty password
    (None, "password", 422, None),  # Missing email
    ("valid@test.com", None, 422, None),  # Missing password
])
def test_login_various_inputs(client, email, password, status_code, detail):
    """
    TestCase 1: Incorrect email or password
    TestCase 2: Assuming 422 Unprocessable Entity for invalid email format
    TestCase 3: Missing email
    TestCase 4: Missing password
    """
    response = client.post(
        "api/login",
        json={"email": email, "password": password}
    )
    assert response.status_code == status_code
    if detail:
        assert response.json()["detail"] == detail


# Comprehensive Error Handling
def test_login_nonexistent_user(client):
    response = client.post("api/login", json={"email": "nonexistent@test.com", 'password': 'password'})
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect email or password"


# Security Tests (SQL Injection)
@pytest.mark.parametrize("email, password", [
    ("'; DROP TABLE users; --", "password"),  # SQL Injection
    ("valid@test.com", "' OR '1'='1"),  # SQL Injection attempt in password
])
def test_login_security_vulnerabilities(client, email, password):
    response = client.post("api/login", json={"email": email, "password": password})
    assert response.status_code in [400, 422]

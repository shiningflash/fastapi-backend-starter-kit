from app.api.auth import login
from app.api.invitation import invite


def test_invite(client):
    login_response = client.post(
        "/login",
        data={"username": "bagdad@gmail.com", "password": "bagdad"}
    )
    
    # Check if login was successful and get the token
    assert login_response.status_code == 200
    token = login_response.json()['access_token']
    
    # Prepare invitation data
    invitation_data = {
        "full_name": "Sakib Al Hasan",
        "email": "sakb@gmail.com",
        "organization": "ABC",
        "organizational_role": "user",
        "role": "user"
    }

    # Send invitation using the '/invite' endpoint with the authorization token
    response = client.post(
        "/invitation/invite",
        json=invitation_data,
        headers={"Authorization": f"Bearer {token}"}
    )

    # Check if the invitation was successfully sent
    assert response.status_code == 200
    assert response.json() == {"message": "Invitation sent successfully"}

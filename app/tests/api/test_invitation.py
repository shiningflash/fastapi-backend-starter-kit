import pytest
from unittest.mock import AsyncMock

from core.config import settings
from app.services.mail import send_email_async


@pytest.mark.asyncio
async def test_invite(client, mocker):
    mocker.patch('app.utils.invitation.generate_invitation_token', return_value="unique_token_123")
    mock_send_email = mocker.patch('app.services.mail.send_email_async', new_callable=AsyncMock)

    invitation_data = {
        "full_name": "Test User Full Name",
        "email": "test_email@example.com",
        "organization": "TestOrg",
        "organizational_role": "Developer",
        "role": "user"
    }

    response = client.post("api/invitation/invite", json=invitation_data)
    
    assert response.status_code == 200
    assert response.json() == {'message': 'Invitation sent successfully'}

    # Assert that send_email_async was called correctly
    # mock_send_email.assert_called_once()
    # mock_send_email.assert_called_with(
    #     subject=f'Invitation to Join {invitation_data["organization"]}',
    #     email_to=invitation_data["email"],
    #     body={
    #         "full_name": invitation_data["full_name"],
    #         "email": invitation_data["email"],
    #         "organization": invitation_data["organization"],
    #         "created_by_name": "Test User",
    #         "invitation_url": f"{settings.BASE_URL}/accept-invitation/unique_token_123"
    #     }
    # )





# def test_invite(client):
#     login_response = client.post(
#         "api/login",
#         json={"email": "bagdad@gmail.com", "password": "bagdad"}
#     )

#     # Check if login was successful and get the token
#     assert login_response.status_code == 200
#     token = client.cookies.get('authorization')

#     mock_invitation = schemas.InvitationCreateRequest.from_orm(InvitationFactory()).__dict__

#     # Send invitation using the '/invite' endpoint with the authorization token
#     response = client.post(
#         "api/invitation/invite",
#         json=mock_invitation,
#         headers={"Authorization": f"Bearer {token}"}
#     )

#     # Check if the invitation was successfully sent
#     assert response.status_code == 200
#     assert response.json() == {"message": "Invitation sent successfully"}
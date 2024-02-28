import pytest

from unittest.mock import AsyncMock
from core.config import settings


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
    # mock_send_email.assert_awaited_once()
    # mock_send_email.assert_awaited_with(
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

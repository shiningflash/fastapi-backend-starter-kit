import pytest
from unittest import mock

from app.tests.utils.dummy import invitation_data


def test_invite_sends_email_successfully(client, mocker):
    """ When the invite API endpoint is called -
        Ensure that an invitation is created successfully
        Ensure that an invitation email is sent successfully with the correct data
    """

    # Mocking a token generation function
    _ = mocker.patch(
        'app.api.invitation.generate_invitation_token',
        return_value="unique_token_123"
    )

    # Mocking the email sending function to prevent actual email dispatch
    mock_send_email = mocker.patch(
        'app.api.invitation.send_email_background',
        return_value=None
    )

    # Execute the api call
    response = client.post("api/invitation/invite", json=invitation_data)

    # Assertions
    assert response.status_code == 200
    assert response.json() == {'message': 'Invitation sent successfully'}

    # Verify the mock was called as expected
    mock_send_email.assert_called_once()
    mock_send_email.assert_called_with(
        background_tasks=mock.ANY,
        subject=f'Invitation to Join {invitation_data["organization"]}',
        email_to=invitation_data["email"],
        body={
            "full_name": invitation_data["full_name"],
            "email": invitation_data["email"],
            "organization": invitation_data["organization"],
            "created_by_name": "test user full name",
            "invitation_url": mock.ANY
        }
    )


@pytest.mark.parametrize("missing_field", [
    ("email"),
    ("organization"),
    ("organizational_role"),
    ("role")
])
def test_invite_missing_required_fields(client, missing_field):
    """
    Ensure the API returns a 422 error for missing required fields in invitation data.
    Each iteration tests a different required field missing from the request.
    """

    # Remove the field being tested in this iteration
    invitation_data.pop(missing_field)

    response = client.post("api/invitation/invite", json=invitation_data)

    assert response.status_code == 422, f"Failed when {missing_field} is missing"

    # Ensure the response details contain information about the missing field
    errors = response.json().get('detail', [])
    assert any(missing_field in error.get("loc", []) for error in errors), f"Missing error details for {missing_field}"


# def test_invite_email_send_failure(client, mocker):
#     """Ensure the API handles email send failures gracefully."""
#     mocker.patch(
#         'app.utils.invitation.generate_invitation_token',
#         return_value="unique_token_123"
#     )
#     mocker.patch(
#         'app.db.crud.CRUDBase.create',
#         return_value=mock.MagicMock()
#     )  # Assume creation is successful

#     # Mock send_email_background to raise an exception
#     mock_send_email = mocker.patch(
#         'app.api.invitation.send_email_background',
#         side_effect=Exception("Email Service Down")
#     )

#     invitation_data = {
#         "full_name": "Test User",
#         "email": "test_email@example.com",
#         "organization": "TestOrg",
#         "organizational_role": "Developer",
#         "role": "user"
#     }

#     response = client.post("api/invitation/invite", json=invitation_data)

#     # In this scenario, decide on the expected behavior: Do you roll back the invitation? Or log the error and proceed?
#     assert response.status_code == 500  # Or another appropriate status code based on your error handling logic
#     assert 'Email Service Down' in response.json().get('detail', '')
#     mock_send_email.assert_called_once()


# def test_invite_invalid_data_5365467587659(client, mocker):
#     """Ensure the API returns a 422 error for invalid invitation data."""
#     # Mocking without side_effect that raises an exception
#     mocker.patch('app.utils.invitation.generate_invitation_token', return_value="unique_token_123")
#     mocker.patch('app.api.invitation.send_email_background', return_value=None)  # No exception raised

#     # Define incomplete invitation data
#     invitation_data = {
#         "full_name": "Test User",
#         # Missing other required fields
#     }

#     response = client.post("api/invitation/invite", json=invitation_data)

#     # Now, the test should reach this point without an exception being raised prematurely
#     assert response.status_code == 422
#     assert 'validation error' in response.json().get('detail', '').lower()


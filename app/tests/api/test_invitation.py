import factory
from faker import Faker

from app import models
from app import schemas

fake = Faker(["en_US"])


class InvitationFactory(factory.Factory):
    class Meta:
        model = models.Invitation

    full_name = fake.name()
    organization = fake.company()
    email = "{}@{}.io".format(
        full_name.split()[0].lower(), organization.split()[0].lower()
    )
    organizational_role = "user"
    role = "user"


def test_invite(client):
    login_response = client.post(
        "api/login",
        json={"email": "bagdad@gmail.com", "password": "bagdad"}
    )

    # Check if login was successful and get the token
    assert login_response.status_code == 200
    token = client.cookies.get('authorization')

    mock_invitation = schemas.InvitationCreateRequest.from_orm(InvitationFactory()).__dict__

    # Send invitation using the '/invite' endpoint with the authorization token
    response = client.post(
        "api/invitation/invite",
        json=mock_invitation,
        headers={"Authorization": f"Bearer {token}"}
    )

    # Check if the invitation was successfully sent
    assert response.status_code == 200
    assert response.json() == {"message": "Invitation sent successfully"}

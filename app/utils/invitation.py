import secrets
from itsdangerous import URLSafeTimedSerializer as Serializer

from core.config import settings


def generate_invitation_token(data) -> str:
    """
    Generates a secure token for email invitations.
    Args: email, full_name, organization, organizational_role, role
    Returns: str: A secure and unique token.
    """
    serializer = Serializer(
        settings.INVITATION_URL_SECRET_KEY,
        salt=settings.INVITATION_URL_SECURITY_PASSWORD_SALT
    )
    unique_id = str(secrets.token_urlsafe())
    token_data = data.__dict__
    token_data['unique_id'] = unique_id
    token = serializer.dumps(token_data)
    return token


def confirm_invitation_token(token: str) -> str:
    """
    Validates and confirms the invitation token.
    Args: token (str)
    Returns: Data from the token if everything ok
    """
    serializer = Serializer(
        settings.INVITATION_URL_SECRET_KEY,
        salt=settings.INVITATION_URL_SECURITY_PASSWORD_SALT
    )
    try:
        # Deserialize the token and ensure it's not expired
        data = serializer.loads(token, max_age=settings.INVITATION_URL_MAX_AGE)
    except Exception:  # Catch exceptions like SignatureExpired, BadSignature
        return None
    data['token'] = token
    return data

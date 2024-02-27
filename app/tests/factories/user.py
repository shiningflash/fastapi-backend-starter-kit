import factory
from faker import Faker
from app.models import User

from app.tests.conftest import TestingSessionLocal
from app.utils.security import get_password_hash

fake = Faker()


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session_persistence = "commit"

    full_name = factory.Faker('name')
    email = factory.LazyAttribute(lambda _: fake.email())
    organization_name = factory.Faker('company')
    organizational_role = factory.Faker('job')
    role = factory.Iterator(['user', 'superuser', 'admin'])
    password = factory.LazyAttribute(lambda _: get_password_hash("password"))

    @factory.post_generation
    def set_email(self, create, extracted, **kwargs):
        if extracted:
            # Use the extracted email if provided.
            self.email = extracted

    @factory.post_generation
    def set_password(self, create, extracted, **kwargs):
        if extracted:
            # Use the extracted password, hash it, and set it.
            self.password = get_password_hash(extracted)
        else:
            # If no password was provided, use 'password' and hash it.
            self.password = get_password_hash("password")
    
    @classmethod
    def create(cls, **kwargs):
        session = kwargs.pop('session', None)
        if session is None:
            raise ValueError("Session is required to create a UserFactory instance.")
        cls._meta.sqlalchemy_session = session
        return super().create(**kwargs)

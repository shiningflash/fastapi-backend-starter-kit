import factory
from app.models import CasbinRule
from app.tests.conftest import TestingSessionLocal


class CasbinRuleFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = CasbinRule
        sqlalchemy_session = TestingSessionLocal()
        sqlalchemy_session_persistence = "commit"

    ptype = "g"  # The ptype field is always set to "g"

    v0 = factory.LazyAttribute(lambda o: o.context.get('v0'))  # email
    v1 = factory.LazyAttribute(lambda o: o.context.get('v1'))  # role
    v2 = factory.LazyAttribute(lambda o: o.context.get('v2'))  # organization_name

from sqlalchemy import Column, String, String, Column, Integer

from app.db.base_class import Base


class CasbinRule(Base):
    __tablename__ = "casbin_rule"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    ptype = Column(String(255))
    v0 = Column(String(255))
    v1 = Column(String(255))
    v2 = Column(String(255))
    v3 = Column(String(255))
    v4 = Column(String(255))
    v5 = Column(String(255))

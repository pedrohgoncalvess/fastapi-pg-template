from sqlalchemy import Column, Integer, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from database.models.base import Base


class Entity(Base):
    __tablename__ = 'entity'
    __table_args__ = {'schema': 'financial'}

    id = Column(Integer, primary_key=True)
    name = Column(Integer, unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    status = Column(Boolean, nullable=False, default=True)
    entity_acc_fk = relationship("Entity", backref="financial.acc_payable")
from sqlalchemy import Column, Integer, DateTime, Boolean, func, String
from sqlalchemy.orm import relationship
from database.models.base import Base
from database.models.financial.acc_payable import AccPayable #This import is necessary for estabelish relationship


class Entity(Base):
    __tablename__ = 'entity'
    __table_args__ = {'schema': 'financial'}

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    status = Column(Boolean, nullable=False, default=True)
    entity_acc_fk = relationship(
        "AccPayable",
        back_populates="acc_entity_fk",
        primaryjoin="Entity.id == AccPayable.id_entity",
        foreign_keys="[AccPayable.id_entity]"
    )


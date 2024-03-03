from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from database.models.base import Base


class AccPayable(Base):
    __tablename__ = 'acc_payable'
    __table_args__ = {'schema': 'financial'}

    id = Column(Integer, primary_key=True)
    id_entity = Column(Integer, unique=True, nullable=False)
    type = Column(String(10), nullable=False)
    cost = Column(Numeric, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    status = Column(Boolean, nullable=False, default=False)
    acc_entity_fk = relationship(
        "Entity",
        back_populates="entity_acc_fk",
        primaryjoin="AccPayable.id_table == Entity.id",
        foreign_keys=[id_entity]
    )


class Entity(Base):
    __tablename__ = 'entity'
    __table_args__ = {'schema': 'financial'}

    id = Column(Integer, primary_key=True)
    name = Column(Integer, unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    status = Column(Boolean, nullable=False, default=True)
    entity_acc_fk = relationship("Entity", backref="financial.acc_payable")

from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean, func, ForeignKey, Computed
from sqlalchemy.orm import relationship
from database.models.base import Base


class AccPayable(Base):
    __tablename__ = 'acc_payable'
    __table_args__ = {'schema': 'financial'}

    id = Column(Integer, primary_key=True)
    id_entity = Column(Integer, ForeignKey('financial.entity.id'), unique=True, nullable=False)
    type = Column(String(10), nullable=False)
    cost = Column(Numeric, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    status = Column(Boolean, nullable=False, default=False)
    compost_id = Column(String(50), Computed("generate_compost_id(id_entity, type, cost)"))
    acc_entity_fk = relationship(
        "Entity",
        back_populates="entity_acc_fk",
        primaryjoin="AccPayable.id_entity == Entity.id",
        foreign_keys=[id_entity]
    )


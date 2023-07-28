from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, \
    UniqueConstraint
from sqlalchemy.orm import relationship

from db.db import Base


class File(Base):
    __tablename__ = 'file'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    path = Column(String)
    size = Column(Integer)
    create_date = Column(
        DateTime(timezone=True), server_default=func.now()
    )
    user_id = Column(ForeignKey('user.id'))
    author = relationship('User', back_populates='files')

    __table_args__ = (UniqueConstraint(
        'name', 'path', name="unique file with path"),
    )

    def __repr__(self):
        return f'{self.username}'

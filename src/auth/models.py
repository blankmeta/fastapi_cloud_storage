from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from db.db import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    create_date = Column(
        DateTime(timezone=True), server_default=func.now()
    )
    files = relationship(
        'File',
        cascade="all, delete",
        passive_deletes=True
    )

    def __repr__(self):
        return f'{self.username}'

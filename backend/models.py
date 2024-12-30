from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database import Base

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    url = Column(String)
    category = Column(String)
    source = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

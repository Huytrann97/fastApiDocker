from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from database import Base

class __User(Base):
    __tablename__ = "card_informations"
    
    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(Integer )
    full_name = Column(String(50))
    birthday = Column(String(50))
    address = Column(String(50))
    expire_date = Column(String(50))

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from database import Base
from datetime import datetime

class Card(Base):
    __tablename__ = "cards"
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, index=True, unique=True)
    front_image_url = Column(String(100))

class User(Base):
    __tablename__ = "card_informations"
    
    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(Integer )
    full_name = Column(String(50))
    birthday = Column(String(50))
    address = Column(String(50))
    expire_date = Column(String(50))



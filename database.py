from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import os
from dotenv import load_dotenv
load_dotenv()

# Thay thế URL_DATABASE với thông tin kết nối JawsDB MySQL của bạn
# URL_DATABASE = os.getenv("JAWSDB_URL")

engine = create_engine(os.getenv("JAWSDB_URL"))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

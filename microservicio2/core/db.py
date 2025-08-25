from sqlalchemy import create_engine
import os

DATABASE_URL = os.getenv("DATABASE_URL")
#DATABASE_URL = "postgresql://jeusma:123456@localhost:5433/dbms2"
engine = create_engine(DATABASE_URL)

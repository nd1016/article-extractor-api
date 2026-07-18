from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os
# Azure will provide the DATABASE_URL through Environment Variables
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://user:pass@127.0.0.1:5433/db")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a SessionLocal class. Each instance of this class will be a database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency function to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

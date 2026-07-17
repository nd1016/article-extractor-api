from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os
# Azure will provide the DATABASE_URL through Environment Variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://dev_user:dev_password@127.0.0.1:5433/article_cache_db")

# Update this to port 5433 if you had to change it earlier for Docker!
#DATABASE_URL = "postgresql://dev_user:dev_password@127.0.0.1:5433/article_cache_db"

# Create the engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a SessionLocal class. Each instance of this class will be a database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency function to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
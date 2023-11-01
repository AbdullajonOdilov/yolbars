from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine=create_engine('mysql+pymysql://root@localhost:3306/tiger')

# $2b$12$6zUrhmEQ6fUWCytj5nSjnu0qph2j81GhYpcoY1xgi36ojKObmDJ8i
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Agar password blank hai (XAMPP default)
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/classify"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
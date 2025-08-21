from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Agar password blank hai (XAMPP default)
DATABASE_URL = "mysql+pymysql://u174570443_arghadas:/0wRH6ph41M>@srv1334.hstgr.io:3306/u174570443_classifiy_py"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
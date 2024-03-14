from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Define SQLAlchemy engine and session
#SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root@localhost/mydb"
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:root@mysql_db:3306/mydb"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Define User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=False, index=True)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)

    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active
        }


# CRUD Operations
def create_user(db_session, user_data):
    try:
        db_user = User(**user_data)
        db_session.add(db_user)
        db_session.commit()
        db_session.refresh(db_user)
        return db_user, None
    except Exception as e:
        print(f"An error occurred while Creating user: {e}")
        error_message = f"An error occurred while Creating user: {e}"
        print(error_message)
        return None, error_message


def get_user(db_session, user_id):
    try:
        user = db_session.query(User).filter(User.id == user_id).first()
        return user
    except Exception as e:
        print(f"An error occurred while fetching user with ID {user_id}: {e}")
        return None


def update_user(db_session, user_id, user_data):
    db_user = db_session.query(User).filter(User.id == user_id).first()
    if db_user:
        for key, value in user_data.items():
            setattr(db_user, key, value)
        db_session.commit()
        db_session.refresh(db_user)
    return db_user


def delete_user(db_session, user_id):
    db_user = db_session.query(User).filter(User.id == user_id).first()
    if db_user:
        db_session.delete(db_user)
        db_session.commit()
    return db_user


def get_all_users(db_session):
    db_users = db_session.query(User).all()
    return db_users


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

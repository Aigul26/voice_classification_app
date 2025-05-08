from sqlalchemy.orm import Session
from app.models import User
from app.utils.auth import get_password_hash
from app.pyd import UserCreate


def get_user_by_login(db: Session, login: str) -> User | None:
    return db.query(User).filter(User.login == login).first()

def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(
        login=user.login,
        name=user.name,
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
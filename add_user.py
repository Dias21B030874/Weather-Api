from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.auth import get_password_hash
from app.models import User

db: Session = SessionLocal()

username = "user1"
password = "password"

hashed_password = get_password_hash(password)

new_user = User(username=username, hashed_password=hashed_password, disabled=False)

db.add(new_user)
db.commit()

print(f"Пользователь {username} успешно создан!")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from database_setup import Base, User

engine = create_engine('sqlite:///diary.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def update_user(username, email=None, name=None, password=None):
    user = session.query(User).filter_by(username=username).first()
    if user:
        if email:
            user.email = email
        if name:
            user.name = name
        if password:
            user.set_password(password)

        try:
            session.commit()
            print(f"User {user.username} updated successfully.")
        except IntegrityError as e:
            session.rollback()
            print(f"Failed to update user {user.username}: {e}")
    else:
        print(f"User with username {username} not found.")

def add_user(username, email, name, password):
    # Check if email already exists
    existing_user = session.query(User).filter_by(email=email).first()
    if existing_user:
        print(f"User with email {email} already exists.")
        return

    # Create a new user
    new_user = User(username=username, email=email, name=name)
    new_user.set_password(password)

    try:
        session.add(new_user)
        session.commit()
        print(f"User {username} added successfully.")
    except IntegrityError as e:
        session.rollback()
        print(f"Failed to add user {username}: {e}")

# Add users
add_user("admin", "admin@admin.ua", "Адмін", "00000000")
add_user("admin2", "admin2@admin.ua", "Адмін", "00000001")

# Update user
update_user(username="admin", name="Новий Адмін", email="admin@admin.ua", password="00000000")
update_user(username="admin2", name="Новий Адмін2", email="admin2@admin.ua", password="00000001")

import sys
import datetime
from sqlalchemy import Column,Integer,String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
Base = declarative_base()

class Subject(Base):
    __tablename__ = 'subject'
    id = Column(Integer, primary_key = True)
    title = Column(String(250),nullable = False)
    teacher = Column(String(250),nullable = False)
    study_account_materials = Column(String(250))
    grade = Column(Integer)

class User(Base, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True)
    username = Column(String(100),nullable = False, unique=True)
    name = Column(String(250),nullable = True)
    email = Column(String(250),nullable = True, unique=True)
    password_hash = Column(String(250),nullable = False)
    update_date = Column(DateTime(), default = datetime.datetime.utcnow, onupdate = datetime.datetime.utcnow)

    def __repr__(self):
        return f"{self.id}{self.username}"

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash, password)
    
class Teacher(Base, UserMixin):
    __tablename__ = "Teacher"
    id = Column(Integer, primary_key = True)
    username = Column(String(100),nullable = False, unique=True)
    name = Column(String(250),nullable = True)
    email = Column(String(250),nullable = True, unique=True)
    password_hash = Column(String(250),nullable = False)
    update_date = Column(DateTime(), default = datetime.datetime.utcnow, onupdate = datetime.datetime.utcnow)

    def __repr__(self):
        return f"{self.id}{self.username}"

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash, password)

engine = create_engine('sqlite:///biblioteka.db')
Base.metadata.create_all(engine)
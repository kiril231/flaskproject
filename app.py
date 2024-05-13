from flask import Flask, render_template,request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base,User
from flask_login import LoginManager, login_required,login_user,logout_user


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = "secret key"
engine = create_engine('sqlite:///diary.db',connect_args={'check_same_thread': False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/',methods=['POST','GET'])
def registr():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        name = request.form['name']
        user = session.query(User).filter_by(username=username).first()
        if user:
            return "Вже існує у системі"
        else:
            user_new = User(username=username, email=email, name=name)
            user_new.set_password(password)
            session.add_all([user_new])
            session.commit()
            return "нового користувача зареэстровано у системі!"
    else:
        return render_template('register.html')

if __name__ == "__main__":
	app.run()
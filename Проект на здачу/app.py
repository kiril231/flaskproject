from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Subject
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = "secret key"

# Database setup
engine = create_engine('sqlite:///diary.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return session.query(User).filter_by(id=user_id).first()

login_manager.login_view = 'login'

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = session.query(User).filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return render_template('iflogined.html')
        else:
            return "Невірний логін або пароль"
    return render_template('login.html')

@app.route('/', methods=['POST', 'GET'])
def registr():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        name = request.form['name']
        existing_user = session.query(User).filter_by(username=username).first()
        if existing_user:
            return "Користувач вже існує"
        else:
            new_user = User(username=username, email=email, name=name)
            new_user.set_password(password)
            session.add(new_user)
            session.commit()
            return "Новий користувач зареєстрований!"
    return render_template('register.html')

@app.route('/home', methods=['POST', 'GET'])
@login_required
def home():
    return render_template('index.html')

@app.route('/cabinet', methods=['POST', 'GET'])
@login_required
def stat():
    subjects = session.query(Subject).all()
    username = current_user.username
    if username in ["admin", "admin2"]:
        if request.method == "POST":
            username = request.form['username']
            user = session.query(User).filter_by(username=username).first()
            if user:
                return "Користувача додано"
            else:
                return "Користувача не знайдено"
        return render_template('chiefteacher_cab.html', username=current_user.name)
    return render_template('user_cab.html', username=current_user.name, subjects=subjects)

@app.route('/about', methods=['POST', 'GET'])
@login_required
def about():
    return render_template("aboutus.html")

@app.route('/delete_subject/<int:subject_id>', methods=['POST', 'GET'])
@login_required
def deleteSubject(subject_id):
    username = current_user.username
    subject_to_delete = session.query(Subject).get(subject_id)
    if username in ["admin", "admin2"]:
        if subject_to_delete:
            session.delete(subject_to_delete)
            session.commit()
            return redirect(url_for('subjects'))
        else:
            return "Subject not found"

@app.route('/subjects', methods=['POST', 'GET'])
@login_required
def subjects():
    subjects = session.query(Subject).all()
    return render_template('subjects.html', subjects=subjects)


@app.route('/cabinet/classes/', methods=["GET", "POST"])
@login_required
def newSubject():
    if request.method == "POST":
        #Extract form data using .get() to handle potential missing fields
        title = request.form.get('name', '').strip()
        teacher = request.form.get('teacher', '').strip()
        study_account_materials = request.form.get('study_account_materials', '').strip()
        grade = request.form.get('grade', '').strip()

        #Ensure required fields are not empty
        if not title or not teacher:
            # Return to the form with an error message
            error = "Назва та вчитель обов'язкові"
            return render_template('subjectAdd.html', error=error)

        #Create and add the new subject to the session
        new_subject = Subject(
            title=title,
            teacher=teacher,
            study_account_materials=study_account_materials,
            grade=grade
        )
        session.add(new_subject)
        session.commit()

        #Redirect to the subjects page
        return redirect(url_for('subjects'))

    #Handle GET request, render the form to add a new subject
    return render_template('subjectAdd.html')

@app.route('/useradd', methods=['POST', 'GET'])
@login_required
def useradd():
    users = session.query(User).all()
    subjects = session.query(Subject).all()
    return render_template('userAdd.html', users=users, subjects=subjects)

if __name__ == "__main__":
    app.run()
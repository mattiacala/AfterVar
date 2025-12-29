from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy #for db
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user #preserve user session 
from werkzeug.security import generate_password_hash, check_password_hash #for pwd security
from datetime import datetime

app = Flask(__name__)

#config db
app.config['SECRET_KEY'] = 'z|jdnds(3243)d$erks9ijsn!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aftervar.db'

#init db
db = SQLAlchemy(app)
login_manager=LoginManager()
login_manager.init_app(app)

#to translate the UID -> user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#user table, usermixin -> function for info of user session, db.model -> to create table
class User(UserMixin, db.Model):
    
    __tablename__ = 'users'
    
    #column
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    punteggio = db.Column(db.Integer)
    squad_prefer = db.Column(db.String(50), nullable=False)
    data_iscr = db.Column(db.DateTime, default=datetime.now)

    #to save encrypt password
    def set_pwd(self, password):
        self.password_hash = generate_password_hash(password)

    #to auth user with correct pwd
    def check_pwd(self, password):
        return check_password_hash(self.password_hash, password)


#Main Menu ON TOP

@app.route('/')
def HomePage():
    return render_template('home.html')

@app.route('/episodi')
def Episodi():
    return render_template('episodi.html')

@app.route('/classifica')
def Classifica():
    return render_template('classifica.html')

@app.route('/arbitri')
def Arbitri():
    return render_template('arbitri.html')

@app.route('/regolamento')
def Regolamento():
    return render_template('regolamento.html')

@app.route('/notizie')
def Notizie():
    return render_template('notizie.html')


#user
@app.route('/login', methods=['GET', 'POST'])
def Login():
    return render_template('login.html')

@app.route('/registrazione', methods=['GET', 'POST'])
def Registrazione():
    return render_template('registrazione.html')

@app.route('/logout',)
def Logout():
    #user exit
    logout_user()
    return redirect(url_for('HomePage'))

#MENU IN FOOTER

@app.route('/privacy')
def privacy_policy():
    return render_template('privacy.html')

@app.route('/cookie')
def cookie_policy():
    return render_template('cookie.html')

@app.route('/terminiecondizioni')
def termini_e_condizioni():
    return render_template('terminiecondizioni.html')

@app.route('/aboutus')
def About_Us():
    return render_template('aboutus.html')

if __name__ == '__main__':
       with app.app_context(): #refer to app
        db.create_all() #create db if not exist

        app.run(host='0.0.0.0', port=5000, debug=True) # host -> to open app to all devices with same network

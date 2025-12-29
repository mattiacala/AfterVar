from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy #for db
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user #preserve user session 
from werkzeug.security import generate_password_hash, check_password_hash #for pwd security
from datetime import datetime #for date and time

app = Flask(__name__) #Create the Flask app. __name__ tells Flask where to look for templates and static files.

#config db
app.config['SECRET_KEY'] = 'z|jdnds(3243)d$erks9ijsn!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aftervar.db'

#init db
db = SQLAlchemy(app)
login_manager = LoginManager()
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
    nome = db.Column(db.String(50), nullable=True)
    cognome = db.Column(db.String(50), nullable=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    punteggio = db.Column(db.Integer, default=0)
    squad_prefer = db.Column(db.String(50), nullable=False)
    data_iscr = db.Column(db.DateTime, default=datetime.now)

    #to save encrypt password
    def set_pwd(self, password):
        self.password_hash = generate_password_hash(password)

    #to auth user with correct pwd
    def check_pwd(self, password):
        return check_password_hash(self.password_hash, password)

#Create db Ref 
class Arbitro(db.Model):
    __tablename__ = 'arbitri'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    cognome = db.Column(db.String(50), nullable=False)
    sezione = db.Column(db.String(50), nullable=False)
    anno_nascita = db.Column(db.Integer)
    img_url = db.Column(db.String(200), default='static/img/default_ref.png')

#function to populate the referees table if they don't exist
def popola_arbitri():
    if Arbitro.query.first():
        return

    dati_iniziali = [
        ("Rosario", "Abisso", "Palermo", 1985),
        ("Giovanni", "Ayroldi", "Molfetta", 1991),
        ("Daniele", "Chiffi", "Padova", 1984),
        ("Andrea", "Colombo", "Como", 1990),
        ("Marco", "Di Bello", "Brindisi", 1981),
        ("Daniele", "Doveri", "Roma 1", 1977),
        ("Maria Sole", "Ferrieri Caputi", "Livorno", 1990),
        ("Marco", "Guida", "Torre Annunziata", 1981),
        ("Fabio", "Maresca", "Napoli", 1981),
        ("Maurizio", "Mariani", "Aprilia", 1982),
        ("Davide", "Massa", "Imperia", 1981),
        ("Luca", "Pairetto", "Nichelino", 1984),
        ("Simone", "Sozza", "Seregno", 1987),
        ("Claudio", "Allegretta", "Molfetta", 1990),
        ("Andrea", "Calzavara", "Varese", 1993),
        ("Giuseppe", "Mucera", "Palermo", 1990),
        ("Niccolò", "Turrini", "Firenze", 1993),
        ("Andrea", "Zanotti", "Rimini", 1993)
    ]
    
    #add row
    try:
        for nome, cognome, sezione, anno in dati_iniziali:
            nuovo = Arbitro(nome=nome, cognome=cognome, sezione=sezione, anno_nascita=anno)
            db.session.add(nuovo)
        db.session.commit()
        print("Database arbitri popolato con successo!")
    except Exception as e:
        db.session.rollback()
        print(f"Errore popolamento: {e}")

#Main Menu ON TOP

@app.route('/')
def HomePage():
    return render_template('home.html')

@app.route('/arbitri')
def Arbitri():
    # check if not exist
    try:
        lista_arbitri = Arbitro.query.order_by(Arbitro.cognome).all()
        if not lista_arbitri:
            popola_arbitri()
            lista_arbitri = Arbitro.query.order_by(Arbitro.cognome).all()
        return render_template('arbitri.html', arbitri=lista_arbitri)
    except Exception as e:
        return f"Errore caricamento database (prova a cancellare aftervar.db e riavviare): {e}"

@app.route('/episodi')
def Episodi():
    return render_template('episodi.html')

@app.route('/classifica')
def Classifica():
    return render_template('classifica.html')

@app.route('/regolamento')
def Regolamento():
    return render_template('regolamento.html')

@app.route('/notizie')
def Notizie():
    return render_template('notizie.html')


#user logic

@app.route('/login', methods=['GET', 'POST'])
def Login():
    if request.method == 'POST':
        #take data in html form
        username = request.form.get('username')
        password = request.form.get('pwd')

        #search user in the db
        user = User.query.filter_by(username=username).first()

        #verify password
        if user and user.check_pwd(password):
            login_user(user)
            return redirect(url_for('HomePage'))
        else:
            flash('Username o Password errati.')
            
    return render_template('login.html')

@app.route('/registrazione', methods=['GET', 'POST'])
def Registrazione():
    if request.method == 'POST':
        #take data in html form
        nome = request.form.get('nome')
        cognome = request.form.get('cognome')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('pwd')
        squadra = request.form.get('sqpref')

        #check if it already exists
        user_exists = User.query.filter((User.email == email) | (User.username == username)).first()
        
        if user_exists:
            flash('Email o Username già esistenti!')
            return redirect(url_for('Registrazione'))

        #create a new user
        new_user = User(
            nome=nome,
            cognome=cognome,
            username=username, 
            email=email, 
            squad_prefer=squadra
        )
        new_user.set_pwd(password) #encrypt the password

        #save to db
        try:
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user) #automatic login after registration
            return redirect(url_for('HomePage'))
        except Exception as e:
            flash(f"Errore registrazione: {e}")
            db.session.rollback()

    return render_template('registrazione.html')

@app.route('/logout')
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

    app.run(host='0.0.0.0', port=5000, debug=True) #host -> to open app to all devices with same network
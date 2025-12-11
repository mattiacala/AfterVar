from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')

def HomePage():
    return render_template('home.html')

@app.route('/regolamento')

def view_regolamento():
    return render_template('regolamento.html')

@app.route('/infoarbitri')

def view_info_arbitri():
    return render_template('Info_Arbitri.html')

@app.route('/newscalcio')

def view_news_calcio():
    return render_template('News_Calcio.html')

@app.route('/chisiamo')

def Chi_Siamo():
    return render_template('Chi_Siamo.html')



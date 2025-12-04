from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def HomePage():
    return render_template('home.html')



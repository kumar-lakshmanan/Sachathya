#For Sachathya
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return "kuma----resand---"

@app.route('/refresh')
def refresh():
    return "kuma----refresh--"

from flask import Flask, render_template
from bert import execute

app = Flask(__name__)

@app.route('/')
def hello():
    input = "i am sad"
    output = execute(input)
    return render_template('index.html', value = output)



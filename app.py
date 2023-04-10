from flask import Flask, render_template, request
from bert import execute

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def hello():
    if request.method == 'POST': 
        user_input = request.form.get("user_input")
        output = execute(user_input)
        return render_template('index.html', user_input = user_input, bot_output = output)
    else: 
        return render_template('index.html')



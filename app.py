from flask import Flask, render_template, request
import main
import random

app = Flask(__name__)

# @app.route('/', methods = ['GET', 'POST'])
# def hello():
#     if request.method == 'POST': 
#         # user_input = request.form.get("user_input")
#         # output = execute(user_input)
#         # return render_template('index.html', user_input = user_input, bot_output = output)
#         return {"hi": "hello"}
#     else: 
#         return {"hi2": "hello2"}
#         # return render_template('index.html')

# @app.route('/test', methods = ['GET', 'POST'])
# def test(): 
#     return str(random.randint(0, 5))

@app.route("/preprocess", methods = ['GET', 'POST'])
def test(): 
    return "This is the root"

@app.route('/testPost', methods = ['GET', 'POST'])
def testPost():
    user_input = request.json["user"]
    bot_output = main.execute_vote(user_input)
    return {"user_input" : user_input, "bot_output": bot_output}





from flask import Flask,render_template,request, redirect
import os
app = Flask(__name__)



#get to see a route, post to send the data
@app.route('/',methods = ['POST','GET'])
def index():
    if request.method == 'POST':
        pass
    else:
        return render_template('index.html'),200

@app.route("/login",methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        return render_template('login.html')

@app.route("/signup",methods = ['POST','GET'])
def signup():
    if request.method == 'POST':
        return render_template('signup.html')


if __name__ == "__main__":
    app.run(debug = True,host = '0.0.0.0')
from flask import Flask,render_template,request, session,redirect,url_for
import src.db_repository as db
import src.login as login
import re

app = Flask(__name__,template_folder='src/templates',static_folder = 'src/static')
def getApp() -> Flask:
    return app

#get to see a route, post to send the data
@app.route('/',methods = ['POST','GET'])
def index():
    if request.method == 'POST':
        pass
    else:
        return render_template('index.html'),200

@app.route("/login",methods = ['POST','GET'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = login.hashPassword(request.form['password'])
        account = db.fetchQuery(query=f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return render_template('index.html', msg='Logged in successfully!')
        else:
            msg = 'Usuario o contraseña inválidos.'
    return render_template('login.html', msg=msg)

@app.route("/logout")
def logout():
    session.pop('loggedin',None)
    session.pop('id',None)
    session.pop('username',None)
    return redirect(url_for('login'))

@app.route("/signup",methods = ['POST','GET'])
def signup():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        account = db.fetchQuery(query=f"SELECT * FROM users WHERE username = '{username}'")
        if account:
            msg = 'Cuenta ya existe'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Correo inválido'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Cuenta debe contener carácteres alfanuméricos'
        elif not username or not password or not email:
            msg = 'Información incompleta'
        else:
            db.createUser(username,password,email)
            msg = 'Cuenta creada con éxito'
    return render_template('signup.html',msg = msg)


if __name__ == "__main__":
    app.run(debug = True,host = '0.0.0.0')

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

@app.route("/hobby",methods = ["POST","GET"])
def create_hobby():
    errors = []
    if not session.get('loggedin'):
        return redirect(url_for('login'))

    user_id = session['id']
    if not user_id:
        return redirect(url_for('login'))

    if request.method == "POST":
        name = request.form["name"].strip()
        satisfaction_level = request.form["satisfaction_level"].strip()
        hability = request.form["hability"].strip()
        time = request.form["time"].strip()

        if not name:
            errors.append("Campo nombre requerido")
        elif not satisfaction_level:
            errors.append("Campo nivel de satisfaccion requerido")
        elif not hability:
            errors.append("Campo habilidad requerido")
        elif not time:
            errors.append("Campo tiempo requerido")
        elif int(satisfaction_level) > 10 or int(satisfaction_level)<0:
            errors.append("Nivel de satisfaccion debe estar entre 0 y 10")

        if errors:
            return render_template('hobby.html',errors = errors)

        hobby = db.fetchQuery(query=f"SELECT * FROM hobbies WHERE user_id = {user_id} AND name = '{name}'")
        if hobby:
            errors.append("Hobby ya existe")
            return render_template('hobby.html',errors = errors)
        db.fetchQuery(query= f"iNSERT INTO hobbies (user_id,name,satisfaction_level,hability,time) VALUES ({user_id},'{name}','{satisfaction_level}','{hability}','{time}')")
    return render_template('hobby.html', msg="Hobby añadido")


if __name__ == "__main__":
    app.run(debug = True,host = '0.0.0.0')

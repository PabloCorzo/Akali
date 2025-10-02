from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import hashlib


db : SQLAlchemy


# ------COMO VA MYSQLALCHEMY------

    #cada clase es una tabla, cada atributo es una columna de la tabla
    #id es autoincrement aunque no lo indiquen los parametros
        #porque es la primera columna que es INT y PK de las tablas
    #si no se pone parametro de nombre, toma el de la variable
        #EJEMPLO: director = db.Column(db.String(200))

def createDb(app : Flask):
    db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__= 'Users'
    _id = db.Column('id',db.Integer,primary_key = True)
    username = db.Column(db.String(32),unique = True,nullable = False)
    mail = db.Column(db.String(32),unique = True,nullable = True)
    password = db.Column(db.String(32),nullable = False)

    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.password = self.hashPassword(password)

    def checkPassword(self):
        return Users.query.filter_by(username = self.username, password = self.password)
    
    def hashPassword(self,password : str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
class Peliculas(db.Model):
    __tablename___ = "Films"
    _id = db.Column('id',db.Integer,primary_key = True)
    title = db.Column(db.String(200),nullable = False)
    director = db.Column(db.String(200))
    actors = db.Column(db.String(200))
    synopsis = db.Column(db.String(1000))

    def __init__(self,title, director,actors,synopsis):
        self.title = title
        self.director = director
        self.actors = actors
        self.synopsis = synopsis


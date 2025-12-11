"""
Models module - Activity related models
Este módulo contiene todos los modelos de base de datos de la aplicación.
"""

from database import db
import hashlib
from games import blackjack as bjg

################3
from datetime import datetime


def hashPassword(password: str) -> str:
    """Hash a password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()


class Users(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(32), unique=True, nullable=False)
    email = db.Column('email', db.String(32), unique=True, nullable=True)
    password = db.Column('password', db.String(64), nullable=False)
    coins = db.Column('coins', db.Integer, default=0, nullable=False)
    last_daily_claim = db.Column(db.DateTime, nullable=True)

    def __init__(self, username, email, password,coins =  0):
        self.username = username
        self.email = email
        self.password = hashPassword(password)
        self.coins = coins
class Task(db.Model):
    _id = db.Column('task_id', db.Integer, primary_key=True,unique = True)
    name = db.Column('name', db.String(32),unique=False, nullable=False)
    completed = db.Column('completed', db.Boolean, unique=False, nullable=True)
    _user_id = db.Column('user_id',db.Integer,db.ForeignKey('users.id'), unique = False, nullable = False)
    def __init__(self,name, user):
        self.name = name
        # self._user_id = Users.query.filter_by(username = user).first()._id
        self._user_id = user
        self.completed = 0
        
class ScheduleItem(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    _user_id = db.Column('user_id',db.Integer,db.ForeignKey('users.id'), unique = False, nullable = False)
    title = db.Column('title', db.String(100), unique=False, nullable=False)
    start_time = db.Column('start_time', db.DateTime, unique=False, nullable=False)
    end_time = db.Column('end_time', db.DateTime, unique=False, nullable=False)
    item_type = db.Column('item_type', db.String(50), unique=False, nullable=False)
    item_id = db.Column('item_id', db.Integer, unique=False, nullable=False)
    
    @property
    def id(self):
        return self._id
    
    def __init__(self, user_id, title, start_time, end_time, item_type, item_id):
        self._user_id = user_id
        self.title = title
        self.start_time = start_time
        self.end_time = end_time
        self.item_type = item_type
        self.item_id = item_id

class Activity(db.Model):
    __tablename__ = 'activities'
    _activity_id = db.Column('activity_id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(100), unique=False, nullable=False)
    user_id = db.Column('user_id', db.Integer,db.ForeignKey('users.id'), unique=False, nullable=True)
    satisfaction_level = db.Column('satisfaction_level', db.Integer, nullable=True)
    ability = db.Column('ability', db.String(100), nullable=True)
    time = db.Column('time', db.Float, nullable=True)

    def __init__(self, name, user_id, satisfaction_level, ability, time):
        self.name = name
        self.user_id = user_id
        self.satisfaction_level = satisfaction_level
        self.ability = ability
        self.time = time


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    director = db.Column(db.String(255), nullable=True)
    actors = db.Column(db.String(500), nullable=True)
    synopsis = db.Column(db.Text, nullable=True)
    ###########
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, title, director=None, actors=None, synopsis=None, user_id=None):
        self.title = title
        self.director = director
        self.actors = actors
        self.synopsis = synopsis
        ##############
        self.user_id = user_id

##########################
#PARA MANTENER UNA SOLA PARTIDA CONCURRENTE DE BLACKJACK POR CUENTA
class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'), nullable=False,index = True)
    player_hand = db.Column(db.String(64))
    dealer_hand = db.Column(db.String(64))
    turn = db.Column(db.Integer)
    deck = db.Column(db.String(64))
    bet = db.Column(db.Integer,nullable = False)

    def initialize_game(self):
        state = bjg.BlackJack().state
        return state

    def __init__(self, uid,bet):
        self.title = 'Blackjack state'
        self.user_id = uid
        self.bet = bet
        

        s = self.initialize_game()
        stats = s.serialize()
        #CHANGED BY LOGIC
        self.player_hand = ''.join(stats['phand'])
        self.dealer_hand = ''.join(stats['dhand'])
        self.deck = ''.join(stats['deck'])
        self.turn = 0
# Game.query.filter_by(user_id = session['id']).update({
            # 'dealer_hand' : ''.join(dhand),
            # 'player_hand' : ''.join(phand),
            # 'deck' : ''.join(deck),
            # 'turn' : bj.turn,
            #  })

# -------------------- NUEVOS: ENTRENAMIENTOS + NUTRICIÓN --------------------

class Workout(db.Model):
    __tablename__ = "workouts"
    id = db.Column(db.Integer, primary_key=True)
    # Relación con usuario (tabla 'users')
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'), nullable=False,index = True)
    date = db.Column(db.Date, default=datetime.utcnow)
    title = db.Column(db.String(120), nullable=False)
    duration_min = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text)
    # Relación 1-N con Exercise
    exercises = db.relationship("Exercise", backref="workout", cascade="all, delete-orphan")


class Exercise(db.Model):
    __tablename__ = "exercises"
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    kind = db.Column(db.String(50))       # fuerza/cardio/movilidad...
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    weight_kg = db.Column(db.Float)
    time_sec = db.Column(db.Integer)
    distance_km = db.Column(db.Float)


class NutritionEntry(db.Model):
    __tablename__ = "nutrition_entries"
    id = db.Column(db.Integer, primary_key=True)
    # Relación con usuario (tabla 'users')
    user_id = db.Column(db.Integer,db.ForeignKey('users.id') , nullable=False, index=True)
    date = db.Column(db.Date, default=datetime.utcnow)
    meal_type = db.Column(db.String(50))  # desayuno/comida/cena/snack
    food = db.Column(db.String(200), nullable=False)
    calories = db.Column(db.Integer, default=0)
    protein_g = db.Column(db.Float, default=0)
    carbs_g = db.Column(db.Float, default=0)
    fat_g = db.Column(db.Float, default=0)
    notes = db.Column(db.Text)


#########################################

class Flashcard(db.Model):
    __tablename__ = "flashcards"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.BigInteger, nullable=False)

    question = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), default="General")

    bad = db.Column(db.Boolean, default=False)

    def __init__(self, user_id, question, answer, category="General"):
        self.user_id = user_id
        self.question = question
        self.answer = answer
        self.category = category



# -------------------- SKINS OWNED BY USER --------------------
class OwnedSkin(db.Model):
    __tablename__ = "owned_skins"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    skin_id = db.Column(db.Integer, nullable=False)
    equipped = db.Column(db.Boolean, unique=False, nullable=True)

    def __init__(self, user_id, skin_id, equipped = 0):
        self.user_id = user_id
        self.skin_id = skin_id
        self.equipped = equipped
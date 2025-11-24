from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from model import Game
from database import db
from utils import  isLogged, login_required
from games import blackjack as bjg
from time import sleep
from copy import deepcopy

games_bp = Blueprint(
    'games', __name__,
    template_folder='../templates',
    static_folder='../static'
)

@games_bp.route("/dashboard/games", methods=["GET"])
@login_required
def games():
    q_title    = (request.args.get("title") or "").strip()
    searched = any([q_title])

    games = []
    if searched:
        query = Game.query.filter(Game.user_id == session['id'])
        if q_title:
            query = query.filter(Game.title.ilike(f"%{q_title}%"))
        games = query.order_by(Game.id.desc()).all()

    return render_template("games.html", games=games, searched=searched)



#------------------------------------
def start_game() -> bjg.BlackJack:
    
    return bjg.BlackJack()





def get_dealer_move(state : bjg.GameState) -> int:
    
    #insta win
    if state.player_score() > 21 or state.player_score() < state.dealer_score():
        return 0
    
    #hit until 17+
    if state.dealer_score() < 17:
        return 1
    
    #stay at 17+
    return 0


@games_bp.route("/dashboard/blackjack",methods = ["GET","POST"])
@login_required
def blackjack(action = 3):

    #add action var to the state object to pass it here and apply result

    #player_hand
    #dealer_hand
    #deck
    #turn  
    action = request.args.get('action')


    if action == "NEW":
        session["game"] = None
        action = 3

    if not session["game"]:

        bj = start_game().state
        d = bj.serialize()
        session["game"] = True
        session["game_player_hand"] = d["phand"]
        session["game_dealer_hand"] = d["dhand"]
        session["game_deck"] = d["deck"]
        session["game_turn"] = d["turn"]
        
    else:
        phand = session["game_player_hand"]
        dhand = session["game_dealer_hand"]
        deck = session["game_deck"]
        turn = session["game_turn"]
        stats = {}    
        bj = start_game().state
        stats["phand"] = phand
        stats["dhand"] = dhand
        stats["deck"] = deck
        stats["turn"] = turn

        bj.to_state(stats)

        
    if bj.turn != 0:
        action = None

    if action:

    #action is 3 when the next button is pressed, also when entering through games page
        if int(action != 3):
            new_state = bj.result(action)
            bj = new_state
            d = bj.serialize()
            session["game_player_hand"] = d["phand"]
            session["game_dealer_hand"] = d["dhand"]
            session["game_deck"] = d["deck"]
            session["game_turn"] = d["turn"]

    elif bj.turn == 1:

        action = get_dealer_move(bj)
        new_state = bj.result(action)
        bj = new_state
        d = bj.serialize()
        session["game_player_hand"] = d["phand"]
        session["game_dealer_hand"] = d["dhand"]
        session["game_deck"] = d["deck"]
        session["game_turn"] = d["turn"]

    # Determinar estado de la mascota
    if bj.turn < 2:
        mascot_state = "playing"
    else:
        winner = bj.get_winner()
    if winner == 1:
        mascot_state = "win"
    elif winner == -1:
        mascot_state = "lose"
    else:
        mascot_state = "tie"


        
    return render_template("blackjack.html",state = bj, mascot_state=mascot_state)
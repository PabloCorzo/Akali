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


#FOR REFERENCE
# def play():
#     while not bj.state.is_over():
#         #get score of current player to see valid moves (hit/pass)
#         if bj.state.turn == 0:
#             score = bj.state.player_score()
#         else:
#             score = bj.state.dealer_score()
#         legal_actions = bj.state.actions(score)
#         #show player hand
#         if bj.state.turn == 0:
#             for card in bj.state.player_hand:
#                 print(card.name)
#             print(f"your score: {bj.state.player_score()}")
#         #if is players turn, only one dealer card is shown
#         hide = bj.state.turn == 0
#         print(f"dealer score: {bj.state.dealer_score(hide = hide)}")
#         if hide:
#             sleep(0.5)
        
#         #random invalid move which wont work so while loop gets executed
#         move = -1 
#         if bj.state.turn == 0:
#                 while move not in legal_actions:
#                     move = bj.player.get_move(bj.state)
#         elif bj.state.turn == 1:
#             if bj.state.player_score() > 21:
#                 bj.state.turn = 2
#                 move = 2
#             else:
#                 while move not in legal_actions:
#                     move = bj.dealer.get_move(bj.state)
#         if move != 2:
#             new_state = bj.state.result(move)
#             bj.state = new_state
#     #HERE, GAME HAS ENDED
#         print("final results:")
#         print(f"your score : {bj.state.player_score()}")
#         print(f"house score : {bj.state.dealer_score()}")
#         if bj.state.turn == 1:
#             print(f"dealer score: {bj.state.dealer_score(hide = False)}")
#             sleep(0.5)
#         if bj.state.player_score() > 21 or bj.state.player_score() < bj.state.dealer_score() <= 21:
#             print("YOU LOSE")
#         elif 21 >= bj.state.player_score() > bj.state.dealer_score() or bj.state.dealer_score() > 21:
#             print("YOU WIN")
#         elif bj.state.player_score() == bj.state.dealer_score():
#             print("IT'S A TIE")

# def get_winner(state : bjg.GameState) -> int:

#     #either player is above 21 or below dealer, who isnt above 21   
#     if state.player_score() > 21 or state.player_score() < state.dealer_score() <= 21:
#         print("YOU LOSE")

#     #player is above dealer, but not 21 or dealer is above 21
#     elif 21 >= state.player_score() > state.dealer_score() or state.dealer_score() > 21:
#         print("YOU WIN")

#     #both are tied
#     elif state.player_score() == state.dealer_score():
#             print("IT'S A TIE")


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

        
    return render_template("blackjack.html",state = bj)
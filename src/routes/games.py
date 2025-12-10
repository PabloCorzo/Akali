from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from model import Game, Users
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
def blackjack(action = None):

    #add action var to the state object to pass it here and apply result

    db_state = Game.query.filter_by(user_id = session['id']).first()
    if not db_state:
        print('\n\nGAME NOT FOUND ON DB\n\n')
        
        db_state = Game(session['id'],bet = request.form['bet'].strip())
        db.session.add(db_state)
        db.session.commit()
    if request.method == 'POST':
        try:
            bet = int(request.form["bet"].strip())
        except:
            bet = db_state.bet
        refresh = False
    else:
        refresh = True
        bet = db_state.bet
    print(f'\n\n\n\nBET IS {bet}\n\n\n\n')

    print(f'ACTION IS {action}')
    #create game if its first time (with default/invalid values)
    
    bj = start_game().state
    stats = {}    
    stats["phand"] = list(db_state.player_hand)
    stats["dhand"] = list(db_state.dealer_hand)
    stats["deck"] = list(db_state.deck)
    stats["turn"] = db_state.turn
    bj.to_state(stats)
    print(f'\n\n GAMESTATE ACQUIRED FROM DB:\n {stats}  \n\n')
    print(bj.turn)
    
    #game is ongoing
    print(f'\n\nDBS  TURN RECORD MARKS {db_state.turn}\n\n')
    action = request.args.get('action')
    print(action)

    if action == "NEW":
        
        bj = start_game().state
        dhand = [card.name for card in bj.dealer_hand]
        phand = [card.name for card in bj.player_hand]
        deck = [card.name for card in bj.deck]
        Game.query.filter_by(user_id = session['id']).update({
            'dealer_hand' : ''.join(dhand),
            'player_hand' : ''.join(phand),
            'deck' : ''.join(deck),
            'turn' : bj.turn,
            'bet' :  request.form['bet'].strip(),
             })
        db.session.commit()
        action = 3

        
    if bj.turn != 0:
        action = None


    if action:
    #action is 3 when the next button is pressed, also when entering through games page
        if int(action != 3):
            print('\n\nACTION IS ',action,'\n\n')
            new_state = bj.result(action)
            bj = new_state
            dhand = [card.name for card in bj.dealer_hand]
            phand = [card.name for card in bj.player_hand]
            deck = [card.name for card in bj.deck]
            Game.query.filter_by(user_id = session['id']).update({
            'dealer_hand' : ''.join(dhand),
            'player_hand' : ''.join(phand),
            'deck' : ''.join(deck),
            'turn' : bj.turn,
             })
            db.session.commit()

    elif bj.turn == 1:

        action = get_dealer_move(bj)
        new_state = bj.result(action)
        bj = new_state
        dhand = [card.name for card in bj.dealer_hand]
        phand = [card.name for card in bj.player_hand]
        deck = [card.name for card in bj.deck]
        Game.query.filter_by(user_id = session['id']).update({
            'dealer_hand' : ''.join(dhand),
            'player_hand' : ''.join(phand),
            'deck' : ''.join(deck),
            'turn' : bj.turn,
             })
        db.session.commit()


    #Consultar las monedas del usuario
    coins = Users.query.filter_by(_id = session['id']).first().coins

    # Determinar estado de la mascota
    if bj.turn < 2:
        mascot_state = "playing"
    else:
        winner = bj.get_winner()
        if winner == 1:
            mascot_state = "win"

            if refresh:
                pass

            elif coins > 0:
                Users.query.filter_by(_id = session['id']).update({
                    'coins' : coins + bet,
                })
            else:
                Users.query.filter_by(_id = session['id']).update({
                    'coins' : coins + 1,
                })
            db.session.commit()
        elif winner == -1:
            mascot_state = "lose"

            if refresh:
                pass
            else:
                Users.query.filter_by(_id = session['id']).update({
                        'coins' : coins - bet,
                    })            
                db.session.commit()
        else:
            mascot_state = "tie"

    new_db_state = Game.query.filter_by(user_id = session['id']).first()
    stats = {}    
    stats["phand"] = list(new_db_state.player_hand)
    stats["dhand"] = list(new_db_state.dealer_hand)
    stats["deck"] = list(new_db_state.deck)
    stats["turn"] = new_db_state.turn
    print(f'\n\n GAMESTATE GIVEN TO DB:\n {stats}  \n\n')

    print(f'refresh is {refresh} given method {request.method}')
    return render_template("blackjack.html",state = bj, mascot_state=mascot_state)
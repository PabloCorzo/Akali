from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from model import Game
from database import db
from utils import  isLogged, login_required

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

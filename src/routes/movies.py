from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from model import Movie
from database import db
from utils import  isLogged

movies_bp = Blueprint(
    'movies', __name__, 
    template_folder='../templates',
    static_folder='../static'
)


@movies_bp.route("/dashboard/movies", methods=["GET"])
def movies():
    if not isLogged():
        return redirect(url_for('auth.login'))

    q_title    = (request.args.get("title") or "").strip()
    q_director = (request.args.get("director") or "").strip()
    q_actor    = (request.args.get("actor") or "").strip()

    searched = any([q_title, q_director, q_actor])

    movies = []
    if searched:
        query = Movie.query.filter(Movie.user_id == session['id'])
        if q_title:
            query = query.filter(Movie.title.ilike(f"%{q_title}%"))
        if q_director:
            query = query.filter(Movie.director.ilike(f"%{q_director}%"))
        if q_actor:
            query = query.filter(Movie.actors.ilike(f"%{q_actor}%"))
        movies = query.order_by(Movie.id.desc()).all()

    return render_template("movies.html", movies=movies, searched=searched)

@movies_bp.route("/dashboard/movies/create", methods=["POST"])
def create_movie():

    if not isLogged():
        return redirect(url_for('auth.login'))

    title = (request.form.get("title") or "").strip()
    director = (request.form.get("director") or "").strip() or None
    actors = (request.form.get("actors") or "").strip() or None
    synopsis = (request.form.get("synopsis") or "").strip() or None

    if not title:
        flash("El título es obligatorio", "error")
        return redirect(url_for("movies.movies"))

    ###########
    owner_id = session['id']
    m = Movie(title=title, director=director, actors=actors, synopsis=synopsis,user_id=owner_id)
    db.session.add(m)
    db.session.commit()
    flash("Película guardada", "success")
    return redirect(url_for("movies.movies"))



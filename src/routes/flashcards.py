from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from model import Flashcard  # Importa la clase del modelo
from database import db
from utils import login_required
flashcards_bp = Blueprint(
    'flashcards', __name__,
    template_folder='../templates',
    static_folder='../static'
)


# RUTA 1: VISTA DE FLASHCARDS
@flashcards_bp.route("/dashboard/flashcards", methods=["GET"])
@login_required
def list_flashcards():
    """Muestra todas las flashcards del usuario actual."""
    user_id = session['id']
    flashcard_list = Flashcard.query.filter_by(user_id=user_id).order_by(Flashcard.id.desc()).all()
    return render_template('flashcards.html', flashcards=flashcard_list)


# RUTA 2: CREAR FLASHCARD
@flashcards_bp.route("/dashboard/flashcards/create", methods=['POST'])
@login_required
def create_flashcard():
    """Procesa el formulario para crear una nueva flashcard, impidiendo duplicados."""
    user_id = session['id']
    question = (request.form.get('question') or "").strip()
    answer = (request.form.get('answer') or "").strip()
    category = (request.form.get('category') or "General").strip()

    if not question or not answer:
        flash("Debes completar los campos de Pregunta y Respuesta.", "error")
        return redirect(url_for('flashcards.list_flashcards'))

    existing_card = Flashcard.query.filter_by(
        user_id=user_id,
        question=question
    ).first()

    if existing_card:
        flash(f"La pregunta '{question}' ya existe en tus flashcards.", "error")
        return redirect(url_for('flashcards.list_flashcards'))

    new_card = Flashcard(
        user_id=user_id,
        question=question,
        answer=answer,
        category=category
    )
    db.session.add(new_card)
    db.session.commit()
    flash('¡Flashcard creada con éxito!', 'success')
    return redirect(url_for('flashcards.list_flashcards'))


# RUTA 3: ELIMINAR FLASHCARD
@flashcards_bp.route("/dashboard/flashcards/<int:card_id>/delete", methods=['POST'])
@login_required
def delete_flashcard(card_id):
    """Elimina una flashcard si pertenece al usuario actual."""
    card = Flashcard.query.filter_by(id=card_id, user_id=session['id']).first()

    if card:
        db.session.delete(card)
        db.session.commit()
        flash('Flashcard eliminada.', 'success')
    else:
        flash('No se encontró la flashcard o no tienes permiso.', 'error')

    return redirect(url_for('flashcards.list_flashcards'))
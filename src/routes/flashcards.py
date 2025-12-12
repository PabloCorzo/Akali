from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from model import Flashcard  # Importa la clase del modelo
from database import db
from utils import login_required

BAD_WORDS = [
    # --- Violencia sexual / abuso ---
    "violación", "violador", "violar", "vi0lar", "v1olar",
    "violando", "violada",
    "incesto", "pederastia", "pedo",
    "abuso", "abusar", "abuso infantil",
    "pornografía infantil",

    # --- Palabras sensibles sueltas (para filtro, no contexto) ---
    "menor",

    # --- Follar / variantes ---
    "f0llar", "fo11ar", "f0ll4r", "f0ll@r", "f*llar",
    "f0ll-ar", "f0ll.r", "f0ll4rX", "foll4r_",
    "foLL4r", "f0lL4r", "f0|lar", "f°llar",
    "f0l|ar", "f0ll4rXX", "f0l1ar", "f0l!ar",
    "f0l-l4r", "fol-l4r", "foll4rZ", "f0LL4R",
    "f0lLar~", "foll4r!!", "f0ll@r#", "f0l|_ar",
    "f0ll4r??", "f0ll4rrr", "foll_r", "f0ll_r",
    "f0ll4_r", "f0l1arX", "f0ll4r-test",
    "f0ll4r.mock", "f0ll4r.fake", "f0ll4r.sim",
    "f0ll4r-obf", "f0ll4r-enc",

    # --- Necrofilia / variantes ---
    "necrofilia", "necrofília", "necrofilo", "necrófilo",
    "necrofil@", "n3crofilia", "necr0filia",
    "necro-philia", "necr0f1lia", "necro_filia",

    # --- Sexo / variantes ---
    "sexo", "s3xo", "sex0", "seWo", "s€xo",
    "sx", "sxo", "sexo+", "sexo!", "sexo?",
    "sex@", "se_xo",

    # --- Mierda / variantes ---
    "mierda", "m13rda", "mi3rda", "mierd@", "mierd4",
    "m!erda", "mier-da", "mierda!", "mierda?",
    "mrd", "m1erda","mierdon","mierdón",

    # --- Ñordo / variantes ---
    "ñordo", "nordo", "ñ0rdo", "n0rdo",
    "ñord@", "nord@", "ñ0rd0", "n0rd0",
    "ñordo!", "ñordo?",
    "caca", "kaka", "k4ka",
    "culo", "cul0",
    "pedazo de mierda", "mierdecilla",
    "cagar", "cagada", "cagón",
    "cag4r", "c4gada",

    # --- Insultos sexuales / variantes ---
    "cabrona", "cabrón", "c4brona", "c4brón",
    "putain", "put4in",
    "puta", "put@", "put4",
    "puto", "put0",
    "zorra", "z0rra",
    "perra",
    "prostituta", "prostitución",
    "masturbar", "masturbación", "paja",
    "pajear", "paj3ar",
    "corrida", "correrse",
    "orgasmo", "orgasm0",

    # --- Violencia / variantes ---
    "asesinar", "asesinato",
    "matar", "m4tar",
    "asesinar", "asesino",
    "violento", "violencia",
    "apuñalar", "apuñalamiento",
    "disparar", "tiroteo",
    "secuestrar", "secuestro",
    "tortura", "torturar",

    # --- Drogas / variantes ---
    "metanfetamina", "meta", "meth",
    "cocaína", "cocaina", "coc4ina",
    "heroína", "heroina",
    "porro", "porros",
    "marihuana", "maría",
    "hachís", "hachis",
    "droga", "drogas",
    "yonki", "yonqui",

    # --- MAsturbacion ---
    "masturbación", "masturbacion", "masturbarse",
    "masturbe", "masturbate", "masturbate!","paja","pajearse",
    "pajero","pajera","pajilla","pajote",
    "pajilla","pajillero","pajillera",
    "pajillero","pajillera",
    "pajillero","pajillera",

    # --- palabrotas ---
    "gilipollas", "g1lipollas", "gil1pollas",
    "imbecil", "imbécil", "1mbecil",
    "idiota", "1diota",
    "subnormal", "subnorm4l",
    "estupido", "estúpido",
    "retrasado", "retr4sado",
    "asqueroso", "asqueros@",
    "basura", "basur4",
    "escoria","cabron",


    # --- Política / variantes ---
    "ayuso","pedro sanchez","sanchez","psoe","pp","vox","podemos",
    "izquierda unida","ciudadanos","partido popular","partido socialista","extrema derecha","extrema izquierda",
    "socialismo","comunismo","fascismo","dictadura","democracia", "liberalismo","conservadurismo",
]


def contains_bad_word(text: str) -> bool:
    if not text:
        return False
    t = text.lower()
    return any(bad in t for bad in BAD_WORDS)


flashcards_bp = Blueprint(
    'flashcards', __name__,
    template_folder='../templates',
    static_folder='../static'
)


# RUTA 1: VISTA DE FLASHCARDS
@flashcards_bp.route("/dashboard/flashcards", methods=["GET"])
@login_required
def list_flashcards():
    user_id = session['id']

    flashcard_list = (Flashcard.query
                      .filter_by(user_id=user_id)
                      .order_by(Flashcard.id.desc())
                      .all())

    # ¿La última tarjeta tiene contenido prohibido?
    last_has_bad = False
    if flashcard_list:
        last = flashcard_list[0]
        last_has_bad = contains_bad_word(last.question) or contains_bad_word(last.answer)

    return render_template(
        'flashcards.html',
        flashcards=flashcard_list,
        last_has_bad=last_has_bad
    )


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

    new_card.bad = contains_bad_word(question) or contains_bad_word(answer)

    db.session.add(new_card)
    db.session.commit()

    new_card.bad = contains_bad_word(question) or contains_bad_word(answer)

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
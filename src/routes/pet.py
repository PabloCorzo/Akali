from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from utils import login_required
from database import db
from model import OwnedSkin, Users


pet_bp = Blueprint('pet', __name__, template_folder='../templates')

# -------------------------
# SKINS DEFINIDAS
# -------------------------
skins_data= [
    {"id": 1, "nombre": "basico", "precio": 0,
     "imagenes": ["basico.png", "basico_think.png", "basico_llorar.png"]},

    {"id": 2, "nombre": "pijama", "precio": 50,
     "imagenes": ["pijama.png", "pijama_think.png", "pijama_llorar.png"]},

    {"id": 3, "nombre": "cowboy", "precio": 60,
     "imagenes": ["cowboy.png", "cowboy_think.png", "cowboy_llorar.png"]},

    {"id": 4, "nombre": "pirata", "precio": 70,
     "imagenes": ["pirata.png", "pirata_think.png", "pirata_llorar.png"]},

    {"id": 5, "nombre": "pijo", "precio": 80,
     "imagenes": ["pijo.png", "pijo_think.png", "pijo_llorar.png"]},

    {"id": 6, "nombre": "dune", "precio": 90,
     "imagenes": ["dune.png", "dune2.png"]},

    {"id": 7, "nombre": "navidad", "precio": 100,
     "imagenes": ["navidad.png", "navidad_think.png", "navidad_llorar.png"]},

    {"id": 8, "nombre": "traje", "precio": 120,
     "imagenes": ["traje.png", "traje_think.png", "traje_llorar.png"]},

    {"id": 9, "nombre": "sheldon", "precio": 120,
     "imagenes": ["sheldon.png", "sheldon_think.png", "sheldon_llorar.png"]},

    {"id": 10, "nombre": "enfado", "precio": 10,
     "imagenes": ["enfado.png"]}
]


#Hace que `equipped_skin` esté disponible en TODAS las plantillas
@pet_bp.app_context_processor
def inject_equipped_skin():
    return {
        "equipped_skin": session.get("equipped_skin", "basico")
    }

# -------------------------
# ARMARIO (pagina donde está el mueble)
# -------------------------
@pet_bp.route('/dashboard/pet/wardrobe')
@login_required
def wardrobe():
    return render_template("wardrobe.html")

# -------------------------
# PÁGINA DE SKINS
# -------------------------
@pet_bp.route('/dashboard/pet/skins')
@login_required
def skins():
    user_id = session["id"]


    equipped_skin = OwnedSkin.query.filter_by(user_id = user_id, equipped = 1).first()

    #On first request per user, user wont have a skin
    if not equipped_skin:
        skin = OwnedSkin(user_id = user_id, skin_id = 1, equipped = 1)
        db.session.add(skin)
        db.session.commit()
        equipped_skin = OwnedSkin.query.filter_by(equipped = 1).first()

    # Skins que el usuario tiene en la BD
    owned_ids = [skin.skin_id for skin in OwnedSkin.query.filter_by(user_id = user_id)]
    # Skin equipada actualmente

    # Preparar skins con info extra para el HTML
    skins_preparadas = []
    for s in skins_data:
        s_copy = s.copy()
        s_copy["comprada"] = OwnedSkin.query.filter_by(skin_id = s['id']).first() is not None
        s_copy["equipped"] = (s["id"] == equipped_skin.skin_id)
        skins_preparadas.append(s_copy)
        # print(f'\n\n\nskins preparadas is {skins_preparadas}')
    return render_template("skins.html", skins=skins_preparadas)

# -------------------------
# COMPRAR SKIN
# -------------------------
@pet_bp.route("/buy_skin", methods=["POST"])
@login_required
def buy_skin():
    skin_id = int(request.form.get("skin_id"))

    # Buscar skin en la lista
    skin = next((s for s in skins_data if s["id"] == skin_id), None)

    if not skin:
        flash("Skin no encontrada", "danger")
        return redirect(url_for("pet.skins"))

    # Obtener usuario
    user = Users.query.get(session["id"])

    # Verificar si ya la tiene
    owned = OwnedSkin.query.filter_by(user_id=session["id"], skin_id=skin_id).first()
    if owned:
        flash("Ya tienes esta skin", "info")
        return redirect(url_for("pet.skins"))

    # Verificar monedas
    if user.coins < skin["precio"]:
        flash("No tienes suficientes monedas", "danger")
        return redirect(url_for("pet.skins"))

    # Restar monedas
    user.coins -= skin["precio"]

    # Guardar skin
    new_owned = OwnedSkin(user_id=session["id"], skin_id=skin_id)
    db.session.add(new_owned)
    db.session.commit()

    flash("Compraste la skin correctamente 🎉", "success")
    return redirect(url_for("pet.skins"))


# -------------------------
# EQUIPAR SKIN
# -------------------------
@pet_bp.route("/equip_skin", methods=["POST"])
@login_required
def equip_skin():
    skin_id = int(request.form.get("skin_id"))
    print(f'TRIED TO BUY {skin_id}')
    # Confirmar que el usuario la tiene
    owned = OwnedSkin.query.filter_by(
        user_id=session["id"],
        skin_id=skin_id
    ).first()

    if not owned:
        flash("No tienes esta skin", "danger")
        return redirect(url_for("pet.skins"))

    # Guardar skin equipada
    OwnedSkin.query.filter_by(user_id = session['id'], equipped = 1).update({'equipped':0})
    OwnedSkin.query.filter_by(user_id = session['id'], skin_id = skin_id).update({'equipped':1})
    db.session.commit()
    flash("Skin equipada correctamente ⭐", "success")
    return redirect(url_for("pet.skins"))




@pet_bp.app_context_processor
def inject_equipped_skin():
    skin_id = session.get("equipped_skin", 1)  # por defecto 1 = Básico

    # Buscar skin en datos
    skin = next((s for s in skins_data if s["id"] == skin_id), None)

    if skin:
        main_image = skin["imagenes"][0]   # imagen principal
    else:
        main_image = "basico.png"

    return {"equipped_skin_img": main_image, "equipped_skin_id": skin_id}

from flask import Blueprint, render_template, request
from utils import login_required

pet_bp = Blueprint('pet', __name__, template_folder='../templates')

# =============================
#  PÁGINA PRINCIPAL PET
# =============================
@pet_bp.route('/dashboard/pet')
@login_required
def main():
    return render_template('wardrobe.html')

# =============================
#  ARMARIO
# =============================
@pet_bp.route('/dashboard/pet/wardrobe')
@login_required
def wardrobe():
    skins = [
        {"name": "Básico", "img": "basico.png"},
        {"name": "Básico Llorar", "img": "basico_llorar.png"},
        {"name": "Básico Think", "img": "basico_think.png"},
        {"name": "Pijo", "img": "pijo.png"},
        {"name": "Pijo Llorar", "img": "pijo_llorar.png"},
        {"name": "Pijo Think", "img": "pijo_think.png"},
        {"name": "Cowboy", "img": "cowboy.png"},
        {"name": "Cowboy Llorar", "img": "cowboy_llorar.png"},
        {"name": "Cowboy Think", "img": "cowboy_think.png"},
        {"name": "Navidad", "img": "navidad.png"},
        {"name": "Navidad Llorar", "img": "navidad_llorar.png"},
        {"name": "Navidad Think", "img": "navidad_think.png"},
        {"name": "Pijama", "img": "pijama.png"},
        {"name": "Pijama Llorar", "img": "pijama_llorar.png"},
        {"name": "Pijama Think", "img": "pijama_think.png"},
        {"name": "Sheldon", "img": "sheldon.png"},
        {"name": "Sheldon Llorar", "img": "sheldon_llorar.png"},
        {"name": "Sheldon Think", "img": "sheldon_think.png"},
        {"name": "Traje", "img": "traje.png"},
        {"name": "Traje Llorar", "img": "traje_llorar.png"},
        {"name": "Traje Think", "img": "traje_think.png"},
        {"name": "Pirata", "img": "pirata.png"},
        {"name": "Pirata Think", "img": "pirata_think.png"},
        {"name": "Pirata Llorar", "img": "pirata_llorar.png"},
        {"name": "Dune", "img": "dune.png"},
        {"name": "Dune 2", "img": "dune2.png"},
        {"name": "Enfadado", "img": "enfado.png"}
    ]
    return render_template("wardrobe.html", skins=skins)

# =============================
#  DATOS DE TODAS LAS SKINS
# =============================
skins_data = [
    {"id": "basico", "nombre": "Básico", "precio": 0, "comprada": True,
     "imagenes": ["basico.png", "basico_think.png", "basico_llorar.png"]},

    {"id": "cowboy", "nombre": "Cowboy", "precio": 60, "comprada": False,
     "imagenes": ["cowboy.png", "cowboy_think.png", "cowboy_llorar.png"]},

    {"id": "dune", "nombre": "Dune", "precio": 100, "comprada": False,
     "imagenes": ["dune.png", "dune2.png"]},

    {"id": "enfado", "nombre": "Enfado", "precio": 40, "comprada": False,
     "imagenes": ["enfado.png"]},

    {"id": "navidad", "nombre": "Navidad", "precio": 80, "comprada": False,
     "imagenes": ["navidad.png", "navidad_think.png", "navidad_llorar.png"]},

    {"id": "pijama", "nombre": "Pijama", "precio": 50, "comprada": False,
     "imagenes": ["pijama.png", "pijama_think.png", "pijama_llorar.png"]},

    {"id": "pijo", "nombre": "Pijo", "precio": 80, "comprada": False,
     "imagenes": ["pijo.png", "pijo_think.png", "pijo_llorar.png"]},

    {"id": "pirata", "nombre": "Pirata", "precio": 70, "comprada": False,
     "imagenes": ["pirata.png", "pirata_think.png", "pirata_llorar.png"]},

    {"id": "sheldon", "nombre": "Sheldon", "precio": 120, "comprada": False,
     "imagenes": ["sheldon.png", "sheldon_think.png", "sheldon_llorar.png"]},

    {"id": "traje", "nombre": "Traje", "precio": 90, "comprada": False,
     "imagenes": ["traje.png", "traje_think.png", "traje_llorar.png"]}
]

# =============================
#  TIENDA DE SKINS (ÚNICA FUNCIÓN)
# =============================
@pet_bp.route('/dashboard/pet/skins')
@login_required
def skins():
    return render_template('skins.html', skins=skins_data)

# =============================
#  COMPRA DE SKINS
# =============================
@pet_bp.route('/dashboard/pet/buy_skin', methods=['POST'])
@login_required
def buy_skin():
    data = request.get_json()
    skin_id = data['skin_id']
    price = data['price']

    coins = 70  # ejemplo
    if coins < price:
        return {"ok": False}

    return {"ok": True}



current_skin = "basico"   # la que tenga equipada el usuario
skin_main_image = {
    "basico": "basico.png",
    "cowboy": "cowboy.png",
    "dune": "dune.png",
    "enfado": "enfado.png",
    "navidad": "navidad.png",
    "pijama": "pijama.png",
    "pijo": "pijo.png",
    "pirata": "pirata.png",
    "sheldon": "sheldon.png",
    "traje": "traje.png"
}

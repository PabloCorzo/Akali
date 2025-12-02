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
        {"name": "Básico", "img": "basico.jpg"},
        {"name": "Básico Llorar", "img": "basico_llorar.jpg"},
        {"name": "Básico Think", "img": "basico_think.jpg"},
        {"name": "Pijo", "img": "pijo.jpg"},
        {"name": "Pijo Llorar", "img": "pijo_llorar.jpg"},
        {"name": "Pijo Think", "img": "pijo_think.jpg"},
        {"name": "Cowboy", "img": "cowboy.jpg"},
        {"name": "Cowboy Llorar", "img": "cowboy_llorar.jpg"},
        {"name": "Cowboy Think", "img": "cowboy_think.jpg"},
        {"name": "Navidad", "img": "navidad.jpg"},
        {"name": "Navidad Llorar", "img": "navidad_llorar.jpg"},
        {"name": "Navidad Think", "img": "navidad_think.jpg"},
        {"name": "Pijama", "img": "pijama.jpg"},
        {"name": "Pijama Llorar", "img": "pijama_llorar.jpg"},
        {"name": "Pijama Think", "img": "pijama_think.jpg"},
        {"name": "Sheldon", "img": "sheldon.jpg"},
        {"name": "Sheldon Llorar", "img": "sheldon_llorar.jpg"},
        {"name": "Sheldon Think", "img": "sheldon_think.jpg"},
        {"name": "Traje", "img": "traje.jpg"},
        {"name": "Traje Llorar", "img": "traje_llorar.jpg"},
        {"name": "Traje Think", "img": "traje_think.jpg"},
        {"name": "Pirata", "img": "pirata.jpg"},
        {"name": "Pirata Think", "img": "pirata_think.jpg"},
        {"name": "Pirata Llorar", "img": "pirata_llorar.jpg"},
        {"name": "Dune", "img": "dune.png"},
        {"name": "Dune 2", "img": "dune2.png"},
        {"name": "Enfadado", "img": "enfado.jpg"}
    ]
    return render_template("wardrobe.html", skins=skins)

# =============================
#  DATOS DE TODAS LAS SKINS
# =============================
skins_data = [
    {"id": "basico", "nombre": "Básico", "precio": 0, "comprada": True,
     "imagenes": ["basico.jpg", "basico_think.jpg", "basico_llorar.jpg"]},

    {"id": "cowboy", "nombre": "Cowboy", "precio": 60, "comprada": False,
     "imagenes": ["cowboy.jpg", "cowboy_think.jpg", "cowboy_llorar.jpg"]},

    {"id": "dune", "nombre": "Dune", "precio": 100, "comprada": False,
     "imagenes": ["dune.png", "dune2.png"]},

    {"id": "enfado", "nombre": "Enfado", "precio": 40, "comprada": False,
     "imagenes": ["enfado.jpg"]},

    {"id": "navidad", "nombre": "Navidad", "precio": 80, "comprada": False,
     "imagenes": ["navidad.jpg", "navidad_think.jpg", "navidad_llorar.jpg"]},

    {"id": "pijama", "nombre": "Pijama", "precio": 50, "comprada": False,
     "imagenes": ["pijama.jpg", "pijama_think.jpg", "pijama_llorar.jpg"]},

    {"id": "pijo", "nombre": "Pijo", "precio": 80, "comprada": False,
     "imagenes": ["pijo.jpg", "pijo_think.jpg", "pijo_llorar.jpg"]},

    {"id": "pirata", "nombre": "Pirata", "precio": 70, "comprada": False,
     "imagenes": ["pirata.jpg", "pirata_think.jpg", "pirata_llorar.jpg"]},

    {"id": "sheldon", "nombre": "Sheldon", "precio": 120, "comprada": False,
     "imagenes": ["sheldon.jpg", "sheldon_think.jpg", "sheldon_llorar.jpg"]},

    {"id": "traje", "nombre": "Traje", "precio": 90, "comprada": False,
     "imagenes": ["traje.jpg", "traje_think.jpg", "traje_llorar.jpg"]}
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
    "basico": "basico.jpg",
    "cowboy": "cowboy.jpg",
    "dune": "dune.jpg",
    "enfado": "enfado.jpg",
    "navidad": "navidad.jpg",
    "pijama": "pijama.jpg",
    "pijo": "pijo.jpg",
    "pirata": "pirata.jpg",
    "sheldon": "sheldon.jpg",
    "traje": "traje.jpg"
}

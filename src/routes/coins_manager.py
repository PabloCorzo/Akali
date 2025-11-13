# model/coins_manager.py
from database import db
from model import Users


class CoinsManager:

    @staticmethod
    def add_coins(user_id, amount):
        """Añade monedas a un usuario"""
        user = Users.query.get(user_id)  # Esto usa la primary key automáticamente
        if user:
            user.coins += amount
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_balance(user_id):
        """Obtiene el balance de monedas de un usuario"""
        user = Users.query.get(user_id)
        return user.coins if user else 0
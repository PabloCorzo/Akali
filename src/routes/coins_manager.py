# model/coins_manager.py
from database import db
from model import Users
from datetime import datetime, timedelta


class CoinsManager:

    @staticmethod
    def add_coins(user_id, amount):
        """Añade monedas a un usuario"""
        user = Users.query.get(user_id)
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

    @staticmethod
    def can_claim_daily_coins(user_id):
        """Verifica si el usuario puede reclamar monedas diarias"""
        user = Users.query.get(user_id)
        if not user:
            return False, 0

        # Si nunca ha reclamado, puede reclamar
        if not user.last_daily_claim:
            return True, 0

        # Calcular tiempo transcurrido
        now = datetime.now()
        time_since_last_claim = now - user.last_daily_claim

        # Si han pasado 24 horas o más
        if time_since_last_claim >= timedelta(hours=24):
            return True, 0

        # Calcular horas restantes
        time_remaining = timedelta(hours=24) - time_since_last_claim
        hours_remaining = time_remaining.total_seconds() / 3600

        return False, hours_remaining

    @staticmethod
    def claim_daily_coins(user_id, amount=10):
        """Reclama las monedas diarias si es posible"""
        can_claim, hours_remaining = CoinsManager.can_claim_daily_coins(user_id)

        if can_claim:
            user = Users.query.get(user_id)
            if user:
                user.coins += amount
                user.last_daily_claim = datetime.now()
                db.session.commit()
                return True, f"¡Has recibido {amount} monedas! 🪙"

        return False, f"Vuelve dentro de {int(hours_remaining)} horas para reclamar tus monedas diarias! ⏰"
"""
Database module - Shared SQLAlchemy instance
Este módulo contiene la instancia de SQLAlchemy que será compartida
por todos los modelos y la aplicación Flask.
"""

from flask_sqlalchemy import SQLAlchemy

# Crear una única instancia de SQLAlchemy
db = SQLAlchemy()

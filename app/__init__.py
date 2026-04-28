import os
import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    # Register blueprints
    from app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.routes.recipe import bp as recipe_bp
    app.register_blueprint(recipe_bp)

    from app.routes.calendar import bp as calendar_bp
    app.register_blueprint(calendar_bp)

    from app.routes.shopping import bp as shopping_bp
    app.register_blueprint(shopping_bp)

    return app

def init_db():
    """Initializes the database using the schema.sql file."""
    db_path = os.path.join('instance', 'database.db')
    schema_path = os.path.join('database', 'schema.sql')
    
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    with sqlite3.connect(db_path) as conn:
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
    print("Database initialized.")

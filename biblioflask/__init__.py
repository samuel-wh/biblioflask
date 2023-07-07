from flask import Flask
from flask_bootstrap import Bootstrap
from .settings import Settings
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Settings)
    Bootstrap(app)
    db.init_app(app)
    migrar = Migrate(app, db, directory='biblioflask/migrations')
    
    from .apps.books.routes import books_bp
    from .apps.publishers.routes import publishers_bp
    from .apps.authors.routes import authors_bp

    app.register_blueprint(books_bp)
    app.register_blueprint(publishers_bp)
    app.register_blueprint(authors_bp)
    
    return app

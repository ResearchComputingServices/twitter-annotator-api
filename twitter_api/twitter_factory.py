import json

def create_app(package_name):
    from flask import Flask
    app = Flask(package_name)
    from twitter_api.extensions import db, ma, migrate, oidc

    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:admin@127.0.0.1:5432/twitter_data"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['USE_X_SENDFILE'] = True

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    #oidc.init_app(app)

    @app.route('/favicon.ico')
    def favi():
        return 'Hello FaviTown', 200

    return app

def register_blueprints(app):
    from twitter_api.web.views import twitter_bp
    app.register_blueprint(twitter_bp, url_prefix='/twitter_api')
    return app

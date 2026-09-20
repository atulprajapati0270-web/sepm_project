import os
from flask import Flask
from dotenv import load_dotenv
from .extensions import db, login_manager

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-change-me")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "sqlite:///smart_simhastha.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to continue."
    app.jinja_env.globals["getattr"] = getattr

    @app.context_processor
    def inject_lang():
        from flask import session
        current_lang = session.get('lang', 'hi')
        return {
            'lang': current_lang,
            'is_hindi': (current_lang == 'hi')
        }

    from .auth.routes import auth_bp
    from .main.routes import main_bp
    from .traffic.routes import traffic_bp
    from .accommodation.routes import accommodation_bp
    from .food.routes import food_bp
    from .medical.routes import medical_bp
    from .events.routes import events_bp
    from .shahi_snan.routes import shahi_snan_bp
    from .security.routes import security_bp
    from .temples.routes import temples_bp
    from .emergency.routes import emergency_bp
    from .complaints.routes import complaints_bp
    from .lost_found.routes import lost_found_bp
    from .notifications.routes import notifications_bp
    from .admin.routes import admin_bp
    from .maps.routes import maps_bp

    for bp in [
    main_bp, auth_bp, traffic_bp, accommodation_bp, food_bp, medical_bp,
    events_bp, shahi_snan_bp, security_bp, temples_bp, emergency_bp,
    complaints_bp, lost_found_bp, notifications_bp, admin_bp, maps_bp
]:
        app.register_blueprint(bp)

    return app

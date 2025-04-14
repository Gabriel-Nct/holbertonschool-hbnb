import os
from flask import Flask, render_template
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from config import config

bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()

def create_app(config_class="development"):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_dir, 'templates')
    static_path = os.path.join(os.path.dirname(current_dir), 'static')

    app = Flask(__name__, template_folder=template_path, static_folder=static_path)

    if isinstance(config_class, str):
        config_class = config[config_class]
    app.config.from_object(config_class)

    app.config['JWT_SECRET_KEY'] = app.config['SECRET_KEY']

    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    @app.route('/')
    @app.route('/index')
    def index():
        return render_template('index.html')

    @app.route('/login')
    def login():
        return render_template('login.html')
    
    @app.route('/place')
    def place():
        return render_template('place.html')
    
    @app.route('/review')
    def review():
        return render_template('add_review.html')
    

    @app.route('/place/<place_id>')
    def place_id(place_id):
        return render_template('place.html', place_id=place_id)
    
    @app.route('/review/<place_id>')
    def review_id(place_id):
        return render_template('add_review.html', place_id=place_id)


    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/swagger'
    )

    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.auth import api as auth_ns

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    with app.app_context():
        print("\n=== Routes enregistrées ===")
        for rule in app.url_map.iter_rules():
            print(f"{rule.rule} -> {rule.endpoint}")
        print("==========================\n")

    return app

"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Users, People, Planets, FavPeople, FavPlanet

app = Flask(__name__)
app.url_map.strict_slashes = False

# Database configuration
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and admin
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generate sitemap with all endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Routes for API

# GET Routes
@app.route('/people', methods=['GET'])
def handle_people():
    people = People.query.all()
    if not people:
        return jsonify({"msg": "No people found"}), 404
    return jsonify([person.serialize() for person in people]), 200

@app.route('/people/<int:person_id>', methods=['GET'])
def handle_person_id(person_id):
    person = People.query.get(person_id)
    if not person:
        return jsonify({"msg": f"Person with ID {person_id} not found"}), 404
    return jsonify(person.serialize()), 200

@app.route('/planets', methods=['GET'])
def handle_planets():
    planets = Planets.query.all()
    if not planets:
        return jsonify({"msg": "No planets found"}), 404
    return jsonify([planet.serialize() for planet in planets]), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def handle_planet_id(planet_id):
    planet = Planets.query.get(planet_id)
    if not planet:
        return jsonify({"msg": f"Planet with ID {planet_id} not found"}), 404
    return jsonify(planet.serialize()), 200

@app.route('/users', methods=['GET'])
def handle_users():
    users = Users.query.all()
    if not users:
        return jsonify({"msg": "No users found"}), 404
    return jsonify([user.serialize() for user in users]), 200

@app.route('/users/favorites', methods=['GET'])
def handle_users_favorites():
    user_id = 1  # Replace with the actual user ID from authentication
    fav_people = FavPeople.query.filter_by(user_id=user_id).all()
    fav_planets = FavPlanet.query.filter_by(user_id=user_id).all()

    favorites = {
        "people": [fav.serialize() for fav in fav_people],
        "planets": [fav.serialize() for fav in fav_planets],
    }
    return jsonify(favorites), 200

# POST Routes
@app.route('/favorite/people/<int:person_id>', methods=['POST'])
def add_fav_person(person_id):
    user_id = 1  # Replace with the actual user ID from authentication
    existing_fav = FavPeople.query.filter_by(user_id=user_id, people_id=person_id).first()
    if existing_fav:
        return jsonify({"msg": "Person already in favorites"}), 400

    new_fav = FavPeople(user_id=user_id, people_id=person_id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify({"msg": "Person added to favorites"}), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_fav_planet(planet_id):
    user_id = 1  # Replace with the actual user ID from authentication
    existing_fav = FavPlanet.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if existing_fav:
        return jsonify({"msg": "Planet already in favorites"}), 400

    new_fav = FavPlanet(user_id=user_id, planet_id=planet_id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify({"msg": "Planet added to favorites"}), 201

# DELETE Routes
@app.route('/favorite/people/<int:person_id>', methods=['DELETE'])
def delete_fav_person(person_id):
    user_id = 1  # Replace with the actual user ID from authentication
    fav = FavPeople.query.filter_by(user_id=user_id, people_id=person_id).first()
    if not fav:
        return jsonify({"msg": "Favorite person not found"}), 404

    db.session.delete(fav)
    db.session.commit()
    return jsonify({"msg": "Favorite person removed"}), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_fav_planet(planet_id):
    user_id = 1  # Replace with the actual user ID from authentication
    fav = FavPlanet.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if not fav:
        return jsonify({"msg": "Favorite planet not found"}), 404

    db.session.delete(fav)
    db.session.commit()
    return jsonify({"msg": "Favorite planet removed"}), 200

# Run the application
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    favorites = db.relationship('Favorite', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "favorites": [favorite.serialize() for favorite in self.favorites]
        }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id', ondelete="CASCADE"), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id', ondelete="CASCADE"), nullable=True)

    def __repr__(self):
        return f'<Favorite {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.character.name if self.character else self.planet.name,
            "character": self.character.serialize() if self.character else None,
            "planet": self.planet.serialize() if self.planet else None,
        }

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    hair_color = db.Column(db.String(50), nullable=True)
    eye_color = db.Column(db.String(50), nullable=True)
    character_img = db.Column(db.String(512), nullable=True)
    favorites = db.relationship('Favorite', backref='character', lazy=True)

    def __repr__(self):
        return f'<Character {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "character_img": self.character_img if self.character_img else None,
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    diameter = db.Column(db.Integer, nullable=True)
    climate = db.Column(db.String(50), nullable=True)
    population = db.Column(db.String(50), nullable=True)
    favorites = db.relationship('Favorite', backref='planet', lazy=True)

    def __repr__(self):
        return f'<Planet {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "climate": self.climate,
            "population": self.population,
        }
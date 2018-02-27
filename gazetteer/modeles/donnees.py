from flask import url_for
import datetime

from .. app import db

#on crée un modèle pour la typologie des relations.
class Relationship(db.Model):
    __tablename__ = "relationship"
    relationship_id = db.Column(db.Integer, nullable=True, autoincrement=True, primary_key=True)
    relationship_type= db.Column(db.String(45))
    #liaison avec la table connexion
    connexions =db.relationship("Connexion", back_populates="relationships")
#les éléments en relation avec l'API devront être repris.

#création de la table de concordances des relations entre les lieux.
class Connexion(db.Model):
    __tablename__="connexion"
    connexion_id = db.Column(db.Integer, nullable=True, autoincrement=True, primary_key=True)
    connexion_relationship_id = db.Column(db.Integer, db.ForeignKey('relationship.relationship_id'))
    connexion_from_place_id = db.Column(db.Integer, db.ForeignKey('place.place_id'))
    connexion_to_place_id= db.Column(db.Integer, db.ForeignKey('place.place_id'))
    #Spécification de la colonne qui doit être considérée selon le cas de place_id.
    connexion_from =db.relationship("Place", foreign_keys='connexion_from_place_id')
    connexion_to = db.relationship("Place", foreign_keys='connexion_to_place_id')
    #jointures avec les autres tables
    relationships =db.relationship("Relationship", back_populates="connexions")
    place = db.relationship("Place", back_populates="connexions")


class Authorship(db.Model):
    __tablename__ = "authorship"
    authorship_id = db.Column(db.Integer, nullable=True, autoincrement=True, primary_key=True)
    authorship_place_id = db.Column(db.Integer, db.ForeignKey('place.place_id'))
    authorship_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    authorship_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user = db.relationship("User", back_populates="authorships")
    place = db.relationship("Place", back_populates="authorships")

    def author_to_json(self):
        return {
            "author": self.user.to_jsonapi_dict(),
            "on": self.authorship_date
        }


# On crée notre modèle
class Place(db.Model):
    place_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    place_nom = db.Column(db.Text)
    place_description = db.Column(db.Text)
    place_longitude = db.Column(db.Float)
    place_latitude = db.Column(db.Float)
    place_type = db.Column(db.String(45))
    authorships = db.relationship("Authorship", back_populates="place")
    #jointure avec la table connexion.
    connexions = db.relationship("Connexion", back_populates="place")
    def to_jsonapi_dict(self):
        """ It ressembles a little JSON API format but it is not completely compatible

        :return:
        """
        return {
            "type": "place",
            "id": self.place_id,
            "attributes": {
                "name": self.place_nom,
                "description": self.place_description,
                "longitude": self.place_longitude,
                "latitude": self.place_latitude,
                "category": self.place_type
            },
            "links": {
                "self": url_for("lieu", place_id=self.place_id, _external=True),
                "json": url_for("api_places_single", place_id=self.place_id, _external=True)
            },
            "relationships": {
                 "editions": [
                     author.author_to_json()
                     for author in self.authorships
                 ]
            }
        }


    @staticmethod
    def creer_lieu(nom, latitude, longitude, description, type):
        erreurs = []
        if not nom:
            erreurs.append("Le nom du lieu est obligatoire")
        if not latitude:
            erreurs.append("Il faut indiquer la latitude")
        if not longitude:
            erreurs.append("Il faut indiquer la longitude")

        # On vérifie que personne n'a utilisé cet email ou ce login


        # Si on a au moins une erreur
        if len(erreurs) > 0:
            print(erreurs, nom, latitude, description, longitude)
            return False, erreurs

        lieu = Place(
            place_nom=nom,
            place_latitude=latitude,
            place_longitude=longitude,
            place_description=description,
            place_type=type,
            # changer le nom "type"
        )
        print(lieu)
        try:
            # On l'ajoute au transport vers la base de données
            db.session.add(lieu)
            # On envoie le paquet
            db.session.commit()

            # On renvoie l'utilisateur
            return True, lieu

        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def modif_lieu(id, nom, latitude, longitude, description, type):
        erreurs = []
        if not nom:
            erreurs.append("Le nom du lieu est obligatoire")
        if not latitude:
            erreurs.append("Il faut indiquer la latitude")
        if not longitude:
            erreurs.append("Il faut indiquer la longitude")

        # On vérifie que personne n'a utilisé cet email ou ce login


        # Si on a au moins une erreur
        if len(erreurs) > 0:
            print(erreurs, nom, latitude, description, longitude)
            return False, erreurs

        lieu = Place.query.get(id)

        lieu.place_nom = nom
        lieu.place_latitude = latitude
        lieu.place_description = description
        lieu.place_longitude = longitude
        lieu.place_type = type

        try:

            # On l'ajoute au transport vers la base de données
            db.session.add(lieu)
            # On envoie le paquet
            db.session.commit()

            # On renvoie l'utilisateur
            return True, lieu

        except Exception as erreur:
            return False, [str(erreur)]
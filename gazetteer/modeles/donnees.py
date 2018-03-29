from flask import url_for
import datetime
from .. app import db

class Authorship(db.Model):
    __tablename__ = "authorship"
    authorship_id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
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
#jointures
    authorships = db.relationship("Authorship", back_populates="place")
    relations = db.relationship("Relation", back_populates="place")
    link_place1 = db.relationship("link", primaryjoin="Place.place_id==Link.link_place1_id")
    link_place2= db.relationship("link", primaryjoin="Place.place_id==Link.link_place2_id")

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
    def creer_lieu(nom, latitude, longitude, description, typep):
        erreurs = []
        if not nom:
            erreurs.append("Le nom du lieu est obligatoire")
        if not latitude:
            erreurs.append("Il faut indiquer la latitude")
        if not longitude:
            erreurs.append("Il faut indiquer la longitude")

        # Si on a au moins une erreur
        if len(erreurs) > 0:
            print(erreurs, nom, latitude, description, longitude)
            return False, erreurs

        lieu = Place(
            place_nom=nom,
            place_latitude=latitude,
            place_longitude=longitude,
            place_description=description,
            place_type=typep,
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
    def modif_lieu(id, nom, latitude, longitude, description, typep):
        erreurs = []
        if not nom:
            erreurs.append("Le nom du lieu est obligatoire")
        if not latitude:
            erreurs.append("Il faut indiquer la latitude")
        if not longitude:
            erreurs.append("Il faut indiquer la longitude")

        # Si on a au moins une erreur
        if len(erreurs) > 0:
            print(erreurs, nom, latitude, description, longitude)
            return False, erreurs

        lieu = Place.query.get(id)

        lieu.place_nom=nom
        lieu.place_latitude=latitude
        lieu.place_description=description
        lieu.place_longitude=longitude
        lieu.place_type=typep

        try:

            # On l'ajoute au transport vers la base de données
            db.session.add(lieu)
            # On envoie le paquet
            db.session.commit()

            # On renvoie l'utilisateur
            return True, lieu

        except Exception as erreur:
            return False, [str(erreur)]


            #on crée notre classe de références bibliographiques
class Biblio(db.Model):
    biblio_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    biblio_titre = db.Column(db.Text, nullable=False)
    biblio_auteur = db.Column(db.Text, nullable=False)
    biblio_date = db.Column(db.Text)
    biblio_lieu = db.Column(db.Text)
    biblio_type = db.Column(db.Text, nullable=False)
    relations = db.relationship("Relation", back_populates="biblio")

    def to_jsonapi_dict(self):
        """ It ressembles a little JSON API format but it is not completely compatible

        :return:
        """
        return {
            "type": "biblio",
            "id": self.biblio_id,
            "attributes": {
                "titre": self.biblio_titre,
                "auteur": self.biblio_auteur,
                "date": self.biblio_date,
                "lieu": self.biblio_lieu,
                "category": self.place_type
            },
            "links": {
                "self": url_for("biblio", biblio_id=self.biblio_id, _external=True),
                "json": url_for("api_biblios_single", biblio_id=self.biblio_id, _external=True)
            },

        }

    @staticmethod
    def creer_biblio(titre, auteur, date, lieu, typep):
        """ Crée une nouvelle référence bibliographique et renvoie les informations entrées par l'utilisateur
        :param titre: Titre de la référence
        :param auteur: Auteur de la référence
        :param date: Date de publication de la référence
        :param lieu: Lieu de publication de la référence
        :param type: Type de publication
        """
        erreurs = []
        if not titre:
            erreurs.append("Le titre de l'oeuvre est obligatoire")
        if not auteur:
            erreurs.append("Il faut indiquer l'auteur")
        if not typep:
            erreurs.append("Il faut indiquer le type d'oeuvre : article ou livre")

        # Si on a au moins une erreur
        if len(erreurs) > 0:
            print(erreurs, titre, auteur, typep)
            return False, erreurs

        biblio = Biblio(
            biblio_titre=titre,
            biblio_auteur=auteur,
            biblio_date=date,
            biblio_lieu=lieu,
            biblio_type=typep,
            # changer le nom "type"
        )
        print (biblio)

        try:
            # On l'ajoute au transport vers la base de données
            db.session.add(biblio)
            # On envoie la référence
            db.session.commit()

            return True, biblio

        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def modif_biblio(id, titre, auteur, date, lieu, typep):
        erreurs = []
        if not titre:
            erreurs.append("Le titre est obligatoire")
        if not auteur:
            erreurs.append("L'auteur est obligatoire")
        if not typep:
            erreurs.append("Il faut indiquer le type d'ouvrage")

        # Si on a au moins une erreur
        if len(erreurs) > 0:
            print(erreurs, titre, auteur, date, lieu, typep)
            return False, erreurs

        biblio = Biblio.query.get(id)

        biblio.biblio_titre=titre
        biblio.biblio_auteur=auteur
        biblio.biblio_date=date
        biblio.biblio_lieu=lieu
        biblio.biblio_type=typep

        try:

            # On l'ajoute au transport vers la base de données
            db.session.add(biblio)
            # On envoie le paquet
            db.session.commit()

            # On renvoie l'utilisateur
            return True, biblio

        except Exception as erreur:
            return False, [str(erreur)]

class Relation(db.Model):
    __tablename__ = "relation"
    relation_id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    relation_place_id = db.Column(db.Integer, db.ForeignKey('place.place_id'))
    relation_biblio_id = db.Column(db.Integer, db.ForeignKey('biblio.biblio_id'))
    biblio = db.relationship("Biblio", back_populates="relations")
    place = db.relationship("Place", back_populates="relations")

#création d'une classe pour les connexions entre les lieux
class link(db.Model):
    __tablename__="link"
    link_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    link_place1_id =db.Column(db.Integer, db.ForeignKey('place.place_id'))
    link_place2_id= db.Column(db.Integer, db.ForeignKey('place.place_id'))
    link_relation_type = db.Colum(db.String(240), nullable=False)
#jointures
    place1 = db.relationship("Place", foreign_keys=[link_place1_id])
    place2 = db.relationship ("Place", foreign_keys= [link_place2_id])
    # création de la gestions des liens entre les lieux.
    @staticmethod
    def creer_link(link_place1, link_relation_type, link_place2):
# vérif des champs
if not ( (len(link_place1) == len (link_place2)) and (len (link_place1) == len(link_relation_type) )   and (len(link_place2) == len (link_relation_type)) ):
            erreurs.append("Tous les champs doivent être remplis")

# Initialisation de la boucle
            loop = len(link_place1)
# comparaison des lignes
            tuples = []
            reprise = 0
for row in range (0, loop):
            tuple = (link_place1[row], link_relation_type[row], link_place2[row])
for trio in tuples:
    if tuples == trio:
                repeat += 1
                tuples.append(tuple)
#si erreur
if reprise > 0:
            errors.append("certains liens à créer sont identiques")
# Verif de la sélection du champs type et que les lieux sont différents.
for row in range (0, loop):
    if link_relation_type[row] == 'Choisir':
                errors.append("aucun type de relation n'a été sélectionné, ligne " + str(row +1))
    if link_place1[row] == link_place2[row]:
                errors.append("les champs 'Lieu 1' et 'Lieu 2' sont identiques, ligne " + str(row +1))
#si erreurs.
    if len(errors) > 0:
        return False, errors
# On vérifie les ID sont valides
for row in range (0, loop):
            place1 = Place.query.filter(Place.place_id == link_place1[row]).count()
            place2 = Place.query.filter(Place.place_id == link_place2[row]).count()
            if place1 == 0:
                errors.append(link_place1[row] +" n'existe pas, ligne " + str(row +1))
            if place2 == 0:
                errors.append(link_place2[row] +" n'existe pas, ligne " + str(row +1))

# Création d'un nv lien :
liste_link = []
for row in range (0, loop):
# on réinitialise la variable
            liaison = Link_type.query.filter(Link_type.Link_type_name == link_relation_type[row]).all()
            creer_link.append(
                Link(
link_place1_id=link_place1[row],
link_relation_type_id=str(link_relation_type[row]),
link_place2_id=link_place2[row]
                    )
                )
try:
    for row in range (0, loop):
#ajout à la DB.
                db.session.add(creer_link[row])
                db.session.commit()
# Renvoie vers l'utilisateur :
return True, creer_link

# Si erreurs
except Exception as error_creation:
return False, [str(error_creation)]

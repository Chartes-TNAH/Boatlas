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

#creation d'une table de liaison entre link et Place
links=db.Table('links',
    db.Column('link_id', db.Integer, db.ForeignKey('link.link_id')),
    db.Column('link_place1_id', db.Integer, db.ForeignKey('place.place_id')),
    db.Column('link_place2_id', db.Integer, db.ForeignKey('place.place_id')),
    )

# On crée une class link pour gérer la nature des relations.
class Link(db.Model):
    link_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    link_relation_type = db.Column(db.String(45), nullable=False)
    link_relation_description = db.Column(db.String(240))
    typed = db.relationship(
        'Link', secondary=links,
        backref=db.backref('link', lazy='dynamic'))

def to_jsonapi_dict(self):
    """ It ressembles a little JSON API format but it is not completely compatible
    :return:
    """
    return {
        "type": "place",
        "id": self.link_id,
        "attributes": {
            "type": self.link_relation_type,
            "description": self.link_relation_description
             }

        }
# On crée notre modèle
class Place(db.Model):
    #__tablename__ = "left"
    place_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    place_nom = db.Column(db.Text)
    place_description = db.Column(db.Text)
    place_longitude = db.Column(db.Float)
    place_latitude = db.Column(db.Float)
    place_type = db.Column(db.String(45))
#jointures
    authorships = db.relationship("Authorship", back_populates="place")
    #biblios = db.relationship("Biblio", primaryjoin="Place.place_id==Relation.relation_biblio_id")
    relations = db.relationship("Relation", back_populates="place")
#    link_place1 = db.relationship("link", primaryjoin="Place.place_id==link.link_place1_id")
#    link_place2= db.relationship("link", primaryjoin="Place.place_id==link.link_place2_id")
#    liens=db.relationship("link", back_populates="place")
#création d'un mapping avec la table de liaison
    linked = db.relationship(
        'Place', secondary=links,
        primaryjoin=(links.c.link_place1_id == place_id),
        secondaryjoin=(links.c.link_place2_id == place_id),
        backref=db.backref('place', lazy='dynamic'), lazy='dynamic')

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
                 ],
                 "references": [
                 relation.to_jsonapi_dict()
                          for relation in self.relations
                      ]
                 }

            }


    @staticmethod
    def modif_link(id,lieu_1, lieu_2, type, description):
        erreurs = []
        if not lieu_1:
            erreurs.append("Le lieu 1 est nécessaire")
        if not lieu_2:
            erreurs.append("Le lieu 2 est nécessaire")

        # Si les deux lieux sont identiques:
        if lieu_1 == lieu_2:
            erreurs.append("Les deux lieux sont identiques")

        if not type== "topographique" or type=="administrative" or type=="historique":
            erreurs.append("Le type est obligatoire: administrative, topographique ou historique")

        # Si on a au moins une erreur
        if len(erreurs) > 0:
            print(erreurs, titre, auteur, date, lieu, typep)
            return False, erreurs

        connection = link.query.join(link, (links.c.link_id == links.link_id)).get(id)

        link.link_id=id
        link.link_relation_type=type
        link.link_relation_description=description
        links.link_place1_id=type
        links.link_place2_id=description

        try:

            # On l'ajoute au transport vers la base de données
            db.session.add(connection)
            # On envoie le paquet
            db.session.commit()

            # On renvoie l'utilisateur
            return True, connection

        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def create_link(lieu_1, lieu_2):
        erreurs=[]
        if not lieu_1:
            erreurs.append("Le lieu 1 est nécessaire")
        if not lieu_2:
            erreurs.append("Le lieu 2 est nécessaire")

        #ajouter une fonction car les deux lieux ne peuvent être identiquesself.
        if lieu_1 == lieu_2:
            erreurs.append("Le lieu 1 et le lieu 2 ne peuvent pas être identiques")

        #il faudrait vérifier qu'aucune connexion n'a été faite entre ces deux lieux...
        if not self.is_linked(place):
            self.linked.append(place)
        # si on a une erreur
        if len(erreurs)>o:
            print(erreurs,lieu_1, lieu_2)
            return False, erreurs

        connection= links(
        link_place1_id=lieu_1,
        link_place2_id=lieu_2,
        )
        print(connection)
        try:
            # On l'ajoute au transport vers la base de données
            db.session.add(connection)
            # On envoie le paquet
            db.session.commit()

            # On renvoie l'utilisateur
            return True, connection

        except Exception as erreur:
            return False, [str(erreur)]

#join impossible car création pas d'id attribué pour faire la jonction. La solution est de créer la liaison entre les deux lieux, puis de renvoyer directement au template de modif depuis celui de création.
    """connection = link.query.join(link, (links.c.link_id == links.link_id)) (
        link_place1_id=lieu_1,
        link_place2_id=lieu_2,
        link_relation_type = type,
        link_relation_description = description,
        )"""
    def is_linked (self, place):
        return self.liked.filter(links.c.link_place2_id == place_id).count() > 0

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
    #__tablename__ = "right"
    biblio_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    biblio_titre = db.Column(db.Text, nullable=False)
    biblio_auteur = db.Column(db.Text, nullable=False)
    biblio_date = db.Column(db.Text)
    biblio_lieu = db.Column(db.Text)
    biblio_type = db.Column(db.Text, nullable=False)
#Jointure
    relations = db.relationship("Relation", back_populates="biblio")

    def to_jsonapi_dict(self):
        """ Semblant d'API en JSON mais défauts de compatibilité
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
                "category": self.place_type,
                "relationships": self.relations,
            },
            "links": {
                "self": url_for("biblio", biblio_id=self.biblio_id, _external=True),
                "json": url_for("api_biblios_single", biblio_id=self.biblio_id, _external=True)
            },

            "relationships": {
                 "lieux" : [
                          relation.to_json_dict()
                          for relation in self.relations
                      ]
                 }

        }

            #manque retour de lieu vers biblio


    @staticmethod
    def creer_biblio(titre, auteur, date, lieu, typep):
        """ Crée une nouvelle référence bibliographique et
        renvoie les informations entrées par l'utilisateur
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
#Jointure
    biblio = db.relationship("Biblio", back_populates="relations")
    place = db.relationship("Place", back_populates="relations")

    def to_jsonapi_dict(self):
        """ It ressembles a little JSON API format but it is not completely compatible
        :return:
        """
        return {
            "type": "relation",
            "id": self.relation_id,
            "attributes": {
                "lieu": self.relation_place_id,
                "reference": self.relation_biblio_id,
                "biblio": self.biblio,
                "place": self.place,
            },
            "links": {
                "self": url_for("relation", relation_id=self.relation_id, _external=True),
                "json": url_for("api_relations_single", relation_id=self.relation_id, _external=True)
            },
            "relationships":{
            "lieux":self.place.to_jsonapi_dict(),
            "references":self.biblio.to_jsonapi_dict(),
            }

        }

    @staticmethod
    def associer_reference(biblio_id, place_id):
        """ Crée une nouvelle relation entre un lieu et
        une référence. La fonction renvoie les informations
        entrées par l'utilisateur
        """
        erreurs = []
        if not biblio_id:
            erreurs.append("Le biblio_id est obligatoire")
        if not place_id:
            erreurs.append("Il faut indiquer le place_id")


        # Si on a au moins une erreur
        if len(erreurs) > 0:
            print(erreurs, biblio_id, place_id)
            return False, erreurs

        liaison = Relation(
            relation_biblio_id=biblio_id,
            relation_place_id=place_id,

            # changer le nom "type"
        )
        print (liaison)

        try:
            # On l'ajoute au transport vers la base de données
            db.session.add(liaison)
            # On envoie la référence
            db.session.commit()

            return True, liaison

        except Exception as erreur:
            return False, [str(erreur)]



"""
#création d'une classe pour les connexions entre les lieux
class link(db.Model):
    __tablename__="link"
    link_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#    link_place1_id =db.Column(db.Integer, db.ForeignKey('place.place_id'))
#    link_place2_id= db.Column(db.Integer, db.ForeignKey('place.place_id'))
    link_relation_type = db.Column(db.String(45), nullable=False)
    link_relation_description = db.Column(db.String(240))
#jointures
#    place1 = db.relationship("Place", foreign_keys=[link_place1_id])
#    place2 = db.relationship ("Place", foreign_keys= [link_place2_id])
    place=db.relationship("Place", back_populates="link") # si seulement ce fragment de code crée: sqlalchemy.exc.AmbiguousForeignKeysError: Could not determine join condition between parent/child tables on relationship Place.liens-
    #, primaryjoin=link_place1_id==Place.place_id)
    place=db.relationship("Place", back_populates="link") #, primaryjoin=link_place2_id==Place.place_id) ce fragment de code crée : One or more mappers failed to initialize - can't proceed with initialization of other mappers. Triggering mapper: 'Mapper|Place|place'
    # création de la gestions des liens entre les lieux."""
"""
    @staticmethod
    def creer_liaison(lieu1, relation, lieu2, description):
        Crée une nouvelle connexion entre deux lieux.
        :param lieu1: Lieu 1 de la relation
        :param lieu2: lieu 2 de la relation
        :param relation: type de la relation
        :param description: description de la relation


# vérif des champs
        erreurs = []
        if not lieu1:
            erreurs.append("Il faut un lieu 1 pour créer une relation entre deux lieux")
        #if not relation:
        #    erreurs.append("Il faut une nature pour caractériser la relation entre deux lieux")
        if not lieu2:
            erreurs.append("Il faut un lieu 2 pour créer une relation entre deux lieux")
        if lieu1 == lieu2:
            erreurs.append("Une relation ne peut se faire qu'entre deux lieux différents. ")
# retrait de cette ligne qui crée un bug.
        #if not relation =="historique" or relation=="administrative" or relation=="topographique":
            erreurs.append("La nature de la relation doit être administrative, topographique ou historique. ")
        # Si on a au moins une erreur
        if len(erreurs) > 0:
            return False, erreurs

        lien= link(
                    link_place1_id=lieu1,
                    link_relation_type=relation,
                    link_place2_id=lieu2,
                    link_relation_description=description
                        )

        print(link)

        try:
            #envoie vers la db
            db.session.add(link)
            #envoie de la liaison.
            db.session.commit()

            return True, lien

        except Exception as erreur:
            return False, [str(erreur)]
# comparaison des lieu1 et lieu2"""

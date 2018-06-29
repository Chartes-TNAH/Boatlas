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
#links=db.Table('links',
#    db.Column('link_id', db.Integer, db.ForeignKey('link.link_id')),
#    db.Column('link_place1_id', db.Integer, db.ForeignKey('place.place_id')),
#    db.Column('link_place2_id', db.Integer, db.ForeignKey('place.place_id')),
#    )
"""
# On crée une class link pour gérer la nature des relations.
class Link_relation(db.Model):
    nature_id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    link_relation_type = db.Column(db.String(45), nullable=False)
    link_relation_description = db.Column(db.String(240))
    typed = db.relationship("Link", back_populates="links")

#classe Relation
class Link(db.Model):
    #Création d'une table d'associations entre table Nature
    #et la table Place
    __tablename__ = "link"
    link_id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    nature_id = db.Column(db.Integer, db.ForeignKey('link_relation.nature_id'))
    link_place1_id = db.Column(db.Integer, db.ForeignKey('place.place_id'))
    link_place2_id = db.Column(db.Integer, db.ForeignKey('place.place_id'))
#Jointure
    links = db.relationship("Link_relation", back_populates="typed")
    lien = db.relationship("Place", back_populates="connexions")

def to_jsonapi_dict(self):
    #It ressembles a little JSON API format but it is not completely compatible
    #:return:

    return {
        "type": "place",
        "id": self.link_id,
        "attributes": {
            "type": self.link_relation_type,
            "description": self.link_relation_description
             }

        }
"""
# On crée notre modèle
class Place(db.Model):
    """Définit une classe lieu sur le modèle SQL"""
    place_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    place_nom = db.Column(db.Text)
    place_description = db.Column(db.Text)
    place_longitude = db.Column(db.Float)
    place_latitude = db.Column(db.Float)
    place_type = db.Column(db.String(45))
#jointure biblio & utilisateur
    authorships = db.relationship("Authorship", back_populates="place")
    relations = db.relationship("Relation", back_populates="place")
#sans prise en compte de l'ordre des deux place_id.
    #connexions = db.relationship("Link", )
    """connexions = db.relationship(
          "Place", secondary="Link",
            primaryjoin="Link.c.link_place1_id == place_id",
            secondaryjoin="Link.c.link_place2_id == place_id",
            back_populates="lien")"""

    def to_jsonapi_dict(self):
        """ It ressembles a little JSON API format
        but it is not completely compatible

        Affichage des données d'un lieu lorsque celui-ci
        n'est pas lié à une donnée bibliographique
        :return: dictionnaire
        """
        return {
            "relations": {
                "editions": [
                    author.author_to_json()
                    for author in self.authorships
                ],
                # biblio fait référence à ce sur quoi l'on boucle
                "references": [reference.association_to_json()
                               for reference in self.relations]},
                "type": "place",
                "id": self.place_id,
                "attributes": {
                    "name": self.place_nom,
                    "description": self.place_description,
                    "longitude": self.place_longitude,
                    "latitude": self.place_latitude,
                    "category": self.place_type,

                },
                "links": {
                    "self": url_for("lieu", place_id=self.place_id, _external=True),
                    "json": url_for("api_places_single", place_id=self.place_id, _external=True),
                },

            }

    def to_jsonapi_2_dict(self):
        """
        Fonction pour gérer l'affichage des données
        sans redondance
        en cas de relation
        entre une donnée bibliographique et un lieu dans l'API
        :return: dictionnaire data
        """
        data = {
            "editions":[
            author.author_to_json()
            for author in self.authorships
            ],
            #biblio fait référence à ce sur quoi l'on boucle
                "relation":[reference.association_to_json()
                 for reference in self.relations
                              ]

             }
        return data


    def to_jsonapi_dict_2(self):
        """
        Fonction pour gérer l'affichage des lieux
        dans le moteur de recherche de l'API
        :return: dictionnaire data
        """
        data = {
            "type": "place",
            "id": self.place_id,
            "attributes": {
                "name": self.place_nom,
                "description": self.place_description,
                "longitude": self.place_longitude,
                "latitude": self.place_latitude,
                "category": self.place_type,

            },
            "links": {
                "json": url_for("api_places_single", place_id=self.place_id, _external=True),
                "self": url_for("lieu", place_id=self.place_id, _external=True)
            }
        }
        return data

    def dictionnaire_2(self):
        """
        Fonction pour gérer l'affichage des infos de la donnée bibliographique
        en cas de relation avec un lieu dans l'API
        :return: dictionnaire data
        """
        data = {
                "id": self.place_id,
                "type" : "place",
                    "attributes": {
                    "name": self.place_nom,
                    "description": self.place_description,
                    "longitude": self.place_longitude,
                    "latitude": self.place_latitude,
                    "category": self.place_type,

                },
                "links": {
                    "self": url_for("lieu", place_id=self.place_id, _external=True),
                    "json": url_for("api_places_single", place_id=self.place_id, _external=True)
                    }
        }
        return data

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

        connection = link.query.join(link, (link.c.link_id == links.link_id)).get(id)

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
    def create_link(link_id,lieu_1, lieu_2):
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

        connection= link(
        link_id=id,
        link_place1_id=lieu_1,
        link_place2_id=lieu_2
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
        """Création d'un lieu:
        :param nom: nom du lieu
        :param latitude: latitude du lieu
        :param longitude: longitude du lieu
        :param description: description succinte du lieu
        :param typep: détermine la nature du lieu
        returns: liste"""
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
        """Modification d'un lieu:
        :param nom: nom du lieu
        :param latitude: latitude du lieu
        :param longitude: longitude du lieu
        :param description: description succinte du lieu
        :param typep: détermine la nature du lieu
        returns: liste"""
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
    """Création d'une classe biblio sur le modèle SQL"""
    biblio_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    biblio_titre = db.Column(db.Text, nullable=False)
    biblio_auteur = db.Column(db.Text, nullable=False)
    biblio_date = db.Column(db.Text)
    biblio_lieu = db.Column(db.Text)
    biblio_type = db.Column(db.Text, nullable=False)
#Jointure
    relations = db.relationship("Relation", back_populates="biblio")

    def to_jsonapi_dict(self):
        """
        Semblant d'API en JSON mais défauts de compatibilité
        Fonction pour gérer l'affichage d'une donnée bibliographique
        lorsque celle-ci n'est pas en relation avec un lieu dans l'API
        :return: dictionnaire data
        """
        data = {
            "type": "biblio",
            "id": self.biblio_id,
            "attributes": {
                "titre": self.biblio_titre,
                "auteur": self.biblio_auteur,
                "date": self.biblio_date,
                "lieu": self.biblio_lieu,
                "category": self.biblio_type,

            },
            "links": {
                "self": url_for("biblio", biblio_id=self.biblio_id, _external=True),
                "json": url_for("api_biblios_single", biblio_id=self.biblio_id, _external=True)
            },

            "relationships": {
                "endroits": [
                    endroit.association_to_json()
                    for endroit in self.relations
                ]
            }}
        return data

    def to_jsonapi_2_dict(self):
        """ Semblant d'API en JSON mais défauts de compatibilité
        Fonction pour gérer l'affichage sans redondance
        des infos d'une donnée bibliographique
        en cas de relation avec un lieu
        :return: dictionnaire data
        """
        data = {
            "infos": [
                endroit.association_to_json()
                for endroit in self.relations
            ]
        }
        return data

    def to_jsonapi_dict_2(self):
        """
        Fonction pour gérer l'affichage des données bibliographiques
        dans le moteur de recherche dans l'API
        :return: dictionnaire data
        """
        data = {
            "type": "biblio",
            "id": self.biblio_id,
            "attributes": {
                "titre": self.biblio_titre,
                "auteur": self.biblio_auteur,
                "date": self.biblio_date,
                "lieu": self.biblio_lieu,
                "category": self.biblio_type,

            },
            "links": {
                "self": url_for("biblio", biblio_id=self.biblio_id, _external=True),
                "json": url_for("api_biblios_single", biblio_id=self.biblio_id, _external=True)
            }}
        return data

    def dictionnaire_2(self):
        """ Semblant d'API en JSON mais défauts de compatibilité
        Pour gérer l'affichage des infos de la table lieu
        si la donnée bibliographique est en relation avec un lieu
        :return: dictionnaire data
        """
        data = {
            "id": self.biblio_id,
            "attributes": {
                "titre": self.biblio_titre,
                "auteur": self.biblio_auteur,
                "date": self.biblio_date,
                "category": self.biblio_type,
                 "type": "biblio",

            },
            "links": {
                "self": url_for("biblio", biblio_id=self.biblio_id, _external=True),
                "json": url_for("api_biblios_single", biblio_id=self.biblio_id, _external=True)
            }}
        return data


    @staticmethod
    def creer_biblio(titre, auteur, date, lieu, typep):
        """ Crée une nouvelle référence bibliographique et
        renvoie les informations entrées par l'utilisateur
        :param titre: Titre de la référence
        :param auteur: Auteur de la référence
        :param date: Date de publication de la référence
        :param lieu: Lieu de publication de la référence
        :param type: Type de publication
        returns: list
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
        """ Modifie une référence bibliographique et
        renvoie les informations entrées par l'utilisateur
        :param titre: Titre de la référence
        :param auteur: Auteur de la référence
        :param date: Date de publication de la référence
        :param lieu: Lieu de publication de la référence
        :param type: Type de publication
        returns: list
        """
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

    @staticmethod
    def supprimer_biblio(id, titre, auteur, date, lieu, typep):
        """
        Fonction supprimant la donnée bibliographique
        :param biblio_id: identifiant de la donnée bibliographique conservé dans la table d'association
        :returns: booleen
        """

        biblio = Biblio.query.get(id)
        biblio.biblio_titre = titre
        biblio.biblio_auteur = auteur
        biblio.biblio_date = date
        biblio.biblio_lieu = lieu
        biblio.biblio_type = typep


        try:
            db.session.delete(biblio)
            db.session.commit()
            return True, biblio

        except Exception as erreur:
            return False, [str(erreur)]


#classe Relation
class Relation(db.Model):
    """Création d'une table d'associations entre table Biblio
    et la table Place"""
    __tablename__ = "relation"
    relation_id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    relation_place_id = db.Column(db.Integer, db.ForeignKey('place.place_id'))
    relation_biblio_id = db.Column(db.Integer, db.ForeignKey('biblio.biblio_id'))
#Jointure
    biblio = db.relationship("Biblio", back_populates="relations")
    place = db.relationship("Place", back_populates="relations")

#Problème de boucle dans la boucle pour l'API
    def association_to_json(self):
        return {
            "biblio": self.biblio.dictionnaire_2(),
            "place": self.place.dictionnaire_2()
        }

    @staticmethod
    def associer_reference(biblio_id, place_id):
        """ Crée une nouvelle relation entre un lieu et
        une référence. La fonction renvoie les informations
        entrées par l'utilisateur
        :param biblio_id: identifiant de la référence bibliographique
        :param place_id: identifiant du lieu
        returns: list
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

    @staticmethod
    def supprimer_association(relation_place_id, relation_biblio_id, relation_id):
        """
        Fonction supprimant la relation entre
        le lieu et la reference bibliographique
        :param relation_place_id: identifiant du lieu conservé dans la table d'association
        :param relation_biblio_id: identifiant de la référence conservé dans la table d'association
        :param relation_id: identifiant de la relation
        :returns: booleen
        """

        relation_id = Relation.query.get(relation_id)
        relation_biblio_id=relation_biblio_id,
        relation_place_id=relation_place_id

        try:
            db.session.delete(relation_id)
            db.session.commit()
            return True, lieu

        except Exception as erreur:
            return False, [str(erreur)]

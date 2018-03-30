from flask import render_template, request, flash, redirect
from flask_login import current_user, login_user, logout_user, login_required

from ..app import app, login
from ..constantes import LIEUX_PAR_PAGE
from ..modeles.donnees import Place, Biblio, Relation, Authorship
from ..modeles.utilisateurs import User


@app.route("/")
def accueil():
    """ Route permettant l'affichage d'une page accueil
    """
    # On a bien sûr aussi modifié le template pour refléter le changement
    lieux = Place.query.order_by(Place.place_id.desc()).limit(5).all()
    return render_template("pages/accueil.html", nom="Gazetteer", lieux=lieux)


@app.route("/place/<int:place_id>")
def lieu(place_id):
    """ Route permettant l'affichage des données d'un lieu
    :param place_id: Identifiant numérique du lieu
    """
    # On a bien sûr aussi modifié le template pour refléter le changement
    unique_lieu = Place.query.get(place_id)
#Après avoir capturé un objet dans la variable unique_lieu
    reference = unique_lieu.relations
#Je capture dans une varible la liste des relations
    #lien = Relation.query.get(1)
    print(reference)
    #print(lien)
    return render_template("pages/place.html", nom="Gazetteer", lieu=unique_lieu, reference=reference)


@app.route("/recherche")
def recherche():
    """ Route permettant la recherche plein-texte
    """
    # On préfèrera l'utilisation de .get() ici
    #   qui nous permet d'éviter un if long (if "clef" in dictionnaire and dictonnaire["clef"])
    motclef = request.args.get("keyword", None)
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    # On crée une liste vide de résultat (qui restera vide par défaut
    #   si on n'a pas de mot clé)
    resultats = []

    # On fait de même pour le titre de la page
    titre = "Recherche"
    if motclef:
        resultats = Place.query.filter(
            Place.place_nom.like("%{}%".format(motclef))
        ).paginate(page=page, per_page=LIEUX_PAR_PAGE)
        titre = "Résultat pour la recherche `" + motclef + "`"

    return render_template(
        "pages/recherche.html",
        resultats=resultats,
        titre=titre,
        keyword=motclef
    )

@app.route("/recherche_biblio")
def recherche_biblio():
    """ Route permettant la recherche plein-texte
    """
    # On préfèrera l'utilisation de .get() ici
    #   qui nous permet d'éviter un if long (if "clef" in dictionnaire and dictonnaire["clef"])
    motclef = request.args.get("keyword", None)
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    # On crée une liste vide de résultat (qui restera vide par défaut
    #   si on n'a pas de mot clé)
    resultats = []

    # On fait de même pour le titre de la page
    titre = "Recherche_biblio"
    if motclef:
        resultats = Biblio.query.filter(
            Biblio.biblio_titre.like("%{}%".format(motclef))
        ).paginate(page=page, per_page=LIEUX_PAR_PAGE)
        titre = "Résultat pour la recherche `" + motclef + "`"

    return render_template(
        "pages/recherche_biblio.html",
        resultats=resultats,
        titre=titre,
        keyword=motclef
    )

@app.route("/browse")
def browse():
    """ Route permettant la recherche plein-texte
    """
    # On préfèrera l'utilisation de .get() ici
    #   qui nous permet d'éviter un if long (if "clef" in dictionnaire and dictonnaire["clef"])
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    resultats = Place.query.paginate(page=page, per_page=LIEUX_PAR_PAGE)

    return render_template(
        "pages/browse.html",
        resultats=resultats
    )

@app.route("/register", methods=["GET", "POST"])
def inscription():
    """ Route gérant les inscriptions
    """
    # Si on est en POST, cela veut dire que le formulaire a été envoyé
    if request.method == "POST":
        statut, donnees = User.creer(
            login=request.form.get("login", None),
            email=request.form.get("email", None),
            nom=request.form.get("nom", None),
            motdepasse=request.form.get("motdepasse", None)
        )
        if statut is True:
            flash("Enregistrement effectué. Identifiez-vous maintenant", "success")
            return redirect("/")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/inscription.html")
    else:
        return render_template("pages/inscription.html")


@app.route("/connexion", methods=["POST", "GET"])
def connexion():
    """ Route gérant les connexions
    """
    if current_user.is_authenticated is True:
        flash("Vous êtes déjà connecté-e", "info")
        return redirect("/")
    # Si on est en POST, cela veut dire que le formulaire a été envoyé
    if request.method == "POST":
        utilisateur = User.identification(
            login=request.form.get("login", None),
            motdepasse=request.form.get("motdepasse", None)
        )
        if utilisateur:
            flash("Connexion effectuée", "success")
            login_user(utilisateur)
            return redirect("/")
        else:
            flash("Les identifiants n'ont pas été reconnus", "error")

    return render_template("pages/connexion.html")
login.login_view = 'connexion'


@app.route("/deconnexion", methods=["POST", "GET"])
def deconnexion():
    if current_user.is_authenticated is True:
        logout_user()
    flash("Vous êtes déconnecté-e", "info")
    return redirect("/")

@app.route("/depot", methods=["POST", "GET"])
@login_required
def depot():
    if request.method == "POST":
        status, donnees = Place.creer_lieu(
            nom=request.form.get("nom", None),
            latitude=request.form.get("lat", None),
            longitude=request.form.get("longt", None),
            description=request.form.get("desc", None),
            typep=request.form.get("typep", None),

        )
        if status is True:
            flash("Enregistrement effectué. Vous avez ajouté un nouveau lieu", "success")
            return redirect("/")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/depot.html")
    else:
        return render_template("pages/depot.html")

@app.route("/modif_lieu/<int:place_id>")
@login_required
def modif_lieu(place_id):
    status, donnees = Place.modif_lieu(
        id=place_id,
        nom=request.args.get("nom", None),
        latitude=request.args.get("latitude", None),
        longitude=request.args.get("longitude", None),
        description=request.args.get("description", None),
        typep=request.args.get("typep", None)
    )

    if status is True :
        flash("Merci pour votre contribution !", "success")
        unique_lieu = Place.query.get(place_id)
        return redirect("/") #vers le lieu qu'il vient de créer.

    else:
        flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
        unique_lieu = Place.query.get(place_id)
        return render_template("pages/modif_lieu.html", lieu=unique_lieu)

@app.route("/creer_biblio", methods=["POST", "GET"])
def creer_biblio():
    if request.method == "POST":
        statut, donnees = Biblio.creer_biblio(
            titre=request.form.get("titre", None),
            auteur=request.form.get("auteur", None),
            date=request.form.get("date", None),
            lieu=request.form.get("lieu", None),
            typep=request.form.get("typep", None)
        )
        if statut is True:
            flash("Enregistrement effectué. Vous avez ajouté une nouvelle référence bibliographique", "success")
            return redirect("/")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/creer_biblio.html")
    else:
        return render_template("pages/creer_biblio.html")


@app.route("/biblio/<int:biblio_id>")
def biblio(biblio_id):
    """ Route permettant l'affichage des données d'un lieu
    :param biblio_id: Identifiant numérique de la référence bibliographique
    """
    # On récupère le tuple correspondant aux champs de la classe Biblio
    unique_biblio = Biblio.query.get(biblio_id)
    lieux = unique_biblio.relations
#Je capture dans une varible la liste des relations
    print(lieux)
    return render_template("pages/biblio.html", nom="Gazetteer", biblio=unique_biblio, lieux=lieux)

@app.route("/modif_biblio/<int:biblio_id>", methods=["POST", "GET"])
@login_required
def modif_biblio(biblio_id):
    status, donnees = Biblio.modif_biblio(
        id=biblio_id,
        titre=request.args.get("titre", None),
        auteur=request.args.get("auteur", None),
        date=request.args.get("date", None),
        lieu=request.args.get("lieu", None),
        typep=request.args.get("typep", None),
    )

    if status is True :
        flash("Merci pour votre contribution !", "success")
        unique_biblio = Biblio.query.get(biblio_id)
        return redirect("/") #vers le lieu qu'il vient de créer.

    else:
        flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
        unique_biblio = Biblio.query.get(biblio_id)
        return render_template("pages/modif_biblio.html", biblio=unique_biblio)

@app.route("/index_lieux")
def index_lieux():
    """ Route permettant la recherche plein-texte
    """
    # On préfèrera l'utilisation de .get() ici
    #   qui nous permet d'éviter un if long (if "clef" in dictionnaire and dictonnaire["clef"])
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    resultats = Place.query.paginate(page=page, per_page=LIEUX_PAR_PAGE)

    return render_template(
        "pages/index_lieux.html",
        resultats=resultats
    )

@app.route("/creer_liaison", methods=["POST", "GET"])
def creer_liaison():
    if request.method == "POST":
        statut, donnees = Relation.creer_liaison(
            biblio_id=request.form.get("biblio_id", None),
            place_id=request.form.get("place_id", None)
        )
        if statut is True:
            flash("Enregistrement effectué. Vous avez ajouté une nouvelle relation", "success")
            return redirect("/")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/liaison.html")
    else:
        return render_template("pages/liaison.html")

@app.route("/creer_liaison_correcte", methods=["POST", "GET"])
def creer_liaison_correcte():

    lieu = Place.query.get(place_id)
    titres = lieu.relations
    if request.method == "POST":
        statut, donnees = Relation.creer_liaison_correcte(
            place_id=place_id,
            biblio_id=biblio_id,
        #    biblio_titre=request.form.get("biblio_titre", None),
        )
        if statut is True:
            flash("Enregistrement effectué. Vous avez ajouté une nouvelle relation", "success")
            return redirect("/")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/index_biblio.html")
    else:
        return render_template("pages/index_biblio.html")

@app.route("/index_biblio/<int:place_id>")
def index_biblio(place_id):
    """ Route permettant la recherche plein-texte
    """
    # On préfèrera l'utilisation de .get() ici
    #   qui nous permet d'éviter un if long (if "clef" in dictionnaire and dictonnaire["clef"])
    unique_lieu = Place.query.get(place_id)
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    resultats = Biblio.query.paginate(page=page, per_page=LIEUX_PAR_PAGE)

    return render_template(
        "pages/index_biblio.html", lieu=unique_lieu,
        resultats=resultats
    )


"""
#place_id == Relation.query.get(relation_place_id)
#reference = Place.query.get(relations).all() : impossible de faire comme ça
#puisqu'a priori, le lieu n'a pas de relation
#titres = Biblio.query.get(biblio_titre).all()
#biblio_id == Relation.relation_biblio_id

status, donnees = Relation.creer_liaison_correcte(
    place_id=place_id,
    biblio_id=biblio_id,
    #biblio_titre=request.args.get("titre", None),
)

if status is True :
    #flash("Merci pour votre contribution !", "success")
#Ai-je besoin de récupérer l'ID du lieu  ? Oui, si je considère qu'il s'agit d'une modification du lieu
#que de modifier sa référence. En ce cas, deux types de modifications :
#-la modification du lieu
#-la modification de ses relations
    unique_lieu = Place.query.get(place_id)
    return redirect("/index_biblio.html", lieu=unique_lieu) #vers le lieu qu'il vient de créer.

else:
    flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
    unique_lieu = Place.query.get(place_id)
    return render_template("pages/creer_liaison_correcte.html", lieu=unique_lieu)

@app.route("/creer_lien/<int:place_id>", methods=["POST", "GET"])
def creer_lien(place_id):
    if request.method == "POST":
        statut, donnees = Relation.creer_liaison(
            biblio_titre=request.form.get("titre", None),
            place_nom=request.form.get("nom", None)
        )
        if statut is True:
            flash("Enregistrement effectué. Vous avez ajouté une nouvelle relation", "success")
            return redirect("/")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/liaison.html")
    else:
        return render_template("pages/liaison.html")

@app.route("/liaison/<int:biblio_id>/<int:place_id>")
def liaison(biblio_id, place_id):
    """""" Route permettant de lier une bibliographie à un lieu
    :param place_id: Identifiant numérique du lieu
    :param biblio_id: Identifiant numérique de la référence bibliographique
    """"""
    #endroit_1 = Place.liaison(place_id=place_id,
    #biblio_id=relations.biblio.biblio_id)
    #x = Place.query.get(place_id)
    #x = (x, (Biblio.liaison(biblio_id=biblio_id)))
    bibliographie = Relation.liaison(biblio_id=biblio_id,
    place_id=place_id)

    print(bibliographie)


    return render_template("pages/liaison.html", nom="Gazetteer", bibliographie=bibliographie)"""

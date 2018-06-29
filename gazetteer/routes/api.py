from flask import render_template, request, url_for, jsonify, json
from urllib.parse import urlencode

from ..app import app
from ..constantes import LIEUX_PAR_PAGE, API_ROUTE
from ..modeles.donnees import Place, Biblio, Relation, Authorship
from ..modeles.utilisateurs import User


#Classe pour encoder les sets en listes (pour la TypeError "JSON is not serializable")
class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

def Json_404():
    response = jsonify({"erreur": "Unable to perform the query"})
    response.status_code = 404
    return response


@app.route(API_ROUTE+"/places/<int:place_id>")
def api_places_single(place_id):
    """
    Route permettant l'affichage des données d'un lieu
    et, le cas échéant, des données bibliographiques qui lui sont liées
    
    :param id: identifiant numérique du lieu
    :return: dictionnaire data
    """
    lieu = Place.query.get(place_id)
    if not lieu:
        return Json_404
    if lieu.relations:
        return jsonify(lieu.to_jsonapi_2_dict())
    else:
        return jsonify(lieu.to_jsonapi_dict())

@app.route(API_ROUTE+"/biblios/<biblio_id>")
def api_biblios_single(biblio_id):
    """
    Route permettant l'affichage des données d'une référence bibliographique
    et, le cas échéant, des lieux qui lui sont associés

    :param id: identifiant numérique de la donnée bibliographique
    :return: dictionnaire data
    """
    biblio = Biblio.query.get(biblio_id)
    if not biblio:
        return Json_404
    if biblio.relations:
        return jsonify(biblio.to_jsonapi_2_dict())
    else:
        return jsonify(biblio.to_jsonapi_dict())


@app.route(API_ROUTE+"/places")
def api_places_browse():
    """ Route permettant la recherche plein-texte parmi les lieux

    On s'inspirera de http://jsonapi.org/ faute de pouvoir trouver le
    temps d'y coller à 100%
    """
    # q est très souvent utilisé pour indiquer une capacité de recherche
    motclef = request.args.get("q", None)
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    if motclef:
        query = Place.query.filter(
            Place.place_nom.like("%{}%".format(motclef))
        )
    else:
        query = Place.query

    try:
        resultats = query.paginate(page=page, per_page=LIEUX_PAR_PAGE)
    except Exception:
        return Json_404()

    dict_resultats = {
        "links": {
            "self": request.url
        },
        "data": [
            place.to_jsonapi_dict_2()
            for place in resultats.items
        ]
    }

    if resultats.has_next:
        arguments = {
            "page": resultats.next_num
        }
        if motclef:
            arguments["q"] = motclef
        dict_resultats["links"]["next"] = url_for("api_places_browse", _external=True)+"?"+urlencode(arguments)

    if resultats.has_prev:
        arguments = {
            "page": resultats.prev_num
        }
        if motclef:
            arguments["q"] = motclef
        dict_resultats["links"]["prev"] = url_for("api_places_browse", _external=True)+"?"+urlencode(arguments)

    response = jsonify(dict_resultats)
    return response

@app.route(API_ROUTE+"/biblios")
def api_biblios_browse():
    """ Route permettant la recherche plein-texte parmi les données
    bibliographiques
    On s'inspire de http://jsonapi.org/ faute de pouvoir trouver le
    temps d'y coller à 100%
    """
    # q est très souvent utilisé pour indiquer une capacité de recherche
    motclef = request.args.get("q", None)
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    if motclef:
        query = Biblio.query.filter(
            Biblio.biblio_titre.like("%{}%".format(motclef))
        )
    else:
        query = Biblio.query

    try:
        resultats = query.paginate(page=page, per_page=LIEUX_PAR_PAGE)
    except Exception:
        return Json_404()

    dict_resultats = {
        "links": {
            "self": request.url
        },
        "data": [
            biblio.to_jsonapi_dict_2()
            for biblio in resultats.items
        ]
    }

    if resultats.has_next:
        arguments = {
            "page": resultats.next_num
        }
        if motclef:
            arguments["q"] = motclef
        dict_resultats["links"]["next"] = url_for("api_biblios_browse", _external=True)+"?"+urlencode(arguments)

    if resultats.has_prev:
        arguments = {
            "page": resultats.prev_num
        }
        if motclef:
            arguments["q"] = motclef
        dict_resultats["links"]["prev"] = url_for("api_biblios_browse", _external=True)+"?"+urlencode(arguments)

    response = jsonify(dict_resultats)
    return response

@app.route(API_ROUTE+"/places/searchproximity")
def api_places_browse_proximity():

        #On s'inspire du code pour la recherche en plein texte.
        #loc lieu à partir duquel l'utilisateur souhaite faire sa recherche: il a une latitude et une longitude
        #radius: le rayon de recherche de l'utilisateur

        #il faut ajouter la capacité pour l'utilisateur de donner le radius et de préciser la latitude et la longitude qu'il veut voir appliquerself.
        #seulement je ne vois pas comment faire cette demande dans le cadre de l'API.

    loc_latitude = request.args.get("x", None)
    loc_longitude = request.args.get("y", None)
    radius = request.args.get("q", None)
    page = request.args.get("page", 1)
#on conserve la partie sur les gestions des pages afin de gérer l'affiche des résultats (enfin je crois...)
    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1
# si les infos nécessaires pour faire le query sur la DB sont manquantes, le code renvoie toutes les places.
    if not loc_latitude:
        query = Place.query

    if not loc_longitude:
        query = Place.query

    if not radius:
        query = Place.query

    if loc_latitude and loc_longitude and radius:
        pointofsearch = Place.query.filter(func.acos(func.sin(func.radians(loc_latitude)) * func.sin(func.radians(Place.place_latitude)) + func.cos(func.radians(loc_latitude)) * func.cos(func.radians(Place.place_latitude)) * func.cos(func.radians(Place.place_longitude) - (func.radians(loc_longitude)))) * 6371 <= radius).order_by(Place.place_nom.desc(), Place.place_nom.desc()).all()

#ce bout de code est conservé de la fonction si dessus par défaut.
    try:
        resultats = pointofsearch.paginate(page=page, per_page=LIEUX_PAR_PAGE)
    except Exception:
        return Json_404()

#difficulté de visualisation de l'organisation des données récupérées par le pointofsearch. Tentative d'adaptation de la réponse du code pour la recherche plein texte.
    dict_resultats = {
        "links": {
            "self": request.url
        },
        "data": [
            place.to_jsonapi_dict()
            for place in resultats.items
        ]
    }
#je ne suis pas certaine que l'on puisse mettre plusieurs varibables dans le if de gestions des pages de résultats....
    if resultats.has_next:
        arguments = {
            "page": resultats.next_num
        }
        if loc_latitude and loc_longitude and radius:
            arguments["x"] = loc_latitude
            arguments["y"] = loc_longitude
            arguments["q"] = radius
        dict_resultats["links"]["next"] = url_for("api_places_browse_proximity", _external=True)+"?"+urlencode(arguments)

    if resultats.has_prev:
        arguments = {
            "page": resultats.prev_num
        }
        if loc_latitude and loc_longitude and radius:
            arguments["x"] = loc_latitude
            arguments["y"] = loc_longitude
            arguments["q"] = radius
        dict_resultats["links"]["prev"] = url_for("api_places_browse_proximity", _external=True)+"?"+urlencode(arguments)

    response = jsonify(dict_resultats)
    return response

@app.route(API_ROUTE+"/places/searcharea")
def api_places_browse_area():
    # on tente d'ajouter une fonctionalité de recherche par zone avec 4 coordonnées soit 2 latitudes et 2 longitudes chacun représentant un minimum et un maximum...puisqu'il s'agit de lignes.
#On peut supposer qu'en ayant une latitude min et max, et une longitude min et max, on peut tenter d'écrire un query pour identifier les lieux dont les coordonnées sont compris entre ces 4 points.
    latitude_nord = request.args.get("w", None)
    latitude_sud = request.args.get("x", None)
    longitude_ouest = request.args.get("y", None)
    longitude_est = request.args.get("z", None)
    page = request.args.get("page", 1)

#on conserve la partie sur les gestions des pages afin de gérer l'affiche des résultats (enfin je crois...)
    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1
# si les infos nécessaires pour faire le query sur la DB sont manquantes, le code renvoie toutes les places.
    if not latitude_nord:
        query = Place.query

    if not latitude_sud:
        query = Place.query

    if not longitude_est:
        query = Place.query

    if not longitude_ouest:
        query = Place.query

    if latitude_nord and latitude_sud and longitude_est and longitude_ouest:
        areaofsearch= Place.query.filter(db.and_(
        Place.place_latitude.between(latitude_nord, latitude_sud),
        Place.place_longitude.between(longitude_est, longitude_ouest),
        )).order_by(Place.place_nom.desc(), Place.place_nom.desc()).all()

    try:
        resultats = areaofsearch.paginate(page=page, per_page=LIEUX_PAR_PAGE)
    except Exception:
        return Json_404()

#on reprend la même structure pour cette portion de code que pour la fonction par rayon.
    dict_resultats = {
        "links": {
            "self": request.url
        },
        "data": [
            place.to_jsonapi_dict()
            for place in resultats.items
        ]
    }

    if resultats.has_next:
        arguments = {
            "page": resultats.next_num
        }
        if latitude_nord and latitude_sud and longitude_est and longitude_ouest:
            arguments["w"] = latitude_nord
            arguments["x"] = latitude_sud
            arguments["y"] = longitude_ouest
            arguments["z"] = longitude_est
        dict_resultats["links"]["next"] = url_for("api_places_browse_area", _external=True)+"?"+urlencode(arguments)

    if resultats.has_prev:
        arguments = {
            "page": resultats.prev_num
        }
        if latitude_nord and latitude_sud and longitude_est and longitude_ouest:
            arguments["w"] = latitude_nord
            arguments["x"] = latitude_sud
            arguments["y"] = longitude_ouest
            arguments["z"] = longitude_est
        dict_resultats["links"]["prev"] = url_for("api_places_browse_area", _external=True)+"?"+urlencode(arguments)

    response = jsonify(dict_resultats)
    return response

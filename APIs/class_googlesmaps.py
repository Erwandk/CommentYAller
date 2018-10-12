__author__ = 'eke, gab, axel'
from APIs.class_api import API
import requests

# A partir d'un itineraire avec un summary et des steps, cette fonction renvoie la liste des steps


def steps_no_transit(itineraire):
    # non_transit
    itineraire = itineraire["steps"]
    nb_etape = len(itineraire)
    etapes = []
    for k in range(nb_etape):
        distance = itineraire[k]["distance"]["value"]
        duration = itineraire[k]["duration"]["value"]
        s_coord = itineraire[k]["start_location"]
        e_coord = itineraire[k]["end_location"]
        travel_mode = itineraire[k]["travel_mode"]
        transit_details = "No transit"
        etapes.append((distance, duration, s_coord, e_coord, travel_mode, transit_details))
    return etapes


def steps_transit(itineraire):
    distance = itineraire["distance"]["value"]
    duration = itineraire["duration"]["value"]
    s_coord = itineraire["start_location"]
    e_coord = itineraire["end_location"]
    travel_mode = itineraire["travel_mode"]
    departure_stop = itineraire["transit_details"]["departure_stop"]["name"]
    arrival_stop = itineraire["transit_details"]["arrival_stop"]["name"]
    vehicle = itineraire["transit_details"]["line"]["vehicle"]["type"]
    short = itineraire["transit_details"]["line"]["short_name"]
    nb_stations = itineraire["transit_details"]["num_stops"]
    s = (distance, duration, s_coord, e_coord, travel_mode, (departure_stop, arrival_stop, vehicle, short, nb_stations))
    return s


def steps(itineraire):
    # l'étape en transit
    itineraire = itineraire["steps"]
    nb_etape = len(itineraire)
    etapes = []
    cpt = 0
    for k in range(nb_etape):
        if itineraire[k]["travel_mode"] != "TRANSIT":
            for y in steps_no_transit(itineraire[k]):
                cpt += 1
                etapes.append([cpt, y])
        elif itineraire[k]["travel_mode"] == "TRANSIT":
            cpt += 1
            etapes.append([cpt, steps_transit(itineraire[k])])
    return etapes


def summary(itineraire):
    start_address = itineraire["start_address"]
    end_address = itineraire["end_address"]
    duration = itineraire["duration"]["text"]
    distance = itineraire["distance"]["text"]
    su = "Pour aller de {} au {} cela prendra {} et {}".format(start_address, end_address, duration, distance)
    return su


class GoogleMaps(API):
    """
        Class GoogleMaps héritant de la classe mère API
        paramètres de classes :
        - user_id : correspond à l'id du user permettant de se connecter à l'API
        """
    def __init__(self, user_id=9):
        API.__init__(self, nom="googlemaps", url="https://maps.googleapis.com/maps/api/directions/", user_id=user_id)

    def get_json(self, startcoord, endcoord, driving_mode="", transit_mode="", waypoints=""):
        """
                        Methode permettant de récupérer le travel_time de l'API de citymapper
                        :param startcoord : coordonnées GPS de la position de départ
                        :param endcoord : coordonnées GPS de la position d'arrivée
                        :param driving_mode : Quel mode de transport, WALKING, DRIVING, TRANSIT etc...
                        :param transit_mode: Quel type de transit en cas de driving_mode = "TRANSIT"
                        :param waypoints: Ajoute des endroits par lesquels l'itinéraire doit passer ##Format coordonnée
                        :return: Le json sur lequel on va travailler
                        """
        __path = "json?origin={}&destination={}".format(startcoord, endcoord)
        __path_additional = ""
        if driving_mode != "":
            __path_additional += "&mode={}".format(driving_mode)
        if transit_mode != "":
            __path_additional += "&transit_mode=".format(transit_mode)
        if waypoints != "":
            __path_additional += "&waypoints=".format(waypoints)
        __new_url = self.url + __path + __path_additional + "&key=" + str(self.key)

        resp = requests.get(__new_url)

        if resp.status_code != 200:
            raise NotImplementedError("Erreur {} : vous n'avez pas réussi à vous connecter à "
                                      "l'url {}.".format(resp.status_code, __new_url))
        json_data = {}
        try:
            json_data = resp.json()
        except Exception as e:
            print("Les données reçues ne sont pas reçues par la méthode json()")
            print(str(e))
        return json_data

    def get_etape_without_transit(self, startcoord, endcoord, driving_mode="", waypoints=""):
        """
                Methode permettant de récupérer le travel_time de l'API de citymapper
                :param startcoord : coordonnées GPS de la position de départ
                :param endcoord : coordonnées GPS de la position d'arrivée
                :param driving_mode : Quel mode de transport, WALKING, DRIVING, TRANSIT etc...
                :param waypoints: Ajoute des endroits par lesquels l'itinéraire doit passer ##Format coordonnée
                :return: Une liste d'étape qui contient plusieurs paramètres
                """

        assert driving_mode != "transit"

        etapes_description_itineraires = self.get_json(startcoord, endcoord, driving_mode, waypoints)
        etapes_description_itineraires = etapes_description_itineraires["routes"][0]["legs"][0]
        # On met le [0] car liste contenant un seul élément pour l'instant,
        # Plus le cas si on utlise plusieurs itinéraires ou waypoints

        return steps_no_transit(etapes_description_itineraires)

    def get_etape_with_transit(self, startcoord, endcoord, driving_mode="transit", transit_mode="", waypoints=""):
        """
                        Methode permettant de récupérer le travel_time de l'API de citymapper
                        :param startcoord : coordonnées GPS de la position de départ
                        :param endcoord : coordonnées GPS de la position d'arrivée
                        :param driving_mode : Quel mode de transport, WALKING, DRIVING, TRANSIT etc...
                        :param transit_mode: Quel type de transit en cas de driving_mode = "TRANSIT"
                        :param waypoints: Ajoute des endroits par lesquels l'itinéraire doit passer ##Format coordonnée
                        :return: Une liste d'étape qui contient plusieurs paramètres
                        """

        assert driving_mode == "transit"
        etapes_description_itineraires = self.get_json(startcoord, endcoord, driving_mode, transit_mode, waypoints)
        etapes_description_itineraires = etapes_description_itineraires["routes"][0]["legs"][0]
        return steps(etapes_description_itineraires)


if __name__ == '__main__':

    identifiant = 0

    API_GoogleMaps = GoogleMaps(identifiant)

    coord_depart = "48.8341102%2C2.2962797000000137"
    coord_fin = "48.8488043%2C2.288609500000007"

    # requete = API_GoogleMaps.get_etape_without_transit(startcoord=startcoord, endcoord=endcoord,
    # driving_mode= "walking")
    requete = API_GoogleMaps.get_etape_with_transit(startcoord=coord_depart, endcoord=coord_fin,
                                                    driving_mode="transit", transit_mode="bus")

    for x in requete:
        print(x)

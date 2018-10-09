__author__ = 'eke, gab, axel'
from APIs.class_api import API
import requests

class GoogleMaps(API):
    """
        Class GoogleMaps héritant de la classe mère API
        paramètres de classes :
        - user_id : correspond à l'id du user permettant de se connecter à l'API
        """
    def __init__(self,user_id=9):
        API.__init__(self,nom = "googlemaps", url = "https://maps.googleapis.com/maps/api/directions/",user_id = user_id)

    def get_etape(self,startcoord,endcoord,driving_mode="",transit_mode="",waypoints=""):
        """
                Methode permettant de récupérer le travel_time de l'API de citymapper
                :param startcoord : coordonnées GPS de la position de départ
                :param endcoord : coordonnées GPS de la position d'arrivée
                :param driving_mode : Quel mode de transport, WALKING, DRIVING, TRANSIT etc...
                :param transit_mode: Quel type de transit en cas de driving_mode = "TRANSIT"
                :param waypoints: Ajoute des endroits par lesquels l'itinéraire doit passer ##Format coordonnée
                :return: Une liste d'étape qui contient plusieurs paramètres
                """

        __path = "json?origin={}&destination={}".format(startcoord,endcoord)
        __path_additional =""
        if driving_mode !="":
            __path_additional +="&mode={}".format(driving_mode)
        if transit_mode !="":
            __path_additional+="&transit_mode=".format(transit_mode)
        if waypoints != "":
            __path_additional+="&waypoints=".format(waypoints)
        __new_url = self.url + __path +__path_additional + "&key=" + str(self.key)

        resp = requests.get(__new_url)

        if resp.status_code != 200:
            raise NotImplementedError("Erreur {} : vous n'avez pas réussi à vous connecter à "
                                      "l'url {}.".format(resp.status_code, __new_url))
        print(__new_url)
        json_data = {}
        try:
            json_data = resp.json()
        except Exception as e:
            print("Les données reçues ne sont pas reçues par la méthode json()")
            print(str(e))

        etapes_description = json_data["routes"][0]["legs"][0]["steps"]
        # On met le [0] car liste contenant un seul élément pour l'instant, plus le cas si on utlise plusieurs itinéraires ou waypoints
        nb_etape = len(etapes_description)
        etapes =[]
        for k in range(nb_etape):
                distance = etapes_description[k]["distance"]["value"]
                duration = etapes_description[k]["duration"]["value"]
                s_coord = etapes_description[k]["start_location"]
                e_coord = etapes_description[k]["end_location"]
                travel_mode = etapes_description[k]["travel_mode"]
                etapes.append([distance, duration, s_coord,e_coord,travel_mode])
        return etapes

if __name__ == '__main__':

    user_id = 0

    API_GoogleMaps = GoogleMaps(user_id)

    startcoord = "48.8341102%2C2.2962797000000137"
    endcoord = "48.8488043%2C2.288609500000007"

    json_data = API_GoogleMaps.get_etape(startcoord=startcoord, endcoord=endcoord, driving_mode= "walking")

    for x in json_data:
        print(x)
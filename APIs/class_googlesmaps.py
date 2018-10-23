__author__ = 'eke, gab, axel'
from APIs.class_api import API
import requests


class GoogleMaps(API):
    """
    Class GoogleMaps héritant de la classe mère API
    paramètres de classes :
    - user_id : correspond à l'id du user permettant de se connecter à l'API
    - startcoord : coordonnées du point de départ (GPS ou adresse)
    - endcoord : coordonnées du point d'arrivée (GPS ou adresse)
    - driving_mode : mode de déplacement (walking, driving...)
    - transit_mode :
    - waypoints :
    """

    def __init__(self,  startcoord, endcoord, driving_mode, transit_mode, waypoints, user_id=9):
        API.__init__(self, nom="googlemaps", url="https://maps.googleapis.com/maps/api/directions/", user_id=user_id)
        self.__startcoord = startcoord
        self.__endcoord = endcoord
        self._driving_mode = driving_mode
        self.__transit_mode = transit_mode
        self.__waypoints = waypoints
        self._json = dict()

    def get_json(self):
        __path = "json?origin={}&destination={}".format(self.__startcoord, self.__endcoord)
        __path_additional = ""
        if self._driving_mode != "":
            __path_additional += "&mode={}".format(self._driving_mode)
        if (self.__transit_mode != "") & (self._driving_mode == "transit"):
            __path_additional += "&transit_mode={}".format(self.__transit_mode)
        if self.__waypoints != "":
            __path_additional += "&waypoints={}".format(self.__waypoints)
        __new_url = self.url + __path + __path_additional + "&key=" + str(self.key)
        resp = requests.get(__new_url)
        if resp.status_code != 200:
            raise NotImplementedError("Erreur {} : vous n'avez pas réussi à vous connecter à "
                                      "l'url {}.".format(resp.status_code, __new_url))
        __json_data = {}

        try:
            __json_data = resp.json()
        except Exception as e:
            print("Les données reçues ne sont pas reçues par la méthode json()")
            print(str(e))
        self._json = __json_data

    @staticmethod
    def get_etapes(itineraire):
        itineraire = itineraire["steps"]
        nb_etape = len(itineraire)
        etapes = []
        for k in range(nb_etape):
            __distance = itineraire[k]["distance"]["value"]
            __duration = itineraire[k]["duration"]["value"]
            __s_coord = itineraire[k]["start_location"]
            __e_coord = itineraire[k]["end_location"]
            __travel_mode = itineraire[k]["travel_mode"]
            __transit_details = "No transit"
            etapes.append((__distance, __duration, __s_coord, __e_coord, __travel_mode, __transit_details))
        return etapes

    def get_etape(self):
        self.get_json()
        assert self._driving_mode != "transit"
        __itineraire = self._json["routes"][0]["legs"][0]
        return GoogleMaps.get_etapes(__itineraire)

    @property
    def json(self):
        return self._json

    @json.setter
    def json(self, valeur):
        print('You cant touch it and replace the valeur with {}'.format(valeur))

    @property
    def startcoord(self):
        return self.startcoord

    @startcoord.setter
    def startcoord(self, valeur):
        print('You cant touch it and replace the valeur with {}'.format(valeur))

    @property
    def endcoord(self):
        return self.endcoord

    @endcoord.setter
    def endcoord(self, valeur):
        print('You cant touch it and replace the valeur with {}'.format(valeur))

    @property
    def transit_mode(self):
        return self.transit_mode

    @transit_mode.setter
    def transit_mode(self, valeur):
        print('You cant touch it and replace the valeur with {}'.format(valeur))

    @property
    def driving_mode(self):
        return self.driving_mode

    @driving_mode.setter
    def driving_mode(self, valeur):
        print('You cant touch it and replace the valeur with {}'.format(valeur))

    @property
    def waypoints(self):
        return self.waypoints

    @waypoints.setter
    def waypoints(self, valeur):
        print('You cant touch it and replace the valeur with {}'.format(valeur))


"""class GoogleMapsWaypoints(GoogleMaps):
    def __init__(self, __json):
        GoogleMaps.__init__(self)
        self.__waypoints = GoogleMaps.transit_mode"""


class GoogleMapsTransit(GoogleMaps):

    def __init__(self, startcoord, endcoord, driving_mode, transit_mode, waypoints, user_id):
        GoogleMaps.__init__(self, startcoord=startcoord, endcoord=endcoord, driving_mode=driving_mode,
                            transit_mode=transit_mode, waypoints=waypoints, user_id=user_id)

    @staticmethod
    def get_with_transit(itineraire):
        __distance = itineraire["distance"]["value"]
        __duration = itineraire["duration"]["value"]
        __s_coord = itineraire["start_location"]
        __e_coord = itineraire["end_location"]
        __travel_mode = itineraire["travel_mode"]
        __departure_stop = itineraire["transit_details"]["departure_stop"]["name"]
        __arrival_stop = itineraire["transit_details"]["arrival_stop"]["name"]
        __vehicle = itineraire["transit_details"]["line"]["vehicle"]["type"]
        __short = itineraire["transit_details"]["line"]["short_name"]
        __nb_stations = itineraire["transit_details"]["num_stops"]
        __s = (__distance, __duration, __s_coord, __e_coord, __travel_mode,
               (__departure_stop, __arrival_stop, __vehicle, __short, __nb_stations))
        return __s

    def get_etape(self):
        self.get_json()
        assert self._driving_mode == "transit"
        __itineraire = self._json["routes"][0]["legs"][0]["steps"]
        __nb_etape = len(__itineraire)
        __etape = []
        for k in range(__nb_etape):
            if __itineraire[k]["travel_mode"] != "TRANSIT":
                for j in GoogleMaps.get_etapes(__itineraire[k]):
                    __etape.append(j)
            elif __itineraire[k]["travel_mode"] == "TRANSIT":
                __etape.append(GoogleMapsTransit.get_with_transit(__itineraire[k]))
        return __etape


"""class GoogleMapsWaypointsTransit(GoogleMapsWaypoints,GoogleMapsTransit):
    def __init__(self, __json):
        GoogleMapsWaypoints.__init__(self)
        GoogleMapsTransit.__init__(self)"""


if __name__ == '__main__':

    identifiant = 0
    coord_depart = "8+rue+des+morillons+Paris"
    coord_fin = "6+rue+des+marronniers+Paris"
    driving_mode_front = "bicycling"
    transit_mode_front = ""
    waypoints_front = ""

    if driving_mode_front == "transit":
        requete = GoogleMapsTransit(user_id=identifiant, startcoord=coord_depart, endcoord=coord_fin,
                                    driving_mode=driving_mode_front, transit_mode=transit_mode_front,
                                    waypoints=waypoints_front)
    else:
        requete = GoogleMaps(user_id=identifiant, startcoord=coord_depart, endcoord=coord_fin,
                             driving_mode=driving_mode_front, transit_mode=transit_mode_front,
                             waypoints=waypoints_front)

    requete = requete.get_etape()
    for x in requete:
        print(x)

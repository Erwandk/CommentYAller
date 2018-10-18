__author__ = 'eke, gab, axel'
from APIs.class_api import API
import requests


class GoogleMaps(API):
    """
        Class GoogleMaps héritant de la classe mère API
        paramètres de classes :
        - user_id : correspond à l'id du user permettant de se connecter à l'API
        -
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
            distance = itineraire[k]["distance"]["value"]
            duration = itineraire[k]["duration"]["value"]
            s_coord = itineraire[k]["start_location"]
            e_coord = itineraire[k]["end_location"]
            travel_mode = itineraire[k]["travel_mode"]
            transit_details = "No transit"
            etapes.append((distance, duration, s_coord, e_coord, travel_mode, transit_details))
        return etapes

    def get_etape(self):
        assert self._driving_mode != "transit"
        itineraire = self._json["routes"][0]["legs"][0]
        return GoogleMaps.get_etapes(itineraire[:])

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
        s = (distance, duration, s_coord, e_coord, travel_mode,
             (departure_stop, arrival_stop, vehicle, short, nb_stations))
        return s

    def get_etape(self):

        assert self._driving_mode == "transit"
        itineraire = self._json["routes"][0]["legs"][0]["steps"]
        nb_etape = len(itineraire)
        etape = []
        for k in range(nb_etape):
            if itineraire[k]["travel_mode"] != "TRANSIT":
                for j in GoogleMaps.get_etapes(itineraire[k]):
                    etape.append(j)
            elif itineraire[k]["travel_mode"] == "TRANSIT":
                etape.append(GoogleMapsTransit.get_with_transit(itineraire[k]))
            print(k, etape)
        return etape


"""class GoogleMapsWaypointsTransit(GoogleMapsWaypoints,GoogleMapsTransit):
    def __init__(self, __json):
        GoogleMapsWaypoints.__init__(self)
        GoogleMapsTransit.__init__(self)"""


if __name__ == '__main__':

    identifiant = 0
    coord_depart = "8+rue+des+morillons+Paris"
    coord_fin = "6+rue+des+marronniers+Paris"
    driving_mode_front = "transit"
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

    requete.get_json()

    requete = requete.get_etape()
    for x in requete:
        print(x)
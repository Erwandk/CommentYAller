#!usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'eke, gab, axel'

from APIs.class_api import API
import requests


class GoogleMaps(API):
    """
    Class GoogleMaps héritant de la classe mère API
    Paramétrée pour appeler l'API GoogleMaps pour récupérer les différents trajets
    paramètres de classes :
    - user_id : correspond à l'id du user permettant de se connecter à l'API
    - startcoord : coordonnées du point de départ (GPS ou adresse)
    - endcoord : coordonnées du point d'arrivée (GPS ou adresse)
    - driving_mode : mode de déplacement (walking, driving...)
    - transit_mode :
    - waypoints :
    """

    def __init__(self,  startcoord, endcoord, driving_mode, transit_mode, waypoints, user_id=9):
        API.__init__(self, api_name="googlemaps", url="https://maps.googleapis.com/maps/api/directions/",
                     user_id=user_id)
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
            print("Data cannot be parsed by json() method.")
            print(str(e))
        self._json = __json_data

    @staticmethod
    def get_etapes(itinary):
        itinary = itinary["steps"]
        nb_steps = len(itinary)
        steps = []
        for k in range(nb_steps):
            __distance = itinary[k]["distance"]["value"]
            __duration = itinary[k]["duration"]["value"]
            __s_coord = itinary[k]["start_location"]
            __e_coord = itinary[k]["end_location"]
            __travel_mode = itinary[k]["travel_mode"]
            __transit_details = "No transit"
            try:
                __instruction = itinary[k]["html_instructions"].replace("'", " ").encode('utf-8').decode('utf-8')
            except Exception:
                # for some steps there is no instructions
                __instruction = ""
            steps.append((__distance, __duration, __s_coord, __e_coord, __travel_mode, __transit_details, __instruction))
        return steps

    def get_etape(self):
        self.get_json()
        assert self._driving_mode != "transit"
        __itinary = self._json["routes"][0]["legs"][0]
        return GoogleMaps.get_etapes(__itinary)

    @property
    def json(self):
        return self._json

    @json.setter
    def json(self, value):
        raise AttributeError("Your are not allowed to modify json by {}".format(value))

    @property
    def startcoord(self):
        return self.startcoord

    @startcoord.setter
    def startcoord(self, value):
        raise AttributeError("Your are not allowed to modify startcoord by {}".format(value))

    @property
    def endcoord(self):
        return self.endcoord

    @endcoord.setter
    def endcoord(self, value):
        raise AttributeError("Your are not allowed to modify endcoord by {}".format(value))

    @property
    def transit_mode(self):
        return self.transit_mode

    @transit_mode.setter
    def transit_mode(self, value):
        raise AttributeError("Your are not allowed to modify transit_mode by {}".format(value))

    @property
    def driving_mode(self):
        return self.driving_mode

    @driving_mode.setter
    def driving_mode(self, value):
        raise AttributeError("Your are not allowed to modify driving_mode by {}".format(value))

    @property
    def waypoints(self):
        return self.waypoints

    @waypoints.setter
    def waypoints(self, value):
        raise AttributeError("Your are not allowed to modify waypoints by {}".format(value))


"""class GoogleMapsWaypoints(GoogleMaps):
    def __init__(self, __json):
        GoogleMaps.__init__(self)
        self.__waypoints = GoogleMaps.transit_mode"""


class GoogleMapsTransit(GoogleMaps):

    def __init__(self, startcoord, endcoord, driving_mode, transit_mode, waypoints, user_id):
        GoogleMaps.__init__(self, startcoord=startcoord, endcoord=endcoord, driving_mode=driving_mode,
                            transit_mode=transit_mode, waypoints=waypoints, user_id=user_id)

    @staticmethod
    def get_with_transit(itinary):
        __distance = itinary["distance"]["value"]
        __duration = itinary["duration"]["value"]
        __s_coord = itinary["start_location"]
        __e_coord = itinary["end_location"]
        __travel_mode = itinary["travel_mode"]
        __departure_stop = itinary["transit_details"]["departure_stop"]["name"]
        __arrival_stop = itinary["transit_details"]["arrival_stop"]["name"]
        __vehicle = itinary["transit_details"]["line"]["vehicle"]["type"]
        __short = itinary["transit_details"]["line"]["short_name"]
        __nb_stations = itinary["transit_details"]["num_stops"]
        __instruction = "Take the <b>{} line {}</b> from <b>{} to {}</b> for {} stations"\
            .format(__vehicle, __short, __departure_stop, __arrival_stop, __nb_stations) \
            .replace("'", " ")\
            .encode('utf-8')\
            .decode('utf-8')
        __s = (__distance, __duration, __s_coord, __e_coord, __travel_mode,
               (__departure_stop, __arrival_stop, __vehicle, __short, __nb_stations),__instruction)
        return __s

    def get_etape(self):
        self.get_json()
        assert self._driving_mode == "transit"
        __itinary = self._json["routes"][0]["legs"][0]["steps"]
        __nb_steps = len(__itinary)
        __steps = []
        for k in range(__nb_steps):
            if __itinary[k]["travel_mode"] != "TRANSIT":
                for j in GoogleMaps.get_etapes(__itinary[k]):
                    __steps.append(j)
            elif __itinary[k]["travel_mode"] == "TRANSIT":
                __steps.append(GoogleMapsTransit.get_with_transit(__itinary[k]))
        return __steps


"""class GoogleMapsWaypointsTransit(GoogleMapsWaypoints,GoogleMapsTransit):
    def __init__(self, __json):
        GoogleMapsWaypoints.__init__(self)
        GoogleMapsTransit.__init__(self)"""

if __name__ == '__main__':
    startcoord = "8+rue+des+morrillons+Paris"
    endcoord = "6+rue+des+marronniers+Paris"
    driving_mode = "walking"

    test = GoogleMaps(startcoord,endcoord,driving_mode,transit_mode="", waypoints="",user_id=2)
    for k in test.get_etape():
        print(k)


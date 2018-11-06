#!usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'eke, gab, axel'

# Importation de la classe mère API et des modules utilisés
from APIs.class_api import API
import requests


class GoogleMaps(API):
    """
    Class GoogleMaps héritant de la classe mère API
    Paramétrée pour appeler l'API GoogleMaps pour récupérer les différents trajets avec mode de transport sans transit
    """

    def __init__(self,  startcoord, endcoord, driving_mode, transit_mode, user_id=9):
        """
        :param startcoord: coordonnées du point de départ (GPS ou adresse) (str)
        :param endcoord: coordonnées du point d'arrivée (GPS ou adresse) (str)
        :param driving_mode: mode de déplacement (walking, driving...) (str)
        :param transit_mode: mode de transport en commun (str)
        :param user_id: id du user (int)
        """
        assert isinstance(startcoord, str) and isinstance(endcoord, str) and isinstance(driving_mode, str)
        assert isinstance(transit_mode, str) and isinstance(user_id, int)
        API.__init__(self, api_name="googlemaps", url="https://maps.googleapis.com/maps/api/directions/",
                     user_id=user_id)
        self.__startcoord = startcoord
        self.__endcoord = endcoord
        self._driving_mode = driving_mode
        self.__transit_mode = transit_mode
        self._json = dict()

    def get_json(self):
        """
        Permet d'obtenir le fichier json qui contient l'ensemble des informations GoogleMaps
        """

        __path = "json?origin={}&destination={}".format(self.__startcoord, self.__endcoord)
        __path_additional = ""
        if self._driving_mode != "":
            __path_additional += "&mode={}".format(self._driving_mode)
        if (self.__transit_mode != "") & (self._driving_mode == "transit"):
            __path_additional += "&transit_mode={}".format(self.__transit_mode)
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
        """
        Permet de calculer toutes les étapes pour un mode de transport unique.
        :param itinary: itinéraire du trajet
        :return: steps: une liste dont chaque éléments contient les informations de chacune des etapes
        """
        itinary = itinary["steps"]
        nb_steps = len(itinary)
        steps = []
        for i in range(nb_steps):
            __distance = itinary[i]["distance"]["value"]
            __duration = itinary[i]["duration"]["value"]
            __s_coord = itinary[i]["start_location"]
            __e_coord = itinary[i]["end_location"]
            __travel_mode = itinary[i]["travel_mode"]
            __transit_details = "No transit"
            if "html_instructions" in itinary[i]:
                __instruction = itinary[i]["html_instructions"].replace("'", " ").encode('utf-8').decode('utf-8')
            else:
                # for some steps there is no instructions
                __instruction = ""
            steps.append((__distance, __duration, __s_coord, __e_coord,
                          __travel_mode, __transit_details, __instruction))
        return steps

    def get_etape(self):
        """
        Permet d'obtenir les étapes pour un trajet avec un seul mode de transport.
        :return: liste d'étape du trajet
        """
        self.get_json()
        assert self._driving_mode != "transit"
        __itinary = self._json["routes"][0]["legs"][0]
        return GoogleMaps.get_etapes(__itinary)

    # Définition des getters et setters de la classe
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


class GoogleMapsTransit(GoogleMaps):
    """
        Class GoogleMapsTransit héritant de la classe GoogleMaps
        Paramétrée pour appeler l'API GoogleMaps pour récupérer les différents trajets avec transit
        paramètres de classes :
        - user_id : correspond à l'id du user permettant de se connecter à l'API
        - startcoord : coordonnées du point de départ (GPS ou adresse)
        - endcoord : coordonnées du point d'arrivée (GPS ou adresse)
        - driving_mode : mode de déplacement (walking, driving...)
        - transit_mode :
        """

    def __init__(self, startcoord, endcoord, driving_mode, transit_mode, user_id):
        GoogleMaps.__init__(self, startcoord=startcoord, endcoord=endcoord, driving_mode=driving_mode,
                            transit_mode=transit_mode, user_id=user_id)

    @staticmethod
    def get_with_transit(itinary):
        """
        Récuper les informations pour l'étape avec mode de transport TRANSIT au sein du trajet avec transit
        :param itinary:
        :return: les informations sous forme d'un tuple de l'étape TRANSIT
        """
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
        __dep_time_stop = itinary["transit_details"]["departure_time"]["value"]
        __arr_time_stop = itinary["transit_details"]["arrival_time"]["value"]
        __instruction = "Take the <b>{} line {}</b> from <b>{} to {}</b> for {} stations"\
            .format(__vehicle, __short, __departure_stop, __arrival_stop, __nb_stations) \
            .replace("'", " ")\
            .encode('utf-8')\
            .decode('utf-8')
        __s = (__distance, __duration, __s_coord, __e_coord, __travel_mode,
               (__departure_stop, __arrival_stop, __vehicle, __short, __nb_stations, __dep_time_stop, __arr_time_stop),
                __instruction)
        return __s

    def get_etape(self):
        """
        Permet d'obtenir les étapes pour un trajet avec mode de transport transit (transport en commun)
        :return: Liste de tuples d'information sur les étapes du trajet
        """
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


if __name__ == '__main__':
    import pprint

    def test_1():
        startcoord = '6+rue+des+marronniers+paris'
        endcoord = 'gare+de+l+est+paris'
        driving_mode = 'transit'
        transit_mode = ''
        user_id = 2
        test = GoogleMapsTransit(startcoord, endcoord, driving_mode, transit_mode, user_id)
        # test.get_etape()
        pprint.pprint(test.get_etape())

    test_1()

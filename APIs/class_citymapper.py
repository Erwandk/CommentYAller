#!usr/bin/env/python3
# -*- coding: utf-8 -*-

__author__ = 'eke, gab, axel'

from APIs.class_api import API
import requests


class CityMapper(API):
    """
    Class CityMapper héritant de la classe mère API
    paramètres de classes :
    - user_id : correspond à l'id du user permettant de se connecter à l'API
    """

    def __init__(self, user_id=9):
        API.__init__(self, url="https://developer.citymapper.com", nom="citymapper", user_id=user_id)

    def get_travel_time(self, startcoord, endcoord, time, time_type="arrival"):
        """
        Methode permettant de récupérer le travel_time de l'API de citymapper
        :param startcoord : coordonnées GPS de la position de départ
        :param endcoord : coordonnées GPS de la position d'arrivée
        :param time : heure de départ ou d'arrivée, selon le time_type
        :param time_type : type d'heure à considérer (départ, arrivée...)
        :return: une variable json contenant les données récupérées
        """

        __path = "/api/1/traveltime/?startcoord={}&endcoord={}&time={}&time_type={}".format(startcoord, endcoord,
                                                                                            time, time_type)
        __new_url = self.url + __path + "&key=" + str(self.key)

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


if __name__ == '__main__':

    user_id = 0

    API_citymapper = CityMapper(user_id)

    startcoord = "51.525246%2C0.084672"
    endcoord = "51.559098%2C0.074503"
    time = "2014-11-06T19%3A00%3A02-0500"
    time_type = "arrival"

    json_data = API_citymapper.get_travel_time(startcoord=startcoord, endcoord=endcoord, time=time, time_type=time_type)

    print(json_data)

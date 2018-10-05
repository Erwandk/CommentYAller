#!usr/bin/env/python3
# -*- coding: utf-8 -*-

__author__ = 'eke, gab, axel'

import user_api
import requests


class API:

    def __init__(self, url, nom=""):
        self._url = url
        self._nom = nom

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, valeur):
        print("A reflechir : donnez l'accès ou non à la modification de la valeur")
        self._url = valeur

    @property
    def nom(self):
        return self._nom

    @nom.setter
    def nom(self, valeur):
        print("A reflechir : donnez l'accès ou non à la modification de la valeur")
        self._nom = valeur

    def _get_key_by_id(self, user_id):

        key = ""
        if user_id not in (0, 1, 2):
            raise ValueError("Le user_id renseigné pour récupérer les clés n'est pas correct : {}".format(user_id))

        if self.nom == "googlemaps":
            if user_id not in dic_user_key_googlemaps:
                print("Le user_id {} n'est pas présent dans dic_user_key_googlemaps".format(user_id))
            key = dic_user_key_googlemaps[user_id]
        elif self.nom == "citymapper":
            if user_id not in dic_user_key_citymapper:
                print("Le user_id {} n'est pas présent dans dic_user_key_citymapper".format(user_id))
            key = dic_user_key_citymapper[user_d]
        else:
            print("Je ne trouve pas le nom de l'API")
        return key

    def get_infos(self, path, user_id = 9, *params):
        __new_url = self.url + path

        # TODO : correctly parse params to get method
        parse_params = params

        key = self._get_key_by_id(user_id)

        print(__new_url)
        resp = requests.get(__new_url)
        if resp.status_code != 200:
            raise NotImplementedError("Erreur {} : vous n'avez pas réussi à vous connecter à l'url {}.".format(resp.status_code, __new_url))
        json_data = {}
        try:
            json_data = resp.json()
        except Exception as e:
            print("Les données reçues ne sont pas reçues par la méthode json()")

        return json_data


if __name__ == '__main__':

    url = "https://developer.citymapper.com"

    CityMapper = API(url)

    startcoord = "51.525246%2C0.084672"
    endcoord = "51.559098%2C0.074503"
    time = "2014-11-06T19%3A00%3A02-0500"
    time_type = "arrival"
    user_id = 2
    key = dic_user_key_citymapper[user_id]

    path = "/api/1/traveltime/?startcoord={}&endcoord={}&time={}&time_type={}&key={}".format(startcoord, endcoord, time, time_type, key)

    data = CityMapper.get_infos(path)

    for item in data:
        print(item)
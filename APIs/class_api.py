#!usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'eke, gab, axel'

from user_api import *


class API:
    """
    Classe mère des autres classes APIs que nous allons créer durant le projet
    paramètres de classes :
    - url : correspond à l'url racine de l'api en questions
    - user_id : correspond a l'id du user pour recuperer la cle de l'API correspondante
    """

    def __init__(self, url, api_name="", user_id=0):
        self._url = url
        self.__api_name = api_name
        self._user_id = user_id
        self._key = self._get_key_by_id(self._user_id)

    def _get_key_by_id(self, user_id):
        """
         Methode permettant de récupérer la clé de chaque API en fonction du user_id et de son nom
        """

        __key = ""
        if user_id not in (0, 1, 2, 9):
            raise ValueError("user_id to retrieve keys is incorrect : {}".format(user_id))

        if self.__api_name == "googlemaps":
            if user_id not in dic_user_key_googlemaps:
                raise KeyError("user_id {} is not in dic_user_key_googlemaps".format(user_id))
            else:
                __key = dic_user_key_googlemaps[user_id]
        elif self.__api_name == "elevation":
            if user_id not in dic_user_key_googlemaps:
                raise KeyError("user_id {} is not in dic_user_key_googlemaps".format(user_id))
            else:
                __key = dic_user_key_googlemaps[user_id]
        elif self.__api_name == "citymapper":
            if user_id not in dic_user_key_citymapper:
                raise KeyError("user_id {} is not in dic_user_key_citymapper".format(user_id))
            else:
                __key = dic_user_key_citymapper[user_id]
        elif self.__api_name == "ipstack":
            if user_id not in dic_user_key_apistack:
                raise KeyError("user_id {} is not in dic_user_key_apistack".format(user_id))
            else:
                __key = dic_user_key_apistack[user_id]
        else:
            if self.__api_name not in ["meteo", "velib"]:
                raise NameError("I don't find name for API {} with user_id {}".format(self.__api_name, user_id))
        return __key

    # Défintion des getters et setters des attributs de la classe
    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        raise AttributeError("Your are not allowed to modify url by {}".format(value))

    @property
    def api_name(self):
        return self.__api_name

    @api_name.setter
    def api_name(self, value):
        raise AttributeError("Your are not allowed to modify api_name by {}".format(value))

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        if value not in [0, 1, 2, 9]:
            raise AttributeError("user_id should be equal to 0, 1, 2 or 9")
        else:
            self._user_id = value

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        raise AttributeError("Your are not allowed to modify key by {}".format(value))

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

    def __init__(self, url, nom="", user_id=0):
        self._url = url
        self.__nom = nom
        self._user_id = user_id
        self._key = self._get_key_by_id(self._user_id)

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, valeur):
        print("A reflechir : donnez l'accès ou non à la modification de l'url")
        self._url = valeur

    @property
    def nom(self):
        return self.__nom

    @nom.setter
    def nom(self, valeur):
        print("A reflechir : donnez l'accès ou non à la modification du nom")
        self.__nom = valeur

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, valeur):
        print("A reflechir : donnez l'accès ou non à la modification du user_id")
        self._user_id = valeur

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, valeur):
        print("A reflechir : donnez l'accès ou non à la modification de la clé")
        self._key = valeur

    def _get_key_by_id(self, user_id):
        """
         Methode permettant de récupérer la clé de chaque API en fonction du user_id et de son nom
        """

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
            key = dic_user_key_citymapper[user_id]
        else:
            print("Je ne trouve pas le nom de l'API pour l'user_id {}".format(user_id))
        return key

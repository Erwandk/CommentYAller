#!usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'eke, gab, axel'

from APIs.class_api import API
import socket
import requests
import json


class InfoUser(API):
    """
    Classe InfoUser hérite de la classe mère API, permet d'afficher les informations GPS de l'utilisateur
    paramètres de classes :
    - user_id : correspond à l'id du user permettant de se connecter à l'API
    """

    def __init__(self, user_id=0):
        API.__init__(self, url="http://api.ipstack.com/", api_name="ipstack", user_id=user_id)
        try:
            self.__ip = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][0]
        except Exception as e:
            print("Your computer doesn't seem to be connected to internet !")
            print(str(e))
            self.__ip = ""

        self.__continent = ""
        self.__country = ""
        self.__region = ""
        self.__city = ""
        self.__lat = 0
        self.__long = 0

        if self.__ip != "":
            self.__compute_param()

    def __compute_param(self):
        __new_url = self.url + self.__ip + "?access_key=" + self.key
        r = requests.get(__new_url)
        j = json.loads(r.text)
        self.__continent = j['continent_name']
        self.__country = j['country_name']
        self.__region = j['region_name']
        self.__city = j['city']
        self.__lat = j['latitude']
        self.__long = j['longitude']

    @property
    def ip(self):
        return self.__ip

    @ip.setter
    def ip(self, value):
        raise AttributeError("You are not allowed to modify ip by {}".format(value))

    @property
    def continent(self):
        return self.__continent

    @continent.setter
    def continent(self, value):
        raise AttributeError("You are not allowed to modify continent by {}".format(value))

    @property
    def country(self):
        return self.__country

    @country.setter
    def country(self, value):
        raise AttributeError("You are not allowed to modify country by {}".format(value))

    @property
    def region(self):
        return self.__region

    @region.setter
    def region(self, value):
        raise AttributeError("You are not allowed to modify region by {}".format(value))

    @property
    def city(self):
        return self.__city

    @city.setter
    def city(self, value):
        raise AttributeError("You are not allowed to modify city by {}".format(value))

    @property
    def lat(self):
        return self.__lat

    @lat.setter
    def lat(self, value):
        raise AttributeError("You are not allowed to modify lat by {}".format(value))

    @property
    def long(self):
        return self.__long

    @long.setter
    def long(self, value):
        raise AttributeError("You are not allowed to modify long by {}".format(value))

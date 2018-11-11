#!usr/bin/env/python3
# -*- coding: utf-8 -*-

__author__ = 'eke, gab, axel'

# Importation de la classe mère API et des modules utilisés
from APIs.class_api import API
import requests
import time
from threading import Thread


class Meteo(API, Thread):
    """
    Cette classe permet de se connecter à une API météo de récupérer des données pour la journée ou les jours à venir
    """

    def __init__(self):
        Thread.__init__(self)
        API.__init__(self,
                     url="http://www.infoclimat.fr/public-api/gfs/json?_ll=48.85341,2.3488&_auth=CBIAFwN9BiRRfFtsA3ULI"
                         "gBoBTBdK1dwA38CYVs%2BB3pWPVAxVDRTNVY4VyoFKlVjWXQFZl5lUmIBagZ%2BCHpXNghiAGwDaAZhUT5bPgMsCyAAL"
                         "gVkXX1XcANhAmZbPgd6VjRQPVQyUy9WO1cxBTdVf1loBWdeYFJ1AX0GYAhgVzcIYwBjA2MGZVE9WzADMgsgACwFYF0wV"
                         "z0DZwJnW2IHY1ZjUDdUMlMxVjtXZwUwVX9ZYwVkXmBSaAFrBmQIZ1c1CHQAewMZBhdRI1t5A3ELagB1BXhdN1cxAzQ%3"
                         "D&_c=cc703eb909f9f00058063c7c570f6a45",
                     api_name='meteo')
        self.__time = ''
        self.__data = dict()  # Json retourné par l'API
        self.__temperature = 0  # Température au sol en °C
        self.__rain = 0  # Nbr de mm de précipitation (sur un créneau de 3h)
        self.__convective_rain = 0  # Nbr de mm de précipitation convective (sur un créneau de 3h)
        self.__snow = ""  # 'oui' s'il y a un risque de neige, 'non' sinon

    def run(self):
        self.__set_time()  # affecte l'attribut self.__time
        self.__get_json()  # affecte l'attribut self.__data
        self.__temperature = round(self.__data['temperature']['sol']-273, 2)
        self.__rain = self.__data['pluie']
        self.__convective_rain = self.__data['pluie_convective']
        self.__snow = self.__data['risque_neige']

    def __set_time(self):
        """
        Méthode qui définit le créneau horaire à partir de l'heure courante, et affecte l'attribut self.__time
        """
        t = time.localtime()
        # Date
        _date = time.strftime('20%y-%m-%d', t)
        # Créneau horaire
        if t[3] == 0:  # Cas entre 00h00 et 00h59 -> aller sur le créneau 22h de la veille
            _date = time.strftime('20%y-%m-', t) + str(t[2]-1)
            _heure = '22:00:00'
        elif t[3] % 3 == 0 and t[3] != 0:  # Cas des heures suivantes : 3h, 6h, 9h, 12h, 15h, 18h, 21h
            if t[3]-2 < 10:  # Pour transformer 1h, 4h, et 7h en 01h, 04h et 07h
                _heure = '0' + str(t[3]-2) + ':00:00'
            else:
                _heure = str(t[3]-2) + ':00:00'
        elif t[3] % 3 == 1:  # Cas des heures suivantes : 1h, 4h, 7h, 10h, 13h, 16h, 19h, 22h
            if t[3] < 10:  # Pour transformer 1h, 4h, et 7h en 01h, 04h et 07h
                _heure = time.strftime('0%H:00:00', t)
            else:
                _heure = time.strftime('%H:00:00', t)
        elif t[3] % 3 == 2:  # Cas des heures suivantes : 2h, 5h, 8h, 11h, 14h, 17h, 20h, 23h
            if t[3]-1 < 10:  # Pour transformer 2h, 5h, et 8h en 02h, 05h et 08h
                _heure = '0' + str(t[3]-1) + ':00:00'
            else:
                _heure = str(t[3]-1) + ':00:00'
        else:
            raise ValueError("Le format de créneau horaire n'est pas valide.")
        self.__time = _date + ' ' + _heure

    def __get_json(self):
        """
        Méthode qui se connecte à l'API Météo et affecte la valeur de l'attribut self.__data
        """
        # Connexion à l'API
        resp = requests.get(self.url)
        if resp.status_code != 200:
            # This means something went wrong.
            raise NotImplementedError(
                "Erreur {} : vous n'avez pas réussi à vous connecter à l'url {}.".format(resp.status_code, self.url))
        # Retourne les informations extraites pour un créneau horaire précis
        self.__data = resp.json()[self.__time]

    # Définition des getters et setters de la classe
    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, value):
        raise AttributeError("You are not allowed to modify time by {} !".format(value))

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value):
        raise AttributeError("You are not allowed to modify data by {} !".format(value))

    @property
    def temperature(self):
        return self.__temperature

    @temperature.setter
    def temperature(self, value):
        raise AttributeError("You are not allowed to modify temperature by {} !".format(value))

    @property
    def rain(self):
        return self.__rain

    @rain.setter
    def rain(self, value):
        raise AttributeError("You are not allowed to modify rain by {} !".format(value))

    @property
    def convective_rain(self):
        return self.__convective_rain

    @convective_rain.setter
    def convective_rain(self, value):
        raise AttributeError("You are not allowed to modify convective_rain by {} !".format(value))

    @property
    def snow(self):
        return self.__snow

    @snow.setter
    def snow(self, value):
        raise AttributeError("You are not allowed to modify snow by {} !".format(value))

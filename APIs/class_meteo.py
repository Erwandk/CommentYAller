#!usr/bin/env/python3
# -*- coding: utf-8 -*-

__author__ = 'eke, gab, axel'

import requests
import time
from threading import Thread
from APIs.class_api import API


class Meteo(API, Thread):

    def __init__(self):
        Thread.__init__(self)
        API.__init__(self,
                     url='http://www.infoclimat.fr/public-api/gfs/json?_ll=48.85341,2.3488&_auth=CBIAFwN9BiRRfFtsA3ULIgBoBTBdK1dwA38CYVs%2BB3pWPVAxVDRTNVY4VyoFKlVjWXQFZl5lUmIBagZ%2BCHpXNghiAGwDaAZhUT5bPgMsCyAALgVkXX1XcANhAmZbPgd6VjRQPVQyUy9WO1cxBTdVf1loBWdeYFJ1AX0GYAhgVzcIYwBjA2MGZVE9WzADMgsgACwFYF0wVz0DZwJnW2IHY1ZjUDdUMlMxVjtXZwUwVX9ZYwVkXmBSaAFrBmQIZ1c1CHQAewMZBhdRI1t5A3ELagB1BXhdN1cxAzQ%3D&_c=cc703eb909f9f00058063c7c570f6a45',
                     nom='meteo')
        self.__time = ''
        self.__data = dict()  # Json retourné par l'API
        self.temperature = 0  # Température au sol en °C
        self.rain = 0  # Nbr de mm de précipitation (sur un créneau de 3h)
        self.convective_rain = 0  # Nbr de mm de précipitation convective (sur un créneau de 3h)
        self.snow = ""  # 'oui' s'il y a un risque de neige, 'non' sinon

    def run(self):
        self.__time = self.__set_time()
        self.__data = self.__get_json()
        self.temperature = round(self.__data['temperature']['sol']-273, 2)
        self.rain = self.__data['pluie']
        self.convective_rain = self.__data['pluie_convective']
        self.snow = self.__data['risque_neige']

    @staticmethod
    def __set_time():
        t = time.localtime()
        # Date
        _date = time.strftime('20%y-%m-%d', t)
        # Créneau horaire
        if t[3] == 0 or t[3] == 1:  # Cas entre 00h00 et 01h59 -> aller sur le créneau 23h de la veille
            # todo : cas du premier jour du mois -> pour aller sur le créneau de la veille il faut changer de mois
            _date = time.strftime('20%y-%m-', t) + str(t[2]-1)
            _heure = '23:00:00'
        elif t[3] % 3 == 0 and t[3] != 0:  # Cas des heures suivantes : 3h, 6h, 9h, 12h, 15h, 18h, 21h
            if t[3]-1 < 10:  # Pour transformer 2h, 5h, et 8h en 02h, 05h et 08h
                _heure = '0' + str(t[3]-1) + ':00:00'
            else:
                _heure = str(t[3]-1) + ':00:00'
        elif t[3] % 3 == 1 and t[3] != 1:  # Cas des heures suivantes : 4h, 7h, 10h, 13h, 16h, 19h, 22h
            if t[3]-2 < 10:  # Pour transformer 2h, 5h, et 8h en 02h, 05h et 08h
                _heure = '0' + str(t[3]-2) + ':00:00'
            else:
                _heure = str(t[3]-2) + ':00:00'
        elif t[3] % 3 == 2:  # Cas des heures suivantes : 2h, 5h, 8h, 11h, 14h, 17h, 20h, 23h
            if t[3] < 10:  # Pour transformer 2h, 5h, et 8h en 02h, 05h et 08h
                _heure = time.strftime('0%H:00:00', t)
            else:
                _heure = time.strftime('%H:00:00', t)
        else:
            raise ValueError
        _dateheure = _date + ' ' + _heure
        return _dateheure

    def __get_json(self):
        # Connexion à l'API
        resp = requests.get(self.url)
        if resp.status_code != 200:
            # This means something went wrong.
            raise NotImplementedError(
                "Erreur {} : vous n'avez pas réussi à vous connecter à l'url {}.".format(resp.status_code, self.url))
        # Retourne les informations extraites pour un créneau horaire précis
        return resp.json()[self.__time]


if __name__ == '__main__':

    # Tests
    test = Meteo()
    print(test.temperature)
    print(test.rain)
    print(test.convective_rain)
    print(test.snow)

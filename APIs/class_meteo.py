#!usr/bin/env/python3
# -*- coding: utf-8 -*-

__author__ = 'eke, gab, axel'

import requests
from APIs.class_api import API
import time


class Meteo(API):

    def __init__(self):
        API.__init__(self,
                     url='http://www.infoclimat.fr/public-api/gfs/json?_ll=48.85341,2.3488&_auth=CBIAFwN9BiRRfFtsA3ULIgBoBTBdK1dwA38CYVs%2BB3pWPVAxVDRTNVY4VyoFKlVjWXQFZl5lUmIBagZ%2BCHpXNghiAGwDaAZhUT5bPgMsCyAALgVkXX1XcANhAmZbPgd6VjRQPVQyUy9WO1cxBTdVf1loBWdeYFJ1AX0GYAhgVzcIYwBjA2MGZVE9WzADMgsgACwFYF0wVz0DZwJnW2IHY1ZjUDdUMlMxVjtXZwUwVX9ZYwVkXmBSaAFrBmQIZ1c1CHQAewMZBhdRI1t5A3ELagB1BXhdN1cxAzQ%3D&_c=cc703eb909f9f00058063c7c570f6a45',
                     nom='meteo')

    def _set_time(self):
        t = time.localtime()
        # Date
        date = time.strftime('20%y-%m-%d')
        # Créneau horaire
        if t[3] == 0 or t[3] == 1:  # Cas entre 00h00 et 01h59 -> aller sur le créneau 23h de la veille
            # todo : cas du premier jour du mois -> pour aller sur le créneau de la veille il faut changer de mois
            date = time.strftime('20%y-%m-') + str(t[2]-1)
            heure = '23:00:00'
        elif t[3] % 3 == 0 and t[3] != 0:  # Cas des heures suivantes : 3h, 6h, 9h, 12h, 15h, 18h, 21h
            if t[3]-1 < 10:  # Pour transformer 2h, 5h, et 8h en 02h, 05h et 08h
                heure = '0' + str(t[3]-1) + ':00:00'
            else:
                heure = str(t[3]-1) + ':00:00'
        elif t[3] % 3 == 1 and t[3] != 1:  # Cas des heures suivantes : 4h, 7h, 10h, 13h, 16h, 19h, 22h
            if t[3]-2 < 10:  # Pour transformer 2h, 5h, et 8h en 02h, 05h et 08h
                heure = '0' + str(t[3]-2) + ':00:00'
            else:
                heure = str(t[3]-2) + ':00:00'
        elif t[3] % 3 == 2:  # Cas des heures suivantes : 2h, 5h, 8h, 11h, 14h, 17h, 20h, 23h
            if t[3] < 10:  # Pour transformer 2h, 5h, et 8h en 02h, 05h et 08h
                heure = time.strftime('0%H:00:00')
            else:
                heure = time.strftime('%H:00:00')
        dateheure = date + ' ' + heure
        print(dateheure)
        return dateheure

    def get_infos(self):
        # Connexion à l'API
        resp = requests.get(self.url)
        if resp.status_code != 200:
            # This means something went wrong.
            raise NotImplementedError(
                "Erreur {} : vous n'avez pas réussi à vous connecter à l'url {}.".format(resp.status_code, self.url))
        dateheure = self._set_time()
        # Extraction des informations
        weather_data = resp.json()[dateheure]
        return weather_data

    def get_temperature(self):
        weather_data = self.get_infos()
        temperature_celsius = round(weather_data['temperature']['sol']-273, 2)
        print("Température : {} °C".format(temperature_celsius))
        return temperature_celsius

    def get_precipitation(self):
        weather_data = self.get_infos()
        pluie = weather_data['pluie']
        pluie_convective = weather_data['pluie_convective']
        neige = weather_data['risque_neige']
        print("Précipitation : pluie : {} / pluie convective : {} / neige : {} ".format(pluie, pluie_convective, neige))
        return pluie, pluie_convective, neige


if __name__ == '__main__':

    # Tests
    test = Meteo()
    precipitation = test.get_precipitation()
    print(precipitation)
    temperature = test.get_temperature()
    print(temperature)
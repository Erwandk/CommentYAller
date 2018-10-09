import requests
import class_api
import time


class Meteo(class_api.API):

    def __init__(self):
        self.url = 'http://www.infoclimat.fr/public-api/gfs/json?_ll=48.85341,2.3488&_auth=CBIAFwN9BiRRfFtsA3ULIgBoBTBdK1dwA38CYVs%2BB3pWPVAxVDRTNVY4VyoFKlVjWXQFZl5lUmIBagZ%2BCHpXNghiAGwDaAZhUT5bPgMsCyAALgVkXX1XcANhAmZbPgd6VjRQPVQyUy9WO1cxBTdVf1loBWdeYFJ1AX0GYAhgVzcIYwBjA2MGZVE9WzADMgsgACwFYF0wVz0DZwJnW2IHY1ZjUDdUMlMxVjtXZwUwVX9ZYwVkXmBSaAFrBmQIZ1c1CHQAewMZBhdRI1t5A3ELagB1BXhdN1cxAzQ%3D&_c=cc703eb909f9f00058063c7c570f6a45'
        self.nom = 'meteo'

    def get_infos(self):
        #  TODO : à construire à partir de la méthode get_infos de la classe API
        # Connexion à l'API
        resp = requests.get(self.url)
        if resp.status_code != 200:
            # This means something went wrong.
            raise NotImplementedError(
                "Erreur {} : vous n'avez pas réussi à vous connecter à l'url {}.".format(resp.status_code, self.url))
        # Paramétrage du temps (date et heure)
        t = time.localtime()
        # Date
        if len(str(t[2]))<2: # pour passer de 2018-10-7 à 2018-10-07
            a = '0'
        else:
            a = ''
        date = str(t[0]) + '-' + str(t[1]) + '-' + a + str(t[2]) # au format 'aaaa-mm-jj'
        # Créneau horaire
        if t[3]%3 == 0: # Cas des heures suivantes : 00h, 3h, 6h, 9h, 12h, 15h, 18h, 21h
            heure = str(t[3]-1) + ':00:00'
        elif t[3]%3 == 1: # Cas des heures suivantes : 1h, 4h, 7h, 10h, 13h, 16h, 19h, 22h
            heure = str(t[3]-2) + ':00:00'
        elif t[3]%3 == 2:
            heure = str(t[3]) + ':00:00'
        dateheure = date + ' ' + heure
        print(dateheure)
        # Extraction des informations
        weather_data = resp.json()[dateheure]
        return weather_data

    def get_temperature(self):
        weather_data = self.get_infos()
        temperature_celsius = round(weather_data['temperature']['sol']-273,2)
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

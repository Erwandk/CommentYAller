#!usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'eke, gab, axel'

from APIs.class_api import API
import requests


class Elevation(API):
    """
    API Google Maps pour connaître le dénivelé positif et négatif le long d'un chemin
    """

    def __init__(self, steps, user_id=1):
        API.__init__(self, api_name="elevation", url="https://maps.googleapis.com/maps/api/elevation/",
                     user_id=user_id)
        self.__steps = steps  # Liste des étapes de l'itinéraire obtenue par l'API GoogleMaps
        self.__path = 'json?locations='
        self.__asc_elevation = 0  # Dénivelé positif (en m)
        self.__dsc_elevation = 0  # Dénivelé négatif (en m)
        self.__json = dict()

    def compute_elevation(self):
        self.__def_path()
        self.__retrieve_data_api()
        # Calcul du dénivelé positif et négatif
        for i in range(1, len(self.__json['results'])):
            if self.__json['results'][i]['elevation'] > self.__json['results'][i-1]['elevation']:
                self.__asc_elevation += self.__json['results'][i]['elevation']-self.__json['results'][i-1]['elevation']
            elif self.__json['results'][i]['elevation'] < self.__json['results'][i-1]['elevation']:
                self.__dsc_elevation += self.__json['results'][i-1]['elevation']-self.__json['results'][i]['elevation']

    def __def_path(self):
        # ajout du point de départ
        self.__path += '{},{}'.format(self.__steps[0][2]['lat'], self.__steps[0][2]['lng'])
        # pour chaque étape, ajout du point final de l'étape
        for i in range(len(self.__steps)):
            self.__path += '|{},{}'.format(self.__steps[i][3]['lat'], self.__steps[i][3]['lng'])
        # finir en ajoutant la clé
        self.__path += '&key={}'.format(self._key)
        if len(self.__path) > 8192:
            raise AttributeError("Erreur: le nbr de points GPS renseignés dépasse la limite autorisée pour la requête à"
                                 " l'API GoogleMaps Elevation.")

    def __retrieve_data_api(self):
        resp = requests.get(self._url+self.__path)
        if resp.status_code != 200:
            raise NotImplementedError("Erreur {} : vous n'avez pas réussi à vous connecter à "
                                      "l'url {}{}.".format(resp.status_code, self._url, self.__path))
        self.__json = resp.json()
        if self.__json['status'] != 'OK':
            raise NotImplementedError("Requête à l'API GoogleMaps Elevation invalide. "
                                      "Vérifiez la clé ou le quota de requêtes autorisées.")

    @property
    def json(self):
        return self.__json

    @property
    def url(self):
        return self._url

    @property
    def path(self):
        return self.__path

    @property
    def steps(self):
        return self.__steps

    @steps.setter
    def steps(self, value):
        # todo : trouver l'exception à lever
        self.__steps = value

    @property
    def asc_elevation(self):
        return self.__asc_elevation

    @asc_elevation.setter
    def asc_elevation(self, value):
        raise AttributeError("Your are not allowed to modify asc_elevation by {}".format(value))

    @property
    def dsc_elevation(self):
        return self.__dsc_elevation

    @dsc_elevation.setter
    def dsc_elevation(self, value):
        raise AttributeError("Your are not allowed to modify dsc_elevation by {}".format(value))


if __name__ == '__main__':

    def main():
        # a : steps du trajet en vélo
        a = [(77,
              14,
              {'lat': 48.8544597, 'lng': 2.277063},
              {'lat': 48.85404399999999, 'lng': 2.2779031},
              'BICYCLING',
              'No transit'),
             (42,
              58,
              {'lat': 48.85404399999999, 'lng': 2.2779031},
              {'lat': 48.8543168, 'lng': 2.2783061},
              'BICYCLING',
              'No transit'),
             (173,
              59,
              {'lat': 48.8543168, 'lng': 2.2783061},
              {'lat': 48.8554038, 'lng': 2.2766129},
              'BICYCLING',
              'No transit'),
             (129,
              41,
              {'lat': 48.8554038, 'lng': 2.2766129},
              {'lat': 48.8562023, 'lng': 2.2778873},
              'BICYCLING',
              'No transit'),
             (111,
              22,
              {'lat': 48.8562023, 'lng': 2.2778873},
              {'lat': 48.8569232, 'lng': 2.2789319},
              'BICYCLING',
              'No transit'),
             (38,
              7,
              {'lat': 48.8569232, 'lng': 2.2789319},
              {'lat': 48.8566821, 'lng': 2.2792981},
              'BICYCLING',
              'No transit'),
             (155,
              28,
              {'lat': 48.8566821, 'lng': 2.2792981},
              {'lat': 48.85774319999999, 'lng': 2.2796933},
              'BICYCLING',
              'No transit'),
             (369,
              84,
              {'lat': 48.85774319999999, 'lng': 2.2796933},
              {'lat': 48.8585224, 'lng': 2.2845921},
              'BICYCLING',
              'No transit'),
             (29,
              14,
              {'lat': 48.8585224, 'lng': 2.2845921},
              {'lat': 48.8586032, 'lng': 2.2848623},
              'BICYCLING',
              'No transit'),
             (17,
              9,
              {'lat': 48.8586032, 'lng': 2.2848623},
              {'lat': 48.8586961, 'lng': 2.2847108},
              'BICYCLING',
              'No transit'),
             (403,
              102,
              {'lat': 48.8586961, 'lng': 2.2847108},
              {'lat': 48.8620282, 'lng': 2.286593},
              'BICYCLING',
              'No transit'),
             (71,
              26,
              {'lat': 48.8620282, 'lng': 2.286593},
              {'lat': 48.8625045, 'lng': 2.2872211},
              'BICYCLING',
              'No transit'),
             (131,
              24,
              {'lat': 48.8625045, 'lng': 2.2872211},
              {'lat': 48.8634214, 'lng': 2.2875215},
              'BICYCLING',
              'No transit'),
             (1223,
              271,
              {'lat': 48.8634214, 'lng': 2.2875215},
              {'lat': 48.8733455, 'lng': 2.2947326},
              'BICYCLING',
              'No transit'),
             (617,
              107,
              {'lat': 48.8733455, 'lng': 2.2947326},
              {'lat': 48.8778055, 'lng': 2.2981464},
              'BICYCLING',
              'No transit'),
             (67,
              45,
              {'lat': 48.8778055, 'lng': 2.2981464},
              {'lat': 48.87832299999999, 'lng': 2.2985015},
              'BICYCLING',
              'No transit'),
             (1373,
              316,
              {'lat': 48.87832299999999, 'lng': 2.2985015},
              {'lat': 48.8812911, 'lng': 2.3165925},
              'BICYCLING',
              'No transit'),
             (813,
              235,
              {'lat': 48.8812911, 'lng': 2.3165925},
              {'lat': 48.8834131, 'lng': 2.3272065},
              'BICYCLING',
              'No transit'),
             (208,
              61,
              {'lat': 48.8834131, 'lng': 2.3272065},
              {'lat': 48.8844183, 'lng': 2.3294653},
              'BICYCLING',
              'No transit'),
             (238,
              48,
              {'lat': 48.8844183, 'lng': 2.3294653},
              {'lat': 48.8836147, 'lng': 2.3324198},
              'BICYCLING',
              'No transit'),
             (17,
              5,
              {'lat': 48.8836147, 'lng': 2.3324198},
              {'lat': 48.8836489, 'lng': 2.332649},
              'BICYCLING',
              'No transit'),
             (553,
              132,
              {'lat': 48.8836489, 'lng': 2.332649},
              {'lat': 48.8819064, 'lng': 2.3396986},
              'BICYCLING',
              'No transit'),
             (748,
              134,
              {'lat': 48.8819064, 'lng': 2.3396986},
              {'lat': 48.8836148, 'lng': 2.349562},
              'BICYCLING',
              'No transit'),
             (1110,
              244,
              {'lat': 48.8836148, 'lng': 2.349562},
              {'lat': 48.88427189999999, 'lng': 2.3646798},
              'BICYCLING',
              'No transit'),
             (466,
              130,
              {'lat': 48.88427189999999, 'lng': 2.3646798},
              {'lat': 48.8826335, 'lng': 2.369938},
              'BICYCLING',
              'No transit'),
             (1831,
              432,
              {'lat': 48.8826335, 'lng': 2.369938},
              {'lat': 48.8887876, 'lng': 2.3931278},
              'BICYCLING',
              'No transit'),
             (261,
              63,
              {'lat': 48.8887876, 'lng': 2.3931278},
              {'lat': 48.8865138, 'lng': 2.3940114},
              'BICYCLING',
              'No transit'),
             (328,
              148,
              {'lat': 48.8865138, 'lng': 2.3940114},
              {'lat': 48.8837451, 'lng': 2.3948037},
              'BICYCLING',
              'No transit'),
             (72,
              27,
              {'lat': 48.8837451, 'lng': 2.3948037},
              {'lat': 48.8833879, 'lng': 2.3939889},
              'BICYCLING',
              'No transit')]
        # final_pos = {'lat':48.854606, 'lng':2.277205}  # 6 rue des marronniers
        # init_pos = {'lat':48.854962, 'lng':2.275464}  # 31 rue des marronniers
        test = Elevation(a)
        test.compute_elevation()
        print('url {}{}'.format(test.url, test.path))
        print("nombre de caractères:{}".format(len(test.url+test.path)))
        print(test.json)
        # print(test.elevation)
        print(test.asc_elevation)
        print(test.dsc_elevation)


    main()

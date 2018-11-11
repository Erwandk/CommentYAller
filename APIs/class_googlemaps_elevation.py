#!usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'eke, gab, axel'

# Importation de la classe mère API et des modules utilisés
from APIs.class_api import API
import requests


class Elevation(API):
    """
    Classe API Google Maps pour connaître le dénivelé positif et négatif le long d'un chemin
    """

    def __init__(self, steps, user_id=1):
        """
        :param steps: liste des étapes (list)
        :param user_id: id du user (int)
        """
        assert isinstance(steps, list) and isinstance(user_id, int)
        API.__init__(self, api_name="elevation", url="https://maps.googleapis.com/maps/api/elevation/",
                     user_id=user_id)
        self.__steps = steps  # Liste des étapes de l'itinéraire obtenue par l'API GoogleMaps
        self.__path = 'json?locations='
        self.__asc_elevation = 0  # Dénivelé positif (en m)
        self.__dsc_elevation = 0  # Dénivelé négatif (en m)
        self.__json = dict()

    def compute_elevation(self):
        """
        Méthode permettant de calculer l'élévation du trajet
        """
        self.__def_path()
        self.__retrieve_data_api()
        # Calcul du dénivelé positif et négatif
        for i in range(1, len(self.__json['results'])):
            if self.__json['results'][i]['elevation'] > self.__json['results'][i-1]['elevation']:
                self.__asc_elevation += self.__json['results'][i]['elevation']-self.__json['results'][i-1]['elevation']
            elif self.__json['results'][i]['elevation'] < self.__json['results'][i-1]['elevation']:
                self.__dsc_elevation += self.__json['results'][i-1]['elevation']-self.__json['results'][i]['elevation']

    def __def_path(self):
        """
        Méthode permettant de calculer le path de l'url pour se connecter à l'API
        """
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
        """
        Méthode permettant de récupérer les données de l'API
        """
        resp = requests.get(self._url+self.__path)
        if resp.status_code != 200:
            raise NotImplementedError("Erreur {} : vous n'avez pas réussi à vous connecter à "
                                      "l'url {}{}.".format(resp.status_code, self._url, self.__path))
        self.__json = resp.json()
        if self.__json['status'] != 'OK':
            raise NotImplementedError("Requête à l'API GoogleMaps Elevation invalide. "
                                      "Vérifiez la clé ou le quota de requêtes autorisées.")

    # Définition des getters et setters de la classe
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
        assert isinstance(value, list)
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

#!usr/bin/env/python3
# -*- coding: utf-8 -*-

__author__ = 'eke, gab, axel'

from APIs.class_api import API
from threading import Thread
import requests
import math


class Velib_Station(Thread, API):
    """Classe Vélib pour connaître la station de départ et la station d'arrivée d'un itinéraire vélib en fonction de
    l'adresse de départ et de l'adresse d'arrivée de l'utilisateur, et en fonction des vélos et places disponibles en
    temps réel. Rq : pas de calcul d'itinéraire pour du non temps réel (car pas d'infos sur les vélos et places)"""

    def __init__(self, gps_position, type):
        API.__init__(self,
                     url='https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&rows=2000',
                     nom='velib')
        Thread.__init__(self)
        self.__list = list()  # Liste des stations Vélib pourvues de coordonnées GPS avec leurs infos temps réel
        self.__index = 0  # Indice de la station dans la liste self.list
        self.__name = str()
        self.__latitude = float()
        self.__longitude = float()
        self.__coord = str()  # Coord GPS au format exploitable par l'API Google Maps : 'latitude'+'%2C'+'longitude'
        self.__bikes = int()  # Nombre de vélos disponibles
        self.__docks = int()  # Nombre de places disponibles
        self.__type = type  # Prend les valeurs 'departure' et 'arrival' pour distinguer les 2 stations de l'itinéraire
        self.__gps_position = gps_position  # Position renseignée par l'utilisateur (point de départ ou arrivée)

    def __repr__(self):
        return "Station: {}\n" \
               "Coordonnées: {}; {}\n" \
               "Vélos disponibles: {}\n" \
               "Places disponibles: {}".format(self.name, self.latitude, self.longitude, self.bikes, self.docks)

    def run(self):
        """Méthode permettant de choisir la station adéquate et d'attribuer les attributs de l'obj en conséquent
        :param position : adresse renseignée par l'utilisateur ou coord GPS de géoloc - de départ ou d'arrivée"""
        self.__retrieve_data_api()  # Appel à l'API et assignation de l'attribut self.list
        self.__closer_station(self.__gps_position)  # Détermine la station la plus proche et assigne self.index
        self.__name = self.list[self.index]['fields']['name']
        self.__latitude = self.list[self.index]['fields']['lat']
        self.__longitude = self.list[self.index]['fields']['lon']
        self.__coord = str(self.__latitude) + '%2C' + str(self.__longitude)
        self.__bikes = self.list[self.index]['fields']['numbikesavailable']
        self.__docks = self.list[self.index]['fields']['numdocksavailable']

    def __retrieve_data_api(self):
        """Méthode qui se connecte à l'API 'Velib disponibilité temps réel' et affecte l'attribut self.__list : liste de
        dictionnaires des données temps réel des stations comportant des coordonnées GPS"""
        # Connexion à l'API
        resp = requests.get(self.url)
        if resp.status_code != 200:
            # This means something went wrong.
            raise NotImplementedError(
                "Erreur {} : vous n'avez pas réussi à vous connecter à l'url {}.".format(resp.status_code, self.url))
        # Extraction de la liste des stations comportant des coordonnées GPS (les autres sont inexploitables)
        X = resp.json()['records']  # liste de toutes les stations
        self.__list = [X[k] for k in range(len(X)) if 'geometry' in X[k].keys()]
        # Renvoit la liste des stations où les coordonnées GPS existent
        return

    def __closer_station(self, gps_position):
        """ Méthode permettant de définir la station la plus proche d'un point GPS parmi la liste des stations dispos et
        d'affecter l'attribut self.index
        :param gps_position: Coordonnées GPS d'un point (départ ou arrivée) au format dict{'lat':XXX; 'lng':XXX}
        :return:
        """
        d = float('inf')
        if self.__type == 'departure':  # Traitement pour la station de départ (vérifie qu'il y a des vélos dispos)
            for j in range(len(self.__list)):  # Parcourt toute la liste des stations
                station_position = self.__list[j]['fields']['xy']  # format : list [latitude, longitude]
                distance = self.__distance(station_position, gps_position)
                if distance < d and self.__list[j]['fields']['numbikesavailable'] > 0:  # Vérifie la dispo des vélos
                    d = distance
                    self.__index = j
        elif self.__type == 'arrival':  # Traitement pour la station d'arrivée (vérifie qu'il y a des places dispos)
            for j in range(len(self.__list)):  # Parcourt toute la liste des stations
                station_position = self.__list[j]['fields']['xy']  # format : list [latitude, longitude]
                distance = self.__distance(station_position, gps_position)
                if distance < d and self.__list[j]['fields']['numdocksavailable'] > 0:  # Vérifie la dispo des places
                    d = distance
                    self.__index = j
        else:
            raise NotImplementedError("Le type de station renseigné n'est pas reconnu. Type = 'departure' ou 'arrival'")
        return

    @staticmethod
    def __distance(station_position, gps_position):
        """ Méthode permettant de calculer la distance entre une station Vélib et un point donné
        :param station_position: Coordonnées GPS d'une station au format list[latitude, longitude]
        :param gps_position: Coordonnées GPS d'un point (départ ou arrivée) au format dict{'lat':XXX; 'lng':XXX}
        :return:
        """
        x1, y1 = station_position[0], station_position[1]
        x2, y2 = gps_position['lat'], gps_position['lng']
        return math.sqrt((y2-y1)**2+(x2-x1)**2)

    @property
    def list(self):
        return self.__list

    @list.setter
    def list(self, value):
        print("You are not allowed to modify list by {}".format(value))

    @property
    def index(self):
        return self.__index

    @index.setter
    def index(self, value):
        print("You are not allowed to modify index by {}".format(value))

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        print("You are not allowed to modify name by {}".format(value))

    @property
    def latitude(self):
        return self.__latitude

    @latitude.setter
    def latitude(self, value):
        print("You are not allowed to modify latitude by {}".format(value))

    @property
    def longitude(self):
        return self.__longitude

    @longitude.setter
    def longitude(self, value):
        print("You are not allowed to modify longitude by {}".format(value))

    @property
    def coord(self):
        return self.__coord

    @coord.setter
    def coord(self, value):
        print("You are not allowed to modify coord by {}".format(value))

    @property
    def bikes(self):
        return self.__bikes

    @bikes.setter
    def bikes(self, value):
        print("You are not allowed to modify bikes by {}".format(value))

    @property
    def docks(self):
        return self.__docks

    @docks.setter
    def docks(self, value):
        print("You are not allowed to modify docks by {}".format(value))

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        print("You are not allowed to modify type by {}".format(value))

    @property
    def gps_position(self):
        return self.__gps_position

    @gps_position.setter
    def gps_position(self, value):
        # todo : lever exception si mauvais format
        self.__gps_position = value
        return self.__gps_position


if __name__ == '__main__':
    coord = {'lat': 48.834269, 'lng': 2.296338}
    Test = Velib_Station(coord, 'departure')
    Test.start()
    Test.join()
    print(Test)
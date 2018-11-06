#!usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'eke, gab, axel'

import folium
import numpy as np
import os


class Maps:
    """
    Classe représentant le trajet sur une carte, affichée dans la page des résultats
    """

    def __init__(self, trip, trip_type):

        self.__trip = trip
        self.__trip_type = trip_type
        self.__etape = Maps.__set_mode(self)

        # Mise à l'échelle de la carte en calculant les coordonnées des 4 coins
        self.__min_lat = min([etapes[2]["lat"] for etapes in self.__etape]+[trip.gps_final['lat']]) - 0.00025
        self.__max_lat = max([etapes[2]["lat"] for etapes in self.__etape]+[trip.gps_final['lat']]) + 0.00025
        self.__min_lon = min([etapes[2]["lng"] for etapes in self.__etape]+[trip.gps_final['lng']]) - 0.00025
        self.__max_lon = max([etapes[2]["lng"] for etapes in self.__etape]+[trip.gps_final['lng']]) + 0.00025

        # On crée la carte et on l'enregistre
        self.__get_save_map()

    def __set_mode(self):
        """
        Renvoi les étapes propres à un trajet en particulier
        """

        if self.__trip_type == "trip_foot":
            return self.__trip.trip_foot.steps
        elif self.__trip_type == 'trip_bicycle':
            return self.__trip.trip_bicycle.steps
        elif self.__trip_type == "trip_car":
            return self.__trip.trip_car.steps
        elif self.__trip_type == "trip_velib":
            return self.__trip.trip_velib.steps
        elif self.__trip_type == "trip_transit":
            return self.__trip.trip_transit.steps
        else:
            raise ValueError("Could not identify trip_type value !")

    def __get_save_map(self):
        """
        Méthode permettant de créer et enregistrer une carte
        """

        __map_name = "map{}.html".format(self.__trip_type[4:])
        __path = os.path.join(os.getcwd(), "static", "map", str(__map_name))

        # Icones
        __map_icone = {"WALKING": "male", "BICYCLING": "bicycle", "DRIVING": "car", "TRANSIT": "bus"}


        # Création de la carte
        __lat_center = (self.__min_lat + self.__max_lat) / 2
        __lng_center = (self.__min_lon + self.__max_lon) / 2
        __zoom = Maps.compute_zoom([self.__min_lat, self.__min_lon], [self.__max_lat, self.__max_lon])
        maps = folium.Map(location=[__lat_center, __lng_center], zoom_start=__zoom)

        # Ajout de marqueurs initiaux, finaux ainsi que pout chaque étape
        folium.Marker([self.__trip.gps_init["lat"], self.__trip.gps_init["lng"]], icon=folium.Icon(color="green"),
                      popup="<b>Start <br> </b>{}".format(self.__etape[0][6])).add_to(maps)
        folium.Marker([self.__trip.gps_final["lat"], self.__trip.gps_final["lng"]], icon=folium.Icon(color="red"),
                      popup="<b>End</b>").add_to(maps)
        for k in range(1, len(self.__etape)):
            __icone = __map_icone[self.__etape[k][4]]
            folium.Marker([self.__etape[k][2]["lat"], self.__etape[k][2]["lng"]],
                          icon=folium.Icon(icon=__icone, prefix='fa'),
                          popup="<i>Etape {} <br> {}</i>".format(k, self.__etape[k][6])
                          ).add_to(maps)

        # Enregistrement de la carte
        maps.save(__path)

    @staticmethod
    def distance(x1, y1):
        return np.sqrt((x1[0] - y1[0]) ** 2 + (x1[1] - y1[1]) ** 2)

    @staticmethod
    def compute_zoom(x1, y1):
        __dist = Maps.distance(x1, y1)
        return 15 - 31.384 * (__dist - 0.00061)

    # Définition des getters et setters de la classe
    @property
    def min_lat(self):
        return self.__min_lat

    @min_lat.setter
    def min_lat(self, value):
        raise AttributeError("You are not allowed to modify min_lat by {}".format(value))

    @property
    def max_lat(self):
        return self.__max_lat

    @max_lat.setter
    def max_lat(self, value):
        raise AttributeError("You are not allowed to modify max_lat by {}".format(value))

    @property
    def min_lon(self):
        return self.__min_lon

    @min_lon.setter
    def min_lon(self, value):
        raise AttributeError("You are not allowed to modify min_lon by {}".format(value))

    @property
    def max_lon(self):
        return self.__max_lon

    @max_lon.setter
    def max_lon(self, value):
        raise AttributeError("You are not allowed to modify max_lon by {}".format(value))

    @property
    def trip(self):
        return self.__trip

    @trip.setter
    def trip(self, value):
        raise AttributeError("You are not allowed to modify trip by {}".format(value))

    @property
    def trip_type(self):
        return self.__trip_type

    @trip_type.setter
    def trip_type(self, value):
        if value not in ['trip_foot', 'trip_bicycle', 'trip_car', 'trip_velib', 'trip_transit']:
            raise ValueError("You are not allowed to modify trip_type by {}".format(value))
        self.__trip_type = value

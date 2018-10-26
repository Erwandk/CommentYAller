#!usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'eke, gab, axel'

class Carte:

    def __init__(self, trip, type_trip):
        """trip_type est censé etre de la forme 'trip.trip_foot'"""
        self.__etape = Carte.set_mode(trip)
        self.__min_lat = min([etapes[2]["lat"] for etapes in self.__etape]+[trip.gps_final['lat']]) - 0.00025
        self.__max_lat = max([etapes[2]["lat"] for etapes in self.__etape]+[trip.gps_final['lat']]) + 0.00025
        self.__min_lon = min([etapes[2]["lng"] for etapes in self.__etape]+[trip.gps_final['lng']]) - 0.00025
        self.__max_lon = max([etapes[2]["lng"] for etapes in self.__etape]+[trip.gps_final['lng']]) + 0.00025

    @staticmethod
    def set_mode(trip):

        if trip.recommandation == "trip_foot":
            return trip.trip_foot.steps
        elif trip.recommandation == 'trip_bicycle':
            return trip.trip_bicycle.steps
        elif trip.recommandation == "trip_car":
            return trip.trip_car.steps
        else:
            return trip.trip_transit.steps

    @property
    def min_lat(self):
        return self.__min_lat

    @min_lat.setter
    def min_lat(self,valeur):
        print("You are not allowed to modify min_lat by {}".format(valeur))

    @property
    def max_lat(self):
        return self.__max_lat

    @max_lat.setter
    def max_lat(self,valeur):
        print("You are not allowed to modify max_lat by {}".format(valeur))

    @property
    def min_lon(self):
        return self.__min_lon

    @min_lon.setter
    def min_lon(self,valeur):
        print("You are not allowed to modify max_lat by {}".format(valeur))

    @property
    def max_lon(self):
        return self.__max_lon

    @max_lon.setter
    def max_lon(self,valeur):
        print("You are not allowed to modify max_lon by {}".format(valeur))

#!usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'eke, gab, axel'

from Trip.class_itinary import Foot, Bicycle, Car, Transit


class Trip:
    """
    Cette classe représente le trajet dans son ensemble avec toutes les données correspondantes.
    """

    def __init__(self, pos_init, pos_final):
        """
        Le constructeur de cette classe prend en entrée les données de position de départ et d'arrivée
        """
        self.__pos_init = pos_init
        self.__pos_final = pos_final

        self.__gps_init = {'lat': 0, 'lng': 0}
        self.__gps_final = {'lat': 0, 'lng': 0}

        self.__trip_foot = Foot()
        self.__trip_bicycle = Bicycle()
        self.__trip_car = Car()
        self.__trip_transit = Transit()

    # Définition des getters, setters des attributs de notre classe
    @property
    def pos_init(self):
        return self.__pos_init

    @pos_init.setter
    def pos_init(self, valeur):
        print("You are not allowed to modify pos_init by {} !".format(valeur))

    @property
    def pos_final(self):
        return self.__pos_final

    @pos_final.setter
    def pos_final(self, valeur):
        print("You are not allowed to modify pos_final by {} !".format(valeur))

    @property
    def gps_init(self):
        return self.__gps_init

    @gps_init.setter
    def gps_init(self, valeur):
        print("You are not allowed to modify duree_tot by {} !".format(valeur))

    @property
    def gps_final(self):
        return self.__gps_final

    @gps_final.setter
    def gps_final(self, valeur):
        print("You are not allowed to modify gps_final by {} !".format(valeur))

    @property
    def trip_foot(self):
        return self.__trip_foot

    @trip_foot.setter
    def trip_foot(self, valeur):
        print("You are not allowed to modify trip_foot by {} !".format(valeur))

    @property
    def trip_bicyle(self):
        return self.__trip_bicycle

    @trip_bicyle.setter
    def trip_bicyle(self, valeur):
        print("You are not allowed to modify trip_bicyle by {} !".format(valeur))

    @property
    def trip_car(self):
        return self.__trip_car

    @trip_car.setter
    def trip_car(self, valeur):
        print("You are not allowed to modify trip_car by {} !".format(valeur))

    @property
    def trip_transit(self):
        return self.__trip_transit

    @trip_transit.setter
    def trip_transit(self, valeur):
        print("You are not allowed to modify trip_transit by {} !".format(valeur))

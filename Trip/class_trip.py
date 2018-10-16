#!usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'eke, gab, axel'

from Trip.class_itinary import Foot, Bicycle, Car, Transit
from APIs.class_meteo import Meteo


class Trip:
    """
    Cette classe représente le trajet dans son ensemble avec toutes les données correspondantes.
    """

    def __init__(self, pos_init, pos_final, bagage, elevation):
        """
        Le constructeur de cette classe prend en entrée les données de position de départ et d'arrivée
        """
        self.__pos_init = pos_init
        self.__pos_final = pos_final
        self.__bagage = bagage
        self.__elevation = elevation

        self.__meteo = Meteo()

        self.__gps_init = {'lat': 0, 'lng': 0}   # à instancier à l'aide des itinéraires ci-dessous pour éviter
        self.__gps_final = {'lat': 0, 'lng': 0}  # d'appeler de nouveau l'API

        self.__trip_foot = Foot()
        self.__trip_bicycle = Bicycle()
        self.__trip_car = Car()
        self.__trip_transit = Transit()

        # True si nous recommandons le trajet, False sinon
        self.__recommandation = {"foot": True, "bicycle": True, "car": True, "transit": True}

    def analyse(self):
        if self.__bagage == "on":
            self.__recommandation["transit"] = False
        if not self.__meteo.pluie:
            self.__recommandation["foot"] = False
            self.__recommandation["bicycle"] = False

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
    def trip_bicycle(self):
        return self.__trip_bicycle

    @trip_bicycle.setter
    def trip_bicycle(self, valeur):
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

    @property
    def bagage(self):
        return self.__bagage

    @bagage.setter
    def bagage(self, valeur):
        print("You are not allowed to modify bagage by {} !".format(valeur))

    @property
    def elevation(self):
        return self.__elevation

    @elevation.setter
    def elevation(self, valeur):
        print("You are not allowed to modify elevation by {} !".format(valeur))

    @property
    def meteo(self):
        return self.__meteo

    @meteo.setter
    def meteo(self, valeur):
        print("You are not allowed to modify meteo by {} !".format(valeur))

    @property
    def recommandation(self):
        return self.__recommandation

    @recommandation.setter
    def recommandation(self, valeur):
        print("You are not allowed to modify recommandation by {} !".format(valeur))

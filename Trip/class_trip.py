#!usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'eke, gab, axel'

from Trip.class_itinary import Foot, Bicycle, Car, Transit


class Trip:
    """
    Cette classe représente le trajet dans son ensemble avec toutes les données correspondantes.
    """

    def __init__(self, form):
        """
        Le constructeur de cette classe prend en entrée le formulaire entré par l'utilisateur
        """
        self.__pos_init = form.get('pos_init', '')
        self.__pos_final = form.get('pos_final', '')
        self.__check_data = self.__check_form_data()

        self.__gps_init = {'lat': 0, 'lng': 0}
        self.__gps_final = {'lat': 0, 'lng': 0}

        self.__trip_foot = Foot()
        self.__trip_bicycle = Bicycle()
        self.__trip_car = Car()
        self.__trip_transit = Transit()

    def __check_form_data(self):
        """
        Cette fonction checke les données envoyées via le formulaire par l'utilisateur
        """
        if self.pos_init == "" or self.pos_final == "":
            return False
        else:
            return True

    # Définition des getters, setters des attributs de notre classe
    @property
    def check_data(self):
        return self.__check_data

    @check_data.setter
    def check_data(self, valeur):
        print("Reflechir à l'autorisation ou non de la modification de check_data")
        self.__check_data = valeur

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

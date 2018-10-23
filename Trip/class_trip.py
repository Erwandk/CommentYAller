#!usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'eke, gab, axel'

from Trip.class_itinary import Foot, Bicycle, Car, Transit
from APIs.class_meteo import Meteo


class Trip:
    """
    Cette classe représente le trajet dans son ensemble avec toutes les données correspondantes.
    """

    def __init__(self, pos_init, pos_final, bagage, elevation, user_id=0):
        """
        Le constructeur de cette classe prend en entrée les données de position de départ et d'arrivée
        """
        self.__user_id = user_id
        self.__pos_init = self.clean_str(pos_init)
        self.__pos_final = self.clean_str(pos_final)
        self.__bagage = True if bagage == "on" else False
        self.__elevation = True if elevation == "on" else False

        self.__meteo = Meteo()

        self.__trip_foot = Foot(self.__user_id, self.__pos_init, self.pos_final)
        self.__trip_bicycle = Bicycle(self.__user_id, self.__pos_init, self.pos_final)
        self.__trip_car = Car(self.__user_id, self.__pos_init, self.pos_final)
        self.__trip_transit = Transit(self.__user_id, self.__pos_init, self.pos_final)

        self.__gps_init = self.__trip_foot.etapes[0][2]
        self.__gps_final = self.__trip_foot.etapes[len(self.__trip_foot.etapes)-1][3]

        # True si nous recommandons le trajet, False sinon
        self.__recommandation = {"foot": True, "bicycle": True, "car": True, "transit": True}
        self.analyse()

    @staticmethod
    def clean_str(chaine):
        """
         Méthode statique qui transforme une chaine de caractère aux contraintes de l'API GoogleMaps
        """
        __new_chaine = chaine.lower().replace(" ", "+").replace(",", "+")
        if "paris" not in __new_chaine:
            __new_chaine += "+paris"
        return __new_chaine

    def analyse(self):
        """
        Méthode qui calcule nos recommandations en fonction des paramètres du trajet
        """
        if self.__bagage == "on":
            self.__recommandation["transit"] = False
        # TODO : introduire les recommandations météos et autres

    # Définition des getters, setters des attributs de notre classe
    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, valeur):
        print("You are not allowed to modify user_id by {} !".format(valeur))

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
        print("You are not allowed to modify gps_init by {} !".format(valeur))

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

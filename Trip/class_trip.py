#!usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'eke, gab, axel'

from Trip.class_itinary import Foot, Bicycle, Car, Transit, Velib
from APIs.class_meteo import Meteo
import re


class Trip:
    """
    Cette classe représente le trajet dans son ensemble avec toutes les données correspondantes.
    """

    def __init__(self, init_pos, final_pos, bagage, elevation, user_id=0):
        """
        Le constructeur de cette classe prend en entrée les données de position de départ et d'arrivée
        """
        # Définitions des attributs de la classe
        self.__user_id = user_id
        self.__init_pos = self.clean_str(init_pos)
        self.__final_pos = self.clean_str(final_pos)
        self.__bagage = True if bagage == "on" else False
        self.__elevation = True if elevation == "on" else False

        # Définition des différents trajets, sauf Vélib (1 thread = 1 appel à une API)
        self.__meteo = Meteo()
        self.__trip_foot = Foot(self.__user_id, self.__init_pos, self.__final_pos)
        self.__trip_bicycle = Bicycle(self.__user_id, self.__init_pos, self.__final_pos)
        self.__trip_car = Car(self.__user_id, self.__init_pos, self.__final_pos)
        self.__trip_transit = Transit(self.__user_id, self.__init_pos, self.__final_pos)

        # Lancement des threads
        self.__meteo.start()
        self.__trip_foot.start()
        self.__trip_bicycle.start()
        self.__trip_car.start()
        self.__trip_transit.start()

        # Attente de la fin des threads
        self.__meteo.join()
        self.__trip_foot.join()
        self.__trip_bicycle.join()
        self.__trip_car.join()
        self.__trip_transit.join()

        # TODO : compute something to manage bugs (no internet / bad destination -> trip empty)

        # Calcul des positions GPS initiale et finale de l'utilisateur
        self.__gps_init = self.__trip_foot.steps[0][2]  # au format dict{'lat':X; 'lng':X}
        self.__gps_final = self.__trip_foot.steps[len(self.__trip_foot.steps)-1][3]  # au format dict{'lat':X; 'lng':X}

        # Calcul du trajet en Vélib (qui nécessite les coordonnées GPS calculées ci-dessus)
        self.__trip_velib = Velib(self.__user_id, init_pos_dict=self.__gps_init, final_pos_dict=self.__gps_final,
                                  init_pos_str=self.__init_pos, final_pos_str=self.__final_pos)
        self.__trip_velib.compute_itinary()

        self.__recommandation = ""
        self.analyse()

    @staticmethod
    def clean_str(chaine):
        """
         Méthode statique qui transforme une chaine de caractère avec les contraintes de l'API GoogleMaps
        """
        __new_chaine = chaine.lower().replace(" ", "+").replace(",", "+")
        pattern = r'^[0-9]+.[0-9]+%2C[0-9]+.[0-9]+$'
        if not re.match(pattern, __new_chaine):
            if "paris" not in __new_chaine:
                __new_chaine += "+paris"
        return __new_chaine

    def analyse(self):
        """
        Méthode qui calcule nos recommandations en fonction des paramètres du trajet
        """
        x = {"trip_bicycle": self.__trip_bicycle.total_duration, "trip_car": self.__trip_car.total_duration,
             "trip_foot": self.__trip_foot.total_duration, "trip_transit": self.__trip_transit.total_duration}
        if self.__bagage == "on":
            del x["trip_transit"]
        if self.__meteo.snow == "oui" or self.__meteo.rain > 21:
            del x["trip_walking"]
        min_time = min(y for y in x.values())

        for i, j in x.items():
            print(i, "est et vaut", j)
            if j == min_time:
                self.__recommandation = i
                break

    # Définition des getters, setters des attributs de notre classe
    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, value):
        print("You are not allowed to modify user_id by {} !".format(value))

    @property
    def init_pos(self):
        return self.__init_pos

    @init_pos.setter
    def init_pos(self, value):
        print("You are not allowed to modify init_pos by {} !".format(value))

    @property
    def final_pos(self):
        return self.__final_pos

    @final_pos.setter
    def final_pos(self, value):
        print("You are not allowed to modify final_pos by {} !".format(value))

    @property
    def gps_init(self):
        return self.__gps_init

    @gps_init.setter
    def gps_init(self, value):
        print("You are not allowed to modify gps_init by {} !".format(value))

    @property
    def gps_final(self):
        return self.__gps_final

    @gps_final.setter
    def gps_final(self, value):
        print("You are not allowed to modify gps_final by {} !".format(value))

    @property
    def trip_foot(self):
        return self.__trip_foot

    @trip_foot.setter
    def trip_foot(self, value):
        print("You are not allowed to modify trip_foot by {} !".format(value))

    @property
    def trip_bicycle(self):
        return self.__trip_bicycle

    @trip_bicycle.setter
    def trip_bicycle(self, value):
        print("You are not allowed to modify trip_bicyle by {} !".format(value))

    @property
    def trip_car(self):
        return self.__trip_car

    @trip_car.setter
    def trip_car(self, value):
        print("You are not allowed to modify trip_car by {} !".format(value))

    @property
    def trip_transit(self):
        return self.__trip_transit

    @trip_transit.setter
    def trip_transit(self, value):
        print("You are not allowed to modify trip_transit by {} !".format(value))

    @property
    def trip_velib(self):
        return self.__trip_velib

    @trip_velib.setter
    def trip_velib(self, value):
        print("You are not allowed to modify trip_velib by {} !".format(value))

    @property
    def bagage(self):
        return self.__bagage

    @bagage.setter
    def bagage(self, value):
        print("You are not allowed to modify bagage by {} !".format(value))

    @property
    def elevation(self):
        return self.__elevation

    @elevation.setter
    def elevation(self, value):
        print("You are not allowed to modify elevation by {} !".format(value))

    @property
    def meteo(self):
        return self.__meteo

    @meteo.setter
    def meteo(self, value):
        print("You are not allowed to modify meteo by {} !".format(value))

    @property
    def recommandation(self):
        return self.__recommandation

    @recommandation.setter
    def recommandation(self, value):
        print("You are not allowed to modify recommandation by {} !".format(value))

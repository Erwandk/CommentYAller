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
        self.__init_pos = self.__clean_str(init_pos)
        self.__final_pos = self.__clean_str(final_pos)
        self.__bagage = True if bagage == "on" else False
        self.__elevation = True if elevation == "on" else False
        self.__pers_bicycle = True  # if pers_bicycle == 'on' else False
        self.__pers_car = True  # if pers_car == 'on' else False
        # todo: ajouter l'option vélo personnel et voiture personnelle sur le formulaire

        self.__gps_init = dict()
        self.__gps_final = dict()
        self.__weather_ok = bool()  # True si les conditions météo sont jugées décentes, False sinon
        # self.__elevation_ok = bool() # True si l'élévation est acceptable, False sinon
        self.__recommendation = 'trip_transit'
        self.__reco_type_trip = "transit"

        # Définition des différents trajets et de la météo (1 thread = 1 appel à une API)
        # Les threads sont lancés dans la méthodes compute_trip
        self.__meteo = Meteo()
        self.__trip_foot = Foot(self.__user_id, self.__init_pos, self.__final_pos)
        self.__trip_bicycle = Bicycle(self.__user_id, self.__init_pos, self.__final_pos)
        self.__trip_car = Car(self.__user_id, self.__init_pos, self.__final_pos)
        self.__trip_transit = Transit(self.__user_id, self.__init_pos, self.__final_pos)
        self.__trip_velib = Velib(self.__user_id, init_pos_dict=self.__gps_init, final_pos_dict=self.__gps_final,
                                  init_pos_str=self.__init_pos, final_pos_str=self.__final_pos)

        # Calcul des attributs du trajet
        self.__compute_trip()

    @staticmethod
    def __clean_str(chaine):
        """
         Méthode statique qui transforme une chaîne de caractères avec les contraintes de l'API GoogleMaps
        """
        __new_chaine = chaine.lower().replace(" ", "+").replace(",", "+")
        pattern = r'^[0-9]+.[0-9]+%2C[0-9]+.[0-9]+$'
        if not re.match(pattern, __new_chaine):
            if "paris" not in __new_chaine:
                __new_chaine += "+paris"
        return __new_chaine

    def __check_weather(self):
        """
        Méthode qui vérifie les conditions météo pour proposer un trajet à vélo, à partir des critères suivants:
        Température > 8°C
        Précipitations < 21mm sur 3 heures (soit <7mm/h, seuil de pluie modérée, au delà duquel la pluie est forte)
        Précipitations convectives < 21mm sur 3 heures
        Risque neige = non
        :return: True si les conditions sont vérifiées, False sinon
        """
        if self.__meteo.temperature > 8 and self.__meteo.rain < 21 and self.__meteo.convective_rain < 21:
            # ajouter la condition sur le risque de neige
            return True
        else:
            return False

    # def __check_elevation(self):
    #     """
    #     Méthode qui vérifie si le dénivelé est acceptable pour proposer un trajet en vélo selon les critères suivants:
    #     Si l'utilisateur souhaite prendre en compte le dénivéle, au delà de 80m de dénivelé positif le vélo n'est pas
    #     recommandé.
    #     Si l'utilisateur ne souhaite pas prendre en compte le dénivelé, il n'y a pas de limite.
    #     :return: True si les conditions sont vérifiées, False sinon
    #     """
    #     if self.__elevation:
    #         # todo : récupérer le dénivelé dans une autre API MAps
    #         # if XXX return True else False
    #     else:
    #         return True

    def __compute_recommendation(self):
        """
        Méthode qui calcule nos recommandations en fonction des paramètres du trajet. Le trajet de référence est
        l'itinéraire en transport en commun, auquel on compare si les autres options sont mieux.
        """
        # Etude de l'itinéraire à pieds
        # Pour les distances de moins d'1km sous les bonnes conditions météo, nous recommandons un trajet à pieds
        if self.__trip_foot.total_distance < 1001 and self.__weather_ok:
            self.__recommendation = 'trip_foot'
        # Etude de l'itinéraire en vélo (ou vélib)
        # Si l'utilisateur n'est pas chargé et que les conditions météo sont bonnes, étude du trajet à vélo/vélib
        elif not self.__bagage and self.__weather_ok:  # and self.__check_elevation == True:
            # Vérification du trajet en vélo perso
            if self.__pers_bicycle and self.__trip_bicycle.total_duration < self.__trip_transit.total_duration:
                self.__recommendation = 'trip_bicycle'
            # Vérification du trajet en vélib
            elif not self.__pers_bicycle and self.__trip_velib.total_duration < self.__trip_transit.total_duration:
                self.__recommendation = 'trip_velib'
        elif self.__pers_car and self.__trip_car.total_duration < 0.66*self.__trip_transit.total_duration:
            self.__recommendation = 'trip_car'
        else:  # Dans tous les autres cas, privilégier les transports en communs
            self.__recommendation = 'trip_transit'
        print("self.recommendation:{}".format(self.recommendation))
        return

    def __compute_trip(self):
        """
        Méthode qui calcule tous les attributs du trajet.
        :return:
        """
        # Lancement des threads d'appel aux API
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

        # Vérification du bon calcul des itinéraires: en cas de bug, lever une exception
        if not self.__trip_foot.steps or not self.__trip_bicycle.steps or not self.__trip_car.steps \
                or not self.__trip_transit.steps:
            raise ValueError("Les itinéraires n'ont pas pu être calculés: problème de connexion internet ou d'adresses "
                             "mal saisies")

        # Calcul des positions GPS initiale et finale de l'utilisateur
        self.__gps_init = self.__trip_foot.steps[0][2]  # au format dict{'lat':X; 'lng':X}
        self.__gps_final = self.__trip_foot.steps[len(self.__trip_foot.steps)-1][3]  # au format dict{'lat':X; 'lng':X}

        # Calcul de l'itinéraire Vélib (lancé après les autres itis car nécessite le calcul des coord GPS ci-dessus)
        self.__trip_velib.init_pos_dict = self.__gps_init
        self.__trip_velib.dep_station.gps_position = self.__gps_init
        self.__trip_velib.final_pos_dict = self.__gps_final
        self.__trip_velib.arr_station.gps_position = self.__gps_final
        self.__trip_velib.compute_itinary()

        # Vérification du bon calcul de l'itinéraire : en cas de bug, lever une exception
        if not self.__trip_velib.steps:
            raise ValueError("Les itinéraires n'ont pas pu être calculés: problème de connexion internet ou d'adresses "
                             "mal saisies")

        # Calcul de la recommandation d'itinéraire
        self.__weather_ok = self.__check_weather()
        # self.__check_elevation
        self.__compute_recommendation()

    # Définition des getters, setters des attributs de notre classe
    # TODO : Vérifier la liste des getters et setters (complète pour tous les attributs de la classe?)
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
    def check_weather(self):
        return self.__check_weather

    @property
    def reco_type_trip(self):
        return self.__reco_type_trip

    @reco_type_trip.setter
    def reco_type_trip(self, value):
        print("You are not allowed to modify reco_type_trip by {} !".format(value))

    @check_weather.setter
    def check_weather(self, value):
        print("You are not allowed to modify check_weather by {} !".format(value))

    @property
    def recommendation(self):
        return self.__recommendation

    @recommendation.setter
    def recommendation(self, value):
        print("You are not allowed to modify recommendation by {} !".format(value))


if __name__ == '__main__':

    def main():
        init_pos = '6+rue+des+marronniers+paris'
        final_pos = '8+rue+des+morillons+paris'
        bagage = 'off'
        elevation = 'off'
        # pers_bicycle = 'on'
        # pers_car = 'on'
        test = Trip(init_pos, final_pos, bagage, elevation, user_id=0)
        print(test.check_weather)
        print(test.recommendation)

    main()

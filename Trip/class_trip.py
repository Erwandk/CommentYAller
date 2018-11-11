#!usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'eke, gab, axel'

# Importation des données utiles du projet et des librairies
from Trip.class_itinary import Foot, Bicycle, Car, Transit, Velib
from APIs.class_meteo import Meteo
import re


class Trip:
    """
    Cette classe représente le trajet dans son ensemble avec toutes les données correspondantes.
    """

    def __init__(self, init_pos, final_pos, bagage, elevation, pers_bicycle, pers_car, user_id=0):
        """
        :param init_pos: point de départ de l'utilisateur (str)
        :param final_pos: point d'arrivée de l'utilisateur (str)
        :param bagage: option 'bagage' du formulaire de la page principale (str)
        :param elevation: option 'dénivelé' du formulaire de la page principale (str)
        :param pers_bicycle: option 'vélo personnel' du formulaire de la page principale (str)
        :param pers_car: option 'voiture personnelle' du formulaire de la page principale (str)
        :param user_id: id du user (int)
        """
        assert isinstance(init_pos, str) and isinstance(final_pos, str) and isinstance(bagage, str)
        assert isinstance(elevation, str) and isinstance(pers_bicycle, str) and isinstance(pers_car, str)
        assert isinstance(user_id, int)

        # Définitions des attributs de la classe
        self.__user_id = user_id
        self.__init_pos = self.__clean_str(init_pos)  # au format 'latitude'+'%2C'+'longitude' ou 'adresse'+'paris'
        self.__final_pos = self.__clean_str(final_pos)  # au format 'latitude'+'%2C'+'longitude' ou 'adresse'+'paris'
        self.__bagage = True if bagage == "on" else False
        self.__elevation = True if elevation == "on" else False
        self.__pers_bicycle = True if pers_bicycle == 'on' else False
        self.__pers_car = True if pers_car == 'on' else False

        self.__gps_init = dict()
        self.__gps_final = dict()
        self.__weather_ok = bool()  # True si les conditions météo sont jugées décentes, False sinon
        self.__elevation_bicycle_ok = True  # True si l'élévation est acceptable, False sinon
        self.__elevation_velib_ok = True  # True si l'élévation est acceptable, False sinon
        self.__recommendation = str()
        self.__reco_type_trip = "transit"

        # Définition des différents trajets, de leur dénivelé, et de la météo (1 thread = 1 appel à une API)
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
        __new_chaine = '+'.join(chaine.lower().replace(',', '').split())
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
        if self.__meteo.temperature > 8 and self.__meteo.rain < 21 and self.__meteo.convective_rain < 21 \
                and self.__meteo.snow == 'non':
            self.__weather_ok = True
        else:
            self.__weather_ok = False

    def __check_elevation(self):
        """
        Méthode qui vérifie si le dénivelé est acceptable pour proposer un trajet en vélo selon les critères suivants:
        Si l'utilisateur souhaite prendre en compte le dénivéle, au delà de 80m de dénivelé positif le vélo n'est pas
        recommandé.
        Si l'utilisateur ne souhaite pas prendre en compte le dénivelé, il n'y a pas de limite.
        :return: True si les conditions sont vérifiées, False sinon
        """
        if self.__elevation and self.__trip_bicycle.elevation.asc_elevation > 80:
            self.__elevation_bicycle_ok = False
        if self.__elevation and self.__trip_velib.elevation.asc_elevation > 80:
            self.__elevation_velib_ok = False

    def __compute_recommendation(self):
        """
        Méthode qui calcule nos recommandations en fonction des paramètres du trajet. Le trajet de référence est
        l'itinéraire en transport en commun, auquel on compare si les autres options sont mieux.
        """
        # Etude du trajet à pieds
        if self.__trip_foot.total_distance < 1001 and self.__weather_ok:
            self.__reco_type_trip = 'foot'
            self.__recommendation = "Nous vous recommandons de vous rendre à destination à pieds, compte tenu de la "\
                                    "météo clémente et de la distance à parcourir."
        # Etude du trajet en voiture si aucune recommandation n'a été trouvée précédemment
        if not self.__recommendation and self.__pers_car and self.__bagage:  # Cas avec bagage
            self.__reco_type_trip = 'car'
            self.__recommendation = "Nous vous recommandons de vous rendre à destination avec votre voiture " \
                                    "personnelle, compte tenu de vos bagages."
        if not self.__recommendation and self.__pers_car and \
                self.__trip_car.total_duration < 0.66*self.__trip_transit.total_duration and \
                self.__trip_car.total_duration < 0.66*self.__trip_velib.total_duration and \
                (not self.__pers_bicycle or self.__trip_car.total_duration < 0.66*self.__trip_bicycle.total_duration):
            self.__reco_type_trip = 'car'
            self.__recommendation = "Nous vous recommandons de vous rendre à destination avec votre voiture " \
                                    "personnelle, compte tenu du gain de temps considérable par rapport aux autres"\
                                    " moyens de transport."
        # Etude du trajet en vélo (ou vélib) si aucune recommandation n'a été précédemment trouvée
        if not self.__recommendation and not self.__bagage and self.__weather_ok:
            # Vérification du trajet en vélo perso
            if self.__pers_bicycle and self.__trip_bicycle.total_duration < self.__trip_transit.total_duration and \
                    self.__elevation_bicycle_ok:
                self.__reco_type_trip = 'bicycle'
                self.__recommendation = "Nous vous recommandons de vous rendre à destination avec votre vélo personnel"\
                                        ", compte tenu de la météo clémente, du dénivelé acceptable et du gain de " \
                                        "temps par rapport aux transports en commun."
            # Vérification du trajet en vélib
            elif not self.__pers_bicycle and self.__trip_velib.total_duration < self.__trip_transit.total_duration and \
                    self.__elevation_velib_ok:
                self.__reco_type_trip = 'velib'
                self.__recommendation = "Nous vous recommandons de vous rendre à destination en Vélib', compte tenu de"\
                                        " la météo clémente, du dénivelé acceptable, de la disponibilité des " \
                                        "stations à proximité de vos points de départ et d'arrivée et du gain de temps"\
                                        " par rapport aux transports en commun."
        # Si aucune recommandation n'a été précédemment trouvée, choisir les transports en commun
        if not self.__recommendation:
            self.__reco_type_trip = 'transit'
            self.__recommendation = "Nous vous recommandons de vous rendre à destination en transport en commun. " \
                                    "Malheureusement, le temps de trajet, la météo, le dénivelé ou vos bagages ne " \
                                    "vous encouragent pas à prendre le vélo, et si vous disposez d'une voiture person" \
                                    "nelle, celle-ci ne vous permettra pas un gain de temps de trajet considérable."
        return

    def __compute_trip(self):
        """
        Méthode qui calcule tous les attributs du trajet.
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
        self.__check_weather()
        self.__check_elevation()
        self.__compute_recommendation()

    # Définition des getters, setters des attributs de notre classe
    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, value):
        raise AttributeError("You are not allowed to modify user_id by {} !".format(value))

    @property
    def init_pos(self):
        return self.__init_pos

    @init_pos.setter
    def init_pos(self, value):
        raise AttributeError("You are not allowed to modify init_pos by {} !".format(value))

    @property
    def final_pos(self):
        return self.__final_pos

    @final_pos.setter
    def final_pos(self, value):
        raise AttributeError("You are not allowed to modify final_pos by {} !".format(value))

    @property
    def gps_init(self):
        return self.__gps_init

    @gps_init.setter
    def gps_init(self, value):
        raise AttributeError("You are not allowed to modify gps_init by {} !".format(value))

    @property
    def gps_final(self):
        return self.__gps_final

    @gps_final.setter
    def gps_final(self, value):
        raise AttributeError("You are not allowed to modify gps_final by {} !".format(value))

    @property
    def trip_foot(self):
        return self.__trip_foot

    @trip_foot.setter
    def trip_foot(self, value):
        raise AttributeError("You are not allowed to modify trip_foot by {} !".format(value))

    @property
    def trip_bicycle(self):
        return self.__trip_bicycle

    @trip_bicycle.setter
    def trip_bicycle(self, value):
        raise AttributeError("You are not allowed to modify trip_bicyle by {} !".format(value))

    @property
    def trip_car(self):
        return self.__trip_car

    @trip_car.setter
    def trip_car(self, value):
        raise AttributeError("You are not allowed to modify trip_car by {} !".format(value))

    @property
    def trip_transit(self):
        return self.__trip_transit

    @trip_transit.setter
    def trip_transit(self, value):
        raise AttributeError("You are not allowed to modify trip_transit by {} !".format(value))

    @property
    def trip_velib(self):
        return self.__trip_velib

    @trip_velib.setter
    def trip_velib(self, value):
        raise AttributeError("You are not allowed to modify trip_velib by {} !".format(value))

    @property
    def bagage(self):
        return self.__bagage

    @bagage.setter
    def bagage(self, value):
        raise AttributeError("You are not allowed to modify bagage by {} !".format(value))

    @property
    def elevation(self):
        return self.__elevation

    @elevation.setter
    def elevation(self, value):
        raise AttributeError("You are not allowed to modify elevation by {} !".format(value))

    @property
    def pers_bicycle(self):
        return self.__pers_bicycle

    @pers_bicycle.setter
    def pers_bicycle(self, value):
        raise AttributeError("You are not allowed to modify pers_bicycle by {} !".format(value))

    @property
    def pers_car(self):
        return self.__pers_car

    @pers_car.setter
    def pers_car(self, value):
        raise AttributeError("You are not allowed to modify pers_car by {} !".format(value))

    @property
    def meteo(self):
        return self.__meteo

    @meteo.setter
    def meteo(self, value):
        raise AttributeError("You are not allowed to modify meteo by {} !".format(value))

    @property
    def weather_ok(self):
        return self.__weather_ok

    @weather_ok.setter
    def weather_ok(self, value):
        raise AttributeError("You are not allowed to modify weather_ok by {} !".format(value))

    @property
    def elevation_bicycle_ok(self):
        return self.__elevation_bicycle_ok

    @elevation_bicycle_ok.setter
    def elevation_bicycle_ok(self, value):
        raise AttributeError("You are not allowed to modify elevation_bicycle_ok by {} !".format(value))

    @property
    def elevation_velib_ok(self):
        return self.__elevation_velib_ok

    @elevation_velib_ok.setter
    def elevation_velib_ok(self, value):
        raise AttributeError("You are not allowed to modify elevation_velib_ok by {} !".format(value))

    @property
    def reco_type_trip(self):
        return self.__reco_type_trip

    @reco_type_trip.setter
    def reco_type_trip(self, value):
        raise AttributeError("You are not allowed to modify reco_type_trip by {} !".format(value))

    @property
    def recommendation(self):
        return self.__recommendation

    @recommendation.setter
    def recommendation(self, value):
        raise AttributeError("You are not allowed to modify recommendation by {} !".format(value))

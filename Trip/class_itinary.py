#!usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'eke, gab, axel'

# Importation des librairies utiles
from threading import Thread
import re

# Importation des données utiles du projet
from APIs.class_googlesmaps import GoogleMaps, GoogleMapsTransit
from APIs.class_velib_station import VelibStation
from APIs.class_googlemaps_elevation import Elevation


class Foot(Thread):
    """
    Classe représentant le trajet à pied
    """

    def __init__(self, user_id, init_pos, final_pos):
        """
        :param user_id: id du user (int)
        :param init_pos: point de départ du user (str)
        :param final_pos: point d'arrivée du user (str)
        """
        assert isinstance(user_id, int) and isinstance(init_pos, str) and isinstance(final_pos, str)
        Thread.__init__(self)
        self.__user_id = user_id
        self.__init_pos = init_pos
        self.__final_pos = final_pos

        self.__steps = []
        self.__total_duration = 0
        self.__total_distance = 0

    def run(self):
        """
        Fonction lancée à l'execution du thread qui permet d'initier l'obtention des informations pour la classe
        """
        self.__steps = GoogleMaps(user_id=self.__user_id, startcoord=self.__init_pos, endcoord=self.__final_pos,
                                  driving_mode="walking", transit_mode="").get_etape()
        self.__compute_total_duration()
        self.__compute_total_distance()

    def __compute_total_distance(self):
        """
        Calcul de la distance totale
        """
        for step in self.__steps:
            self.__total_distance += step[0]

    def __compute_total_duration(self):
        """
        Calcul de la durée totale
        """
        for step in self.__steps:
            self.__total_duration += step[1]

    # Définition des getters et setters de la classe
    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, value):
        raise AttributeError("You are not allowed to modify user_id by {}".format(value))

    @property
    def init_pos(self):
        return self.__init_pos

    @init_pos.setter
    def init_pos(self, value):
        pattern = r'^[0-9]+.[0-9]+%2C[0-9]+.[0-9]+$'
        if not re.match(pattern, value):
            raise ValueError("La valeur de init_pos indiquée n'est pas au format 'latitude'+'%2C'+'longitude.")
        self.__init_pos = value

    @property
    def final_pos(self):
        return self.__final_pos

    @final_pos.setter
    def final_pos(self, value):
        pattern = r'^[0-9]+.[0-9]+%2C[0-9]+.[0-9]+$'
        if not re.match(pattern, value):
            raise ValueError("La valeur de final_pos indiquée n'est pas au format 'latitude'+'%2C'+'longitude.")
        self.__final_pos = value

    @property
    def total_duration(self):
        return self.__total_duration

    @total_duration.setter
    def total_duration(self, value):
        raise AttributeError("You are not allowed to modify total_duration by {}".format(value))

    @property
    def total_distance(self):
        return self.__total_distance

    @total_distance.setter
    def total_distance(self, value):
        raise AttributeError("You are not allowed to modify total_distance by {}".format(value))

    @property
    def steps(self):
        return self.__steps

    @steps.setter
    def steps(self, value):
        raise AttributeError("You are not allowed to modify steps by {}".format(value))


class Bicycle(Thread):
    """
    Classe représentant le trajet en vélo
    """

    def __init__(self, user_id, init_pos, final_pos):
        """
        :param user_id: id du user (int)
        :param init_pos: point de départ du user (str)
        :param final_pos: point d'arrivée du user (str)
        """
        assert isinstance(user_id, int) and isinstance(init_pos, str) and isinstance(final_pos, str)
        Thread.__init__(self)
        self.__user_id = user_id
        self.__init_pos = init_pos
        self.__final_pos = final_pos

        self.__steps = []
        self.__total_duration = 0
        self.__total_distance = 0
        self.__elevation = Elevation(self.__steps)  # Dénivelé

    def run(self):
        """
        Fonction lancée à l'execution du thread qui permet d'initier l'obtention des informations pour la classe
        """
        self.__steps = GoogleMaps(user_id=self.__user_id, startcoord=self.__init_pos, endcoord=self.__final_pos,
                                  driving_mode="bicycling", transit_mode="").get_etape()
        self.__compute_total_duration()
        self.__compute_total_distance()
        self.__elevation.steps = self.__steps
        self.__elevation.compute_elevation()

    def __compute_total_distance(self):
        """
        Calcul de la distance totale
        """
        for step in self.__steps:
            self.__total_distance += step[0]

    def __compute_total_duration(self):
        """
        Calcul de la durée totale
        """
        for step in self.__steps:
            self.__total_duration += step[1]

    # Définition des getters et setters de la classe
    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, value):
        raise AttributeError("You are not allowed to modify user_id by {}".format(value))

    @property
    def init_pos(self):
        return self.__init_pos

    @init_pos.setter
    def init_pos(self, value):
        pattern = r'^[0-9]+.[0-9]+%2C[0-9]+.[0-9]+$'
        if not re.match(pattern, value):
            raise ValueError("La valeur de init_pos indiquée n'est pas au format 'latitude'+'%2C'+'longitude.")
        self.__init_pos = value

    @property
    def final_pos(self):
        return self.__final_pos

    @final_pos.setter
    def final_pos(self, value):
        pattern = r'^[0-9]+.[0-9]+%2C[0-9]+.[0-9]+$'
        if not re.match(pattern, value):
            raise ValueError("La valeur de final_pos indiquée n'est pas au format 'latitude'+'%2C'+'longitude.")
        self.__final_pos = value

    @property
    def total_duration(self):
        return self.__total_duration

    @total_duration.setter
    def total_duration(self, value):
        raise AttributeError("You are not allowed to modify total_duration by {}".format(value))

    @property
    def total_distance(self):
        return self.__total_distance

    @total_distance.setter
    def total_distance(self, value):
        raise AttributeError("You are not allowed to modify total_distance by {}".format(value))

    @property
    def steps(self):
        return self.__steps

    @steps.setter
    def steps(self, value):
        raise AttributeError("You are not allowed to modify steps by {}".format(value))

    @property
    def elevation(self):
        return self.__elevation

    @elevation.setter
    def elevation(self, value):
        raise AttributeError("You are not allowed to modify elevation by {}".format(value))


class Car(Thread):
    """
    Classe représentant le trajet en voiture
    """

    def __init__(self, user_id, init_pos, final_pos):
        """
        :param user_id: id du user (int)
        :param init_pos: point de départ du user (str)
        :param final_pos: point d'arrivée du user (str)
        """
        assert isinstance(user_id, int) and isinstance(init_pos, str) and isinstance(final_pos, str)
        Thread.__init__(self)
        self.__user_id = user_id
        self.__init_pos = init_pos
        self.__final_pos = final_pos

        self.__steps = []
        self.__total_duration = 0
        self.__total_distance = 0

    def run(self):
        """
        Fonction lancée à l'execution du thread qui permet d'initier l'obtention des informations pour la classe
        """
        self.__steps = GoogleMaps(user_id=self.__user_id, startcoord=self.__init_pos, endcoord=self.__final_pos,
                                  driving_mode="driving", transit_mode="").get_etape()
        self.__compute_total_duration()
        self.__compute_total_distance()

    def __compute_total_distance(self):
        """
        Calcul de la distance totale
        """
        for step in self.__steps:
            self.__total_distance += step[0]

    def __compute_total_duration(self):
        """
        Calcul de la durée totale
        """
        for step in self.__steps:
            self.__total_duration += step[1]

    # Définition des getters et setters de la classe
    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, value):
        raise AttributeError("You are not allowed to modify user_id by {}".format(value))

    @property
    def init_pos(self):
        return self.__init_pos

    @init_pos.setter
    def init_pos(self, value):
        pattern = r'^[0-9]+.[0-9]+%2C[0-9]+.[0-9]+$'
        if not re.match(pattern, value):
            raise ValueError("La valeur de init_pos indiquée n'est pas au format 'latitude'+'%2C'+'longitude.")
        self.__init_pos = value

    @property
    def final_pos(self):
        return self.__final_pos

    @final_pos.setter
    def final_pos(self, value):
        pattern = r'^[0-9]+.[0-9]+%2C[0-9]+.[0-9]+$'
        if not re.match(pattern, value):
            raise ValueError("La valeur de final_pos indiquée n'est pas au format 'latitude'+'%2C'+'longitude.")
        self.__final_pos = value

    @property
    def total_duration(self):
        return self.__total_duration

    @total_duration.setter
    def total_duration(self, value):
        raise AttributeError("You are not allowed to modify total_duration by {}".format(value))

    @property
    def total_distance(self):
        return self.__total_distance

    @total_distance.setter
    def total_distance(self, value):
        raise AttributeError("You are not allowed to modify total_distance by {}".format(value))

    @property
    def steps(self):
        return self.__steps

    @steps.setter
    def steps(self, value):
        raise AttributeError("You are not allowed to modify steps by {}".format(value))


class Transit(Thread):
    """
    Classe représentant le trajet en transport en commun
    """

    def __init__(self, user_id, init_pos, final_pos):
        """
        :param user_id: id du user (int)
        :param init_pos: point de départ du user (str)
        :param final_pos: point d'arrivée du user (str)
        """
        assert isinstance(user_id, int) and isinstance(init_pos, str) and isinstance(final_pos, str)
        Thread.__init__(self)
        self.__user_id = user_id
        self.__init_pos = init_pos
        self.__final_pos = final_pos

        self.__steps = []
        self.__distinct_steps = [[]]
        self.__total_duration = 0
        self.__total_distance = 0
        self.__steps_nbr = 1

    def run(self):
        """
        Fonction lancée à l'execution du thread qui permet d'initier l'obtention des informations pour la classe
        """
        self.__steps = GoogleMapsTransit(user_id=self.__user_id, startcoord=self.__init_pos, endcoord=self.__final_pos,
                                         driving_mode="transit", transit_mode="").get_etape()
        self.__compute_distinct_steps()
        self.__compute_total_duration()
        self.__compute_total_distance()
        self.__steps_nbr = len(self.__distinct_steps)

    def __compute_total_distance(self):
        """
        Calcul de la distance totale
        """
        for step in self.__steps:
            self.__total_distance += step[0]

    def __compute_total_duration(self):
        """
        Calcul de la durée totale
        """
        for step in self.__steps:
            self.__total_duration += step[1]

    def __compute_distinct_steps(self):
        """
        Calcul de la distance et durée pour chacun des différents mode de transport du trajet transit
        """
        n = len(self.__steps)
        self.__distinct_steps[0].append(self.__steps[0])
        __duration = self.__steps[0][1]
        __distance = self.__steps[0][0]
        for x in range(1, n):
            if self.__steps[x][4] != self.__steps[x-1][4] or self.__steps[x][5] != self.__steps[x-1][5]:
                self.__distinct_steps[-1].append((__distance, __duration))
                self.__distinct_steps.append([self.__steps[x]])
                __distance = self.__steps[x][0]
                __duration = self.__steps[x][1]
            else:
                self.__distinct_steps[-1].append(self.__steps[x])
                __distance += self.__steps[x][0]
                __duration += self.__steps[x][1]
        self.__distinct_steps[-1].append((__distance, __duration))

    # Définition des getters et des setters de la classe
    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, value):
        raise AttributeError("You are not allowed to modify user_id by {}".format(value))

    @property
    def init_pos(self):
        return self.__init_pos

    @init_pos.setter
    def init_pos(self, value):
        pattern = r'^[0-9]+.[0-9]+%2C[0-9]+.[0-9]+$'
        if not re.match(pattern, value):
            raise ValueError("La valeur de init_pos indiquée n'est pas au format 'latitude'+'%2C'+'longitude.")
        self.__init_pos = value

    @property
    def final_pos(self):
        return self.__final_pos

    @final_pos.setter
    def final_pos(self, value):
        pattern = r'^[0-9]+.[0-9]+%2C[0-9]+.[0-9]+$'
        if not re.match(pattern, value):
            raise ValueError("La valeur de final_pos indiquée n'est pas au format 'latitude'+'%2C'+'longitude.")
        self.__final_pos = value

    @property
    def total_duration(self):
        return self.__total_duration

    @total_duration.setter
    def total_duration(self, value):
        raise AttributeError("You are not allowed to modify total_duration by {}".format(value))

    @property
    def total_distance(self):
        return self.__total_distance

    @total_distance.setter
    def total_distance(self, value):
        raise AttributeError("You are not allowed to modify total_distance by {}".format(value))

    @property
    def steps_nbr(self):
        return self.__steps_nbr

    @steps_nbr.setter
    def steps_nbr(self, value):
        raise AttributeError("You are not allowed to modify steps_nbr by {}".format(value))

    @property
    def steps(self):
        return self.__steps

    @steps.setter
    def steps(self, value):
        raise AttributeError("You are not allowed to modify steps by {}".format(value))

    @property
    def distinct_steps(self):
        return self.__distinct_steps

    @distinct_steps.setter
    def distinct_steps(self, value):
        raise AttributeError("You are not allowed to modify distinct_steps by {}".format(value))


class Velib:
    """
    Classe représentant le trajet en Vélib
    """

    def __init__(self, user_id, init_pos_dict, final_pos_dict, init_pos_str, final_pos_str):
        """
        :param user_id: id du user (int)
        :param init_pos_dict: point de départ du user (dict)
        :param final_pos_dict: point d'arrivée du user (dict)
        :param init_pos_str: point de départ du user (str)
        :param final_pos_str: point d'arrivée du user (str)
        """
        assert isinstance(user_id, int) and isinstance(init_pos_str, str) and isinstance(final_pos_str, str)
        assert isinstance(init_pos_dict, dict) and isinstance(final_pos_dict, dict)
        self.__user_id = user_id
        self.__init_pos_dict = init_pos_dict  # Coord GPS au format dict{'lat':XXX; 'lng':XXX} pour l'API Vélib
        self.__final_pos_dict = final_pos_dict  # Coord GPS au format dict{'lat':XXX; 'lng':XXX} pour l'API Vélib
        self.__init_pos_str = init_pos_str  # Coord GPS au format 'latitude'+'2%C'+'longitude' pour l'API GoogleMaps
        self.__final_pos_str = final_pos_str  # Coord GPS au format 'latitude'+'2%C'+'longitude' pour l'API GoogleMaps

        self.__dep_station = VelibStation(gps_position=self.__init_pos_dict, station_type='departure')
        # Station de départ
        self.__arr_station = VelibStation(gps_position=self.__final_pos_dict, station_type='arrival')
        # Station d'arrivée

        self.__steps = []
        self.__distinct_steps = [[]]
        self.__total_duration = 0
        self.__total_distance = 0

        # Itinéraire à pieds depuis le point initial jusqu'à la station Vélib de départ
        self.__initial_walking = Foot(user_id=self.user_id, init_pos=self.__init_pos_str,
                                      final_pos=self.__dep_station.coord)
        # Itinéraire en vélo entre les 2 stations Vélib
        self.__bicycling = Bicycle(user_id=self.user_id, init_pos=self.__dep_station.coord,
                                   final_pos=self.__arr_station.coord)
        # Itinéraire à pieds depuis la station Vélib d'arrivée jusqu'à la destination finale
        self.__final_walking = Foot(user_id=self.user_id, init_pos=self.__arr_station.coord,
                                    final_pos=self.__final_pos_str)

        self.__elevation = Elevation(self.__bicycling.steps)  # Dénivelé

    def compute_itinary(self):
        # Lancement des threads de l'API Vélib
        self.__dep_station.start()
        self.__arr_station.start()

        # Attente de la fin des threads
        self.__dep_station.join()
        self.__arr_station.join()

        # Prise en compte des coordonnées des stations Vélib trouvées pour le calcul d'itinéraire avec GoogleMaps
        self.__initial_walking.final_pos = self.__dep_station.coord
        self.__bicycling.init_pos = self.__dep_station.coord
        self.__bicycling.final_pos = self.__arr_station.coord
        self.final_walking.init_pos = self.__arr_station.coord

        # Lancement des threads de l'API GoogleMaps
        self.__initial_walking.start()
        self.__bicycling.start()
        self.__final_walking.start()

        # Attente de la fin des threads
        self.__initial_walking.join()
        self.__bicycling.join()
        self.__final_walking.join()

        # Calcul des caractéristiques de l'itinéraire (étapes, distance, durée, dénivelé)
        self.__steps = self.__initial_walking.steps + self.__bicycling.steps + self.__final_walking.steps
        self.__compute_total_duration()
        self.__compute_total_distance()
        self.__compute_distinct_steps()
        self.__elevation.steps = self.__bicycling.steps  # MAJ de la liste d'étapes qui vient d'être calculée
        self.__elevation.compute_elevation()

    def __compute_total_distance(self):
        for step in self.__steps:
            self.__total_distance += step[0]

    def __compute_total_duration(self):
        for step in self.__steps:
            self.__total_duration += step[1]

    def __compute_distinct_steps(self):
        n = len(self.__steps)
        self.__distinct_steps[0].append(self.__steps[0])
        __duration = self.__steps[0][1]
        __distance = self.__steps[0][0]
        for x in range(1, n):
            if self.__steps[x][4] != self.__steps[x-1][4]:
                self.__distinct_steps[-1].append((__distance, __duration))
                self.__distinct_steps.append([self.__steps[x]])
                __distance = self.__steps[x][0]
                __duration = self.__steps[x][1]
            else:
                self.__distinct_steps[-1].append(self.__steps[x])
                __distance += self.__steps[x][0]
                __duration += self.__steps[x][1]
        self.__distinct_steps[-1].append((__distance, __duration))

    # Définition des getters et setters de la classe
    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, value):
        raise AttributeError("You are not allowed to modify user_id by {}".format(value))

    @property
    def init_pos_dict(self):
        return self.__init_pos_dict

    @init_pos_dict.setter
    def init_pos_dict(self, value):
        if type(value) is not dict or 'lat' not in value.keys() or 'lng' not in value.keys():
            raise ValueError("La valeur de init_pos_dict indiquée n'est pas au format {'lat':..., 'lng':...}.")
        self.__init_pos_dict = value
        return

    @property
    def final_pos_dict(self):
        return self.__final_pos_dict

    @final_pos_dict.setter
    def final_pos_dict(self, value):
        if type(value) is not dict or 'lat' not in value.keys() or 'lng' not in value.keys():
            raise ValueError("La valeur de final_pos_dict indiquée n'est pas au format {'lat':..., 'lng':...}.")
        self.__final_pos_dict = value
        return

    @property
    def init_pos_str(self):
        return self.__init_pos_str

    @init_pos_str.setter
    def init_pos_str(self, value):
        raise AttributeError("You are not allowed to modify init_pos_str by {}".format(value))

    @property
    def final_pos_str(self):
        return self.__final_pos_str

    @final_pos_str.setter
    def final_pos_str(self, value):
        raise AttributeError("You are not allowed to modify final_pos_str by {}".format(value))

    @property
    def dep_station(self):
        return self.__dep_station

    @dep_station.setter
    def dep_station(self, value):
        raise AttributeError("You are not allowed to modify dep_station by {}".format(value))

    @property
    def arr_station(self):
        return self.__arr_station

    @arr_station.setter
    def arr_station(self, value):
        raise AttributeError("You are not allowed to modify arr_station by {}".format(value))

    @property
    def total_duration(self):
        return self.__total_duration

    @total_duration.setter
    def total_duration(self, value):
        raise AttributeError("You are not allowed to modify total_duration by {}".format(value))

    @property
    def total_distance(self):
        return self.__total_distance

    @total_distance.setter
    def total_distance(self, value):
        raise AttributeError("You are not allowed to modify total_distance by {}".format(value))

    @property
    def steps(self):
        return self.__steps

    @steps.setter
    def steps(self, value):
        raise AttributeError("You are not allowed to modify steps by {}".format(value))

    @property
    def initial_walking(self):
        return self.__initial_walking

    @initial_walking.setter
    def initial_walking(self, value):
        raise AttributeError("You are not allowed to modify initial_walking by {}".format(value))

    @property
    def bicycling(self):
        return self.__bicycling

    @bicycling.setter
    def bicycling(self, value):
        raise AttributeError("You are not allowed to modify bicycling by {}".format(value))

    @property
    def final_walking(self):
        return self.__final_walking

    @final_walking.setter
    def final_walking(self, value):
        raise AttributeError("You are not allowed to modify final_walking by {}".format(value))

    @property
    def distinct_steps(self):
        return self.__distinct_steps

    @distinct_steps.setter
    def distinct_steps(self, value):
        raise AttributeError("You are not allowed to modify distinct_steps by {}".format(value))

    @property
    def elevation(self):
        return self.__elevation

    @elevation.setter
    def elevation(self, value):
        raise AttributeError("You are not allowed to modify elevation by {}".format(value))

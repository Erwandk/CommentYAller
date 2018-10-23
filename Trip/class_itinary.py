#!usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'eke, gab, axel'

from APIs.class_googlesmaps import GoogleMaps, GoogleMapsTransit
from threading import Thread


class Foot(Thread):

    def __init__(self, user_id, pos_init, pos_final):
        Thread.__init__(self)
        self.__user_id = user_id
        self.__pos_init = pos_init
        self.__pos_final = pos_final

        self.__etapes = []
        self.__duree_tot = 0
        self.__distance_tot = 0

    def run(self):
        print("Foot is running as one thread")
        self.__etapes = GoogleMaps(user_id=self.__user_id, startcoord=self.__pos_init, endcoord=self.__pos_final,
                                   driving_mode="walking", transit_mode="",
                                   waypoints="").get_etape()
        self.__compute_duree_tot()
        self.__compute_distance_tot()

    def __compute_distance_tot(self):
        for step in self.etapes:
            self.__distance_tot += step[0]

    def __compute_duree_tot(self):
        for step in self.etapes:
            self.__duree_tot += step[1]

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, valeur):
        print("You are not allowed to modify user_id by {}".format(valeur))

    @property
    def pos_init(self):
        return self.__pos_init

    @pos_init.setter
    def pos_init(self, valeur):
        print("You are not allowed to modify pos_init by {}".format(valeur))

    @property
    def pos_final(self):
        return self.__pos_final

    @pos_final.setter
    def pos_final(self, valeur):
        print("You are not allowed to modify pos_final by {}".format(valeur))

    @property
    def duree_tot(self):
        return self.__duree_tot

    @duree_tot.setter
    def duree_tot(self, valeur):
        print("You are not allowed to modify duree_tot by {}".format(valeur))

    @property
    def distance_tot(self):
        return self.__distance_tot

    @distance_tot.setter
    def distance_tot(self, valeur):
        print("You are not allowed to modify distance_tot by {}".format(valeur))

    @property
    def etapes(self):
        return self.__etapes

    @etapes.setter
    def etapes(self, valeur):
        print("You are not allowed to modify etapes by {}".format(valeur))


class Bicycle(Thread):

    def __init__(self, user_id, pos_init, pos_final):
        Thread.__init__(self)
        self.__user_id = user_id
        self.__pos_init = pos_init
        self.__pos_final = pos_final

        self.__etapes = []
        self.__duree_tot = 0
        self.__distance_tot = 0

    def run(self):
        print("Bicycle is running as one thread")
        self.__etapes = GoogleMaps(user_id=self.__user_id, startcoord=self.__pos_init, endcoord=self.__pos_final,
                                   driving_mode="bicycling", transit_mode="",
                                   waypoints="").get_etape()
        self.__compute_duree_tot()
        self.__compute_distance_tot()

    def __compute_distance_tot(self):
        for step in self.etapes:
            self.__distance_tot += step[0]

    def __compute_duree_tot(self):
        for step in self.etapes:
            self.__duree_tot += step[1]

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, valeur):
        print("You are not allowed to modify user_id by {}".format(valeur))

    @property
    def pos_init(self):
        return self.__pos_init

    @pos_init.setter
    def pos_init(self, valeur):
        print("You are not allowed to modify pos_init by {}".format(valeur))

    @property
    def pos_final(self):
        return self.__pos_final

    @pos_final.setter
    def pos_final(self, valeur):
        print("You are not allowed to modify pos_final by {}".format(valeur))

    @property
    def duree_tot(self):
        return self.__duree_tot

    @duree_tot.setter
    def duree_tot(self, valeur):
        print("You are not allowed to modify duree_tot by {}".format(valeur))

    @property
    def distance_tot(self):
        return self.__distance_tot

    @distance_tot.setter
    def distance_tot(self, valeur):
        print("You are not allowed to modify distance_tot by {}".format(valeur))

    @property
    def etapes(self):
        return self.__etapes

    @etapes.setter
    def etapes(self, valeur):
        print("You are not allowed to modify etapes by {}".format(valeur))


class Car(Thread):

    def __init__(self, user_id, pos_init, pos_final):
        Thread.__init__(self)
        self.__user_id = user_id
        self.__pos_init = pos_init
        self.__pos_final = pos_final

        self.__etapes = []
        self.__duree_tot = 0
        self.__distance_tot = 0

    def run(self):
        self.__etapes = GoogleMaps(user_id=self.__user_id, startcoord=self.__pos_init, endcoord=self.__pos_final,
                                   driving_mode="driving", transit_mode="",
                                   waypoints="").get_etape()
        self.__compute_duree_tot()
        self.__compute_distance_tot()

    def __compute_distance_tot(self):
        for step in self.etapes:
            self.__distance_tot += step[0]

    def __compute_duree_tot(self):
        for step in self.etapes:
            self.__duree_tot += step[1]

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, valeur):
        print("You are not allowed to modify user_id by {}".format(valeur))

    @property
    def pos_init(self):
        return self.__pos_init

    @pos_init.setter
    def pos_init(self, valeur):
        print("You are not allowed to modify pos_init by {}".format(valeur))

    @property
    def pos_final(self):
        return self.__pos_final

    @pos_final.setter
    def pos_final(self, valeur):
        print("You are not allowed to modify pos_final by {}".format(valeur))

    @property
    def duree_tot(self):
        return self.__duree_tot

    @duree_tot.setter
    def duree_tot(self, valeur):
        print("You are not allowed to modify duree_tot by {}".format(valeur))

    @property
    def distance_tot(self):
        return self.__distance_tot

    @distance_tot.setter
    def distance_tot(self, valeur):
        print("You are not allowed to modify distance_tot by {}".format(valeur))

    @property
    def etapes(self):
        return self.__etapes

    @etapes.setter
    def etapes(self, valeur):
        print("You are not allowed to modify etapes by {}".format(valeur))


class Transit(Thread):

    def __init__(self, user_id, pos_init, pos_final):
        Thread.__init__(self)
        self.__user_id = user_id
        self.__pos_init = pos_init
        self.__pos_final = pos_final
        self.__etapes = []

        self.__distance_tot = 0
        self.__duree_tot = 0
        self.__nb_etapes = 1

    def run(self):
        self.__etapes = GoogleMapsTransit(user_id=self.__user_id, startcoord=self.__pos_init, endcoord=self.__pos_final,
                                          driving_mode="transit", transit_mode="",
                                          waypoints="").get_etape()
        self.__compute_distance_tot()
        self.__compute_duree_tot()
        self.__compute_nb_etape()

    def __compute_distance_tot(self):
        for step in self.etapes:
            self.__distance_tot += step[0]

    def __compute_duree_tot(self):
        for step in self.etapes:
            self.__duree_tot += step[1]

    def __compute_nb_etape(self):
        n = len(self.__etapes)
        # Is the walking for changing transit mode a step?
        for x in range(0, n-1):
            if self.__etapes[x][5] != self.__etapes[x+1][5]:
                self.__nb_etapes += 1

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, valeur):
        print("You are not allowed to modify user_id by {}".format(valeur))

    @property
    def pos_init(self):
        return self.__pos_init

    @pos_init.setter
    def pos_init(self, valeur):
        print("You are not allowed to modify pos_init by {}".format(valeur))

    @property
    def pos_final(self):
        return self.__pos_final

    @pos_final.setter
    def pos_final(self, valeur):
        print("You are not allowed to modify pos_final by {}".format(valeur))

    @property
    def duree_tot(self):
        return self.__duree_tot

    @duree_tot.setter
    def duree_tot(self, valeur):
        print("You are not allowed to modify duree_tot by {}".format(valeur))

    @property
    def distance_tot(self):
        return self.__distance_tot

    @distance_tot.setter
    def distance_tot(self, valeur):
        print("You are not allowed to modify distance_tot by {}".format(valeur))

    @property
    def etapes(self):
        return self.__etapes

    @etapes.setter
    def etapes(self, valeur):
        print("You are not allowed to modify etapes by {}".format(valeur))

    @property
    def nb_etapes(self):
        return self.__nb_etapes

    @nb_etapes.setter
    def nb_etapes(self, valeur):
        print("You are not allowed to modify nb_etapes by {}".format(valeur))

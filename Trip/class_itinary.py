#!usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'eke, gab, axel'

from APIs.class_googlesmaps_new import GoogleMaps, GoogleMapsTransit


class Foot:

    def __init__(self, user_id, pos_init, pos_final):
        print("pos_init {}, pos_final {}, user_id {}".format(pos_init, pos_final, user_id))
        self.__etapes = GoogleMaps(user_id=user_id, startcoord=pos_init, endcoord=pos_final,
                                   driving_mode="walking", transit_mode="",
                                   waypoints="").get_etape()
        self.__duree_tot = self.compute_duree_tot()
        self.__distance_tot = self.compute_distance_tot()

    def compute_distance_tot(self):
        __distance_tot = 0
        for step in self.etapes:
            __distance_tot += step[0]
        return __distance_tot

    def compute_duree_tot(self):
        __duree_tot = 0
        for step in self.etapes:
            __duree_tot += step[1]
        return __duree_tot

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


class Bicycle:

    def __init__(self, user_id, pos_init, pos_final):
        self.__etapes = GoogleMaps(user_id=user_id, startcoord=pos_init, endcoord=pos_final,
                                   driving_mode="bicycling", transit_mode="",
                                   waypoints="").get_etape()
        self.__duree_tot = self.compute_duree_tot()
        self.__distance_tot = self.compute_distance_tot()

    def compute_distance_tot(self):
        __distance_tot = 0
        for step in self.etapes:
            __distance_tot += step[0]
        return __distance_tot

    def compute_duree_tot(self):
        __duree_tot = 0
        for step in self.etapes:
            __duree_tot += step[1]
        return __duree_tot

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


class Car:

    def __init__(self, user_id, pos_init, pos_final):
        self.__etapes = GoogleMaps(user_id=user_id, startcoord=pos_init, endcoord=pos_final,
                                   driving_mode="driving", transit_mode="",
                                   waypoints="").get_etape()
        self.__duree_tot = self.compute_duree_tot()
        self.__distance_tot = self.compute_distance_tot()

    def compute_distance_tot(self):
        __distance_tot = 0
        for step in self.etapes:
            __distance_tot += step[0]
        return __distance_tot

    def compute_duree_tot(self):
        __duree_tot = 0
        for step in self.etapes:
            __duree_tot += step[1]
        return __duree_tot

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


class Transit:

    def __init__(self,user_id, pos_init, pos_final):
        self.__etapes = GoogleMapsTransit(user_id=user_id, startcoord=pos_init, endcoord=pos_final,
                                          driving_mode="transit", transit_mode="",
                                          waypoints="").get_etape()
        self.__distance_tot = self.compute_distance_tot()
        self.__duree_tot = self.compute_duree_tot()
        self.__nb_etapes = self.compute_nb_etape()

    def compute_distance_tot(self):
        __distance_tot = 0
        for step in self.etapes:
            __distance_tot += step[0]
        return __distance_tot

    def compute_duree_tot(self):
        __duree_tot = 0
        for step in self.etapes:
            __duree_tot += step[1]
        return __duree_tot

    def compute_nb_etape(self):
        __nb_etape = 1
        n = len(self.etapes)
        #Is the walking for changing transit mode a step?
        for x in range(0,n-1):
            if self.etapes[x][5] != self.etapes[x+1][5]:
                __nb_etape += 1
        return __nb_etape

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

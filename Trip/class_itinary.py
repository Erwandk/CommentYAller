#!usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'eke, gab, axel'

from APIs.class_googlesmaps import GoogleMaps, GoogleMapsTransit
from threading import Thread


class Foot(Thread):
    """
    Classe représentant le trajet à pied
    """

    def __init__(self, user_id, init_pos, final_pos):
        Thread.__init__(self)
        self.__user_id = user_id
        self.__init_pos = init_pos
        self.__final_pos = final_pos

        self.__steps = []
        self.__total_duration = 0
        self.__total_distance = 0

    def run(self):
        self.__steps = GoogleMaps(user_id=self.__user_id, startcoord=self.__init_pos, endcoord=self.__final_pos,
                                  driving_mode="walking", transit_mode="",
                                  waypoints="").get_etape()
        self.__compute_total_duration()
        self.__compute_total_distance()

    def __compute_total_distance(self):
        for step in self.__steps:
            self.__total_distance += step[0]

    def __compute_total_duration(self):
        for step in self.__steps:
            self.__total_duration += step[1]

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, value):
        print("You are not allowed to modify user_id by {}".format(value))

    @property
    def init_pos(self):
        return self.__init_pos

    @init_pos.setter
    def init_pos(self, value):
        print("You are not allowed to modify init_pos by {}".format(value))

    @property
    def final_pos(self):
        return self.__final_pos

    @final_pos.setter
    def final_pos(self, value):
        print("You are not allowed to modify final_pos by {}".format(value))

    @property
    def total_duration(self):
        return self.__total_duration

    @total_duration.setter
    def total_duration(self, value):
        print("You are not allowed to modify total_duration by {}".format(value))

    @property
    def total_distance(self):
        return self.__total_distance

    @total_distance.setter
    def total_distance(self, value):
        print("You are not allowed to modify total_distance by {}".format(value))

    @property
    def steps(self):
        return self.__steps

    @steps.setter
    def steps(self, value):
        print("You are not allowed to modify steps by {}".format(value))


class Bicycle(Thread):
    """
    Classe représentant le trajet en vélo
    """

    def __init__(self, user_id, init_pos, final_pos):
        Thread.__init__(self)
        self.__user_id = user_id
        self.__init_pos = init_pos
        self.__final_pos = final_pos

        self.__steps = []
        self.__total_duration = 0
        self.__total_distance = 0

    def run(self):
        self.__steps = GoogleMaps(user_id=self.__user_id, startcoord=self.__init_pos, endcoord=self.__final_pos,
                                  driving_mode="bicycling", transit_mode="",
                                  waypoints="").get_etape()
        self.__compute_total_duration()
        self.__compute_total_distance()

    def __compute_total_distance(self):
        for step in self.__steps:
            self.__total_distance += step[0]

    def __compute_total_duration(self):
        for step in self.__steps:
            self.__total_duration += step[1]

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, value):
        print("You are not allowed to modify user_id by {}".format(value))

    @property
    def init_pos(self):
        return self.__init_pos

    @init_pos.setter
    def init_pos(self, value):
        print("You are not allowed to modify init_pos by {}".format(value))

    @property
    def final_pos(self):
        return self.__final_pos

    @final_pos.setter
    def final_pos(self, value):
        print("You are not allowed to modify final_pos by {}".format(value))

    @property
    def total_duration(self):
        return self.__total_duration

    @total_duration.setter
    def total_duration(self, value):
        print("You are not allowed to modify total_duration by {}".format(value))

    @property
    def total_distance(self):
        return self.__total_distance

    @total_distance.setter
    def total_distance(self, value):
        print("You are not allowed to modify total_distance by {}".format(value))

    @property
    def steps(self):
        return self.__steps

    @steps.setter
    def steps(self, value):
        print("You are not allowed to modify steps by {}".format(value))


class Car(Thread):
    """
    Classe représentant le trajet en voiture
    """

    def __init__(self, user_id, init_pos, final_pos):
        Thread.__init__(self)
        self.__user_id = user_id
        self.__init_pos = init_pos
        self.__final_pos = final_pos

        self.__steps = []
        self.__total_duration = 0
        self.__total_distance = 0

    def run(self):
        self.__steps = GoogleMaps(user_id=self.__user_id, startcoord=self.__init_pos, endcoord=self.__final_pos,
                                  driving_mode="driving", transit_mode="",
                                  waypoints="").get_etape()
        self.__compute_total_duration()
        self.__compute_total_distance()

    def __compute_total_distance(self):
        for step in self.__steps:
            self.__total_distance += step[0]

    def __compute_total_duration(self):
        for step in self.__steps:
            self.__total_duration += step[1]

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, value):
        print("You are not allowed to modify user_id by {}".format(value))

    @property
    def init_pos(self):
        return self.__init_pos

    @init_pos.setter
    def init_pos(self, value):
        print("You are not allowed to modify init_pos by {}".format(value))

    @property
    def final_pos(self):
        return self.__final_pos

    @final_pos.setter
    def final_pos(self, value):
        print("You are not allowed to modify final_pos by {}".format(value))

    @property
    def total_duration(self):
        return self.__total_duration

    @total_duration.setter
    def total_duration(self, value):
        print("You are not allowed to modify total_duration by {}".format(value))

    @property
    def total_distance(self):
        return self.__total_distance

    @total_distance.setter
    def total_distance(self, value):
        print("You are not allowed to modify total_distance by {}".format(value))

    @property
    def steps(self):
        return self.__steps

    @steps.setter
    def steps(self, value):
        print("You are not allowed to modify steps by {}".format(value))


class Transit(Thread):
    """
    Classe représentant le trajet en transport en commun
    """

    def __init__(self, user_id, init_pos, final_pos):
        Thread.__init__(self)
        self.__user_id = user_id
        self.__init_pos = init_pos
        self.__final_pos = final_pos

        self.__steps = []
        self.__total_duration = 0
        self.__total_distance = 0
        self.__steps_nbr = 1

    def run(self):
        self.__steps = GoogleMapsTransit(user_id=self.__user_id, startcoord=self.__init_pos, endcoord=self.__final_pos,
                                  driving_mode="transit", transit_mode="",
                                  waypoints="").get_etape()
        self.__compute_total_duration()
        self.__compute_total_distance()
        self.__compute_steps_nbr()

    def __compute_total_distance(self):
        for step in self.__steps:
            self.__total_distance += step[0]

    def __compute_total_duration(self):
        for step in self.__steps:
            self.__total_duration += step[1]

    def __compute_steps_nbr(self):
        n = len(self.__steps)
        # Is the walking for changing transit mode a step?
        for x in range(0, n - 1):
            if self.__steps[x][5] != self.__steps[x + 1][5]:
                self.__steps_nbr += 1

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, value):
        print("You are not allowed to modify user_id by {}".format(value))

    @property
    def init_pos(self):
        return self.__init_pos

    @init_pos.setter
    def init_pos(self, value):
        print("You are not allowed to modify init_pos by {}".format(value))

    @property
    def final_pos(self):
        return self.__final_pos

    @final_pos.setter
    def final_pos(self, value):
        print("You are not allowed to modify final_pos by {}".format(value))

    @property
    def total_duration(self):
        return self.__total_duration

    @total_duration.setter
    def total_duration(self, value):
        print("You are not allowed to modify total_duration by {}".format(value))

    @property
    def total_distance(self):
        return self.__total_distance

    @total_distance.setter
    def total_distance(self, value):
        print("You are not allowed to modify total_distance by {}".format(value))

    @property
    def steps_nbr(self):
        return self.__steps_nbr

    @steps_nbr.setter
    def steps_nbr(self, value):
        print("You are not allowed to modify steps_nbr by {}".format(value))

    @property
    def steps(self):
        return self.__steps

    @steps.setter
    def steps(self, value):
        print("You are not allowed to modify steps by {}".format(value))

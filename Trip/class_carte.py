#!usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'eke, gab, axel'
import folium
import os


class Carte:

    def __init__(self, trip, trip_type):
        """trip_type est censé etre de la forme 'trip.trip_foot'"""
        self.__etape = Carte.set_mode(trip, trip_type)
        self.__min_lat = min([etapes[2]["lat"] for etapes in self.__etape]+[trip.gps_final['lat']]) - 0.00025
        self.__max_lat = max([etapes[2]["lat"] for etapes in self.__etape]+[trip.gps_final['lat']]) + 0.00025
        self.__min_lon = min([etapes[2]["lng"] for etapes in self.__etape]+[trip.gps_final['lng']]) - 0.00025
        self.__max_lon = max([etapes[2]["lng"] for etapes in self.__etape]+[trip.gps_final['lng']]) + 0.00025
        self.__trip = trip

    @staticmethod
    def set_mode(trip, trip_type):

        if trip_type == "trip_foot":
            return trip.trip_foot.steps
        elif trip_type == 'trip_bicycle':
            return trip.trip_bicycle.steps
        elif trip_type == "trip_car":
            return trip.trip_car.steps
        elif trip_type == "trip_velib":
            return trip.trip_velib.setps
        else:
            return trip.trip_transit.steps

    def get_map(self):

        m = folium.Map(location=[self.trip.gps_init["lat"],self.trip.gps_init["lng"]],zoom_start=26)
        path = os.path.join(os.getcwd(), 'static/carte.html')
        folium.Marker([self.trip.gps_init["lat"],self.trip.gps_init["lng"]], icon=folium.Icon(color="red")
                      , popup="<b>Start</b>").add_to(m)
        folium.Marker([self.trip.gps_final["lat"],self.trip.gps_final["lng"]],icon=folium.Icon(color="red"),
                      popup="<b>End</b>").add_to(m)
        n = len(self.__etape)
        for k in range(1,n):
            print(k)
            folium.Marker([self.__etape[k][2]["lat"],self.__etape[k][2]["lng"]], popup="<i>Etape {}".format(k)).add_to(m)
        m.save(path)

    @property
    def min_lat(self):
        return self.__min_lat

    @min_lat.setter
    def min_lat(self,valeur):
        print("You are not allowed to modify min_lat by {}".format(valeur))

    @property
    def max_lat(self):
        return self.__max_lat

    @max_lat.setter
    def max_lat(self,valeur):
        print("You are not allowed to modify max_lat by {}".format(valeur))

    @property
    def min_lon(self):
        return self.__min_lon

    @min_lon.setter
    def min_lon(self,valeur):
        print("You are not allowed to modify max_lat by {}".format(valeur))

    @property
    def max_lon(self):
        return self.__max_lon

    @max_lon.setter
    def max_lon(self,valeur):
        print("You are not allowed to modify max_lon by {}".format(valeur))

    @property
    def trip(self):
        return self.__trip

    @trip.setter
    def trip(self,valeur):
        print("You are not allowed to modify trip by {}".format(valeur))
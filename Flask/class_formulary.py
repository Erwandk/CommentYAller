#!usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'eke, gab, axel'


class Formulary:
    """
    Cette classe représente le formulaire rentré par l'utilisateur sur la page principale
    """

    def __init__(self, form, info_user):
        """
        :param form: formulaire provenant la page html principale
        :param info_user: object provenant la classe InfoUser renseignant les informations de l'utilisateur
        """
        self.__pos_init = form.get('pos_init', '')
        self.__pos_final = form.get('pos_final', '')
        self.__bagage = form.get('bagage', 'off')
        self.__elevation = form.get('elevation', 'off')
        self.__pers_bicycle = form.get('pers_bicycle', 'off')
        self.__pers_car = form.get('pers_car', 'off')

        self.__compute_info(info_user)
        self.__check_data = self.__check_form_data()

    def __check_form_data(self):
        """
        Méthode checkant les données envoyées via le formulaire par l'utilisateur
        """
        if self.pos_init == "" or self.pos_init == "None%2CNone" or self.pos_final == "":
            return False
        else:
            return True

    def __compute_info(self, info):
        """
        Méthode permettant de récupérer les coordonnées GPS de l'utilisateur dans le cas où le départ
        s'effectue depuis sa propre position
        """
        if self.__pos_init == "Ma position":
            self.__pos_init = str(info.lat) + "%2C" + str(info.long)

    # Définition des getters, setters des attributs de la classe
    @property
    def pos_init(self):
        return self.__pos_init

    @pos_init.setter
    def pos_init(self, value):
        raise AttributeError("You are not allowed to modify pos_init by {}".format(value))

    @property
    def pos_final(self):
        return self.__pos_final

    @pos_final.setter
    def pos_final(self, value):
        raise AttributeError("You are not allowed to modify pos_final by {}".format(value))

    @property
    def check_data(self):
        return self.__check_data

    @check_data.setter
    def check_data(self, value):
        raise AttributeError("You are not allowed to modify check_data by {}".format(value))

    @property
    def bagage(self):
        return self.__bagage

    @bagage.setter
    def bagage(self, value):
        raise AttributeError("You are not allowed to modify bagage by {}".format(value))

    @property
    def elevation(self):
        return self.__elevation

    @elevation.setter
    def elevation(self, value):
        raise AttributeError("You are not allowed to modify elevation by {}".format(value))

    @property
    def pers_bicycle(self):
        return self.__pers_bicycle

    @pers_bicycle.setter
    def pers_bicycle(self, value):
        raise AttributeError("You are not allowed to modify pers_bicycle by {}".format(value))

    @property
    def pers_car(self):
        return self.__pers_car

    @pers_car.setter
    def pers_car(self, value):
        raise AttributeError("You are not allowed to modify pers_car by {}".format(value))
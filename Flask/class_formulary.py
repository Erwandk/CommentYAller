#!usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'eke, gab, axel'


class Formulary:
    """
    Cette classe représente le formulaire rentré par l'utilisateur
    """

    def __init__(self, form):
        """
        Le constructeur de cette classe prend en entrée le formulaire entré par l'utilisateur
        """
        self.__pos_init = form.get('pos_init', '')
        self.__pos_final = form.get('pos_final', '')
        self.__bagage = form.get('bagage', False)
        self.__elevation = form.get('elevation', False)

        self.__check_data = self.__check_form_data()

    def __check_form_data(self):
        """
        Cette fonction checke les données envoyées via le formulaire par l'utilisateur
        """
        if self.pos_init == "" or self.pos_final == "":
            return False
        else:
            return True

    # Définition des getters, setters des attributs de notre classe
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
    def check_data(self):
        return self.__check_data

    @check_data.setter
    def check_data(self, valeur):
        print("Reflechir à l'autorisation ou non de la modification de check_data")
        self.__check_data = valeur

    @property
    def bagage(self):
        return self.__bagage

    @bagage.setter
    def bagage(self, valeur):
        print("Reflechir à l'autorisation ou non de la modification de bagage")
        self.__bagage = valeur

    @property
    def elevation(self):
        return self.__elevation

    @elevation.setter
    def elevation(self, valeur):
        print("Reflechir à l'autorisation ou non de la modification de elevation")
        self.__elevation = valeur

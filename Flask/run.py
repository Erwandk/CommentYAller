#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'eke, axel, gab'

# Importation des librairies
from flask import Flask, request, render_template, url_for, redirect, send_file
import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), "..")))

# Importation des données utiles du projet
from user_api import secret_key
from Flask.class_formulary import Formulary
from APIs.class_InfoUser import InfoUser
from Trip.class_trip import Trip
from Trip.class_map import Maps


app = Flask(__name__)
app.secret_key = secret_key


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    racine du site web
    """
    err = ""

    if request.method == 'POST':
        info_user = InfoUser()
        form = Formulary(request.form, info_user)
        if not form.check_data:
            if form.pos_init == "None%2CNone":
                err = 'La position GPS de l utilisateur est introuvable'
            else:
                err = 'Les données envoyées sont incorrectes'
            return render_template('main_getzere.html', err=err)
        return redirect(url_for('trajet', pos_init=form.pos_init, pos_final=form.pos_final,
                                bagage=form.bagage, elevation=form.elevation, pers_bicycle=form.pers_bicycle,
                                pers_car=form.pers_car))

    elif request.method == 'GET':
        return render_template('main_getzere.html', err=err)

    else:
        raise NotImplementedError("This method is not implemented !")


@app.route('/trajet?<pos_init>&<pos_final>&<bagage>&<elevation>&<pers_bicycle>&<pers_car>')
def trajet(pos_init, pos_final, bagage, elevation, pers_bicycle, pers_car):
    """
    page des résultats
    """
    trip = Trip(pos_init, pos_final, bagage, elevation, pers_bicycle, pers_car)
    trip_types = ['trip_foot', 'trip_bicycle', 'trip_car', 'trip_velib', 'trip_transit']
    maps = []
    for types in trip_types:
        maps.append(Maps(trip=trip, trip_type=types))
    return render_template('trajet_getzere.html', trip=trip)


@app.route('/map_foot.html')
def image_foot():
    """
    :return: carte du trajet à pied
    """
    try:
        path = os.path.join('static', 'map', 'map_foot.html')
        return send_file(path, cache_timeout=0, add_etags=False)
    except Exception:
        raise ImportError("Could not load map at 'static/map/map_foot.html'")


@app.route('/map_bicycle.html')
def image_bicycle():
    """
    :return: carte du trajet à vélo
    """
    try:
        path = os.path.join('static', 'map', 'map_bicycle.html')
        return send_file(path, cache_timeout=0, add_etags=False)
    except Exception:
        raise ImportError("Could not load map at 'static/map/map_bicycle.html'")


@app.route('/map_car.html')
def image_car():
    """
    :return: carte du trajet en voiture
    """
    try:
        path = os.path.join('static', 'map', 'map_car.html')
        return send_file(path, cache_timeout=0, add_etags=False)
    except Exception:
        raise ImportError("Could not load map at 'static/map/map_car.html'")


@app.route('/map_velib.html')
def image_velib():
    """
    :return: carte du trajet en velib
    """
    try:
        path = os.path.join('static', 'map', 'map_velib.html')
        return send_file(path, cache_timeout=0, add_etags=False)
    except Exception:
        raise ImportError("Could not load map at 'static/map/map_velib.html'")


@app.route('/map_transit.html')
def image_transit():
    """
    :return: carte du trajet en transport
    """
    try:
        path = os.path.join('static', 'map', 'map_transit.html')
        return send_file(path, cache_timeout=0, add_etags=False)
    except Exception:
        raise ImportError("Could not load map at 'static/map/map_transit.html'")


@app.template_filter('format_duration')
def convert_duration(second):
    """
    Filtre convertissant une durée (en s) dans un format plus lisible
    """
    assert isinstance(second, int)
    if second < 30:
        return "0 min"
    elif second < 60:
        return "1 min"
    else:
        minut = second // 60
        second = second % 60
        if minut >= 60:
            hour = minut // 60
            minut = minut % 60
            return "{} h {} min".format(hour, minut)
        else:
            if second > 30:
                minut += 1
            return "{} min".format(minut)


@app.template_filter('format_dist')
def convert_dist(meters):
    """
     Filtre convertissant une distance (en m) dans un format plus lisible
    """
    assert isinstance(meters, int)
    if meters > 1000:
        kmeters = meters // 1000
        meters = round((meters % 1000) / 100)
        return "{}.{} kilomètres".format(kmeters, meters)
    else:
        return "{} mètres".format(meters)


@app.template_filter('format_address')
def convert_adress(address):
    """
     Filtre convertissant une adresse d'url (str) en un format plus lisible
    """
    list_address = address.split('+')
    if len(list_address) != 1:
        del(list_address[-1:])
    new_list_address = []
    for mot in list_address:
        try:
            mot = int(mot)
        except Exception:
            mot = mot[0].upper() + mot[1:]
        new_list_address.append(str(mot))
    new_address = " ".join(new_list_address)
    return new_address


@app.template_filter('round')
def round_value(value):
    """
     Filtre permettant d'arrondir une valeur
    """
    return round(value, 2)


@app.template_filter('format_time')
def convert_timestamp(value):
    return time.strftime('%H:%M', time.localtime(value))


if __name__ == '__main__':

    app.run(port=5000)

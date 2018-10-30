#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'eke, axel, gab'

from user_api import secret_key

from flask import Flask, request, render_template, url_for, redirect, send_file
import os

from Flask.class_formulary import Formulary
from APIs.class_InfoUser import InfoUser
from Trip.class_trip import Trip
from Trip.class_map import Maps


app = Flask(__name__)
app.secret_key = secret_key


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    racine de notre site web
    """

    if request.method == 'POST':
        info_user = InfoUser()
        form = Formulary(request.form, info_user)
        if not form.check_data:
            if form.pos_init == "None%2CNone":
                print(u'La position GPS de l utilisateur est introuvable', 'error')
            else:
                print(u'Les données envoyées sont incorrectes', 'error')
            return render_template('main_getzere.html')
        return redirect(url_for('trajet', pos_init=form.pos_init, pos_final=form.pos_final,
                                bagage=form.bagage, elevation=form.elevation, pers_bicycle=form.pers_bicycle,
                                pers_car=form.pers_car))

    elif request.method == 'GET':
        return render_template('main_getzere.html')

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
    try:
        path = os.path.join('static', 'map', 'map_foot.html')
        return send_file(path, cache_timeout=0, add_etags=False)
    except Exception:
        raise ImportError("Could not load map at 'static/map/map_foot.html'")


@app.route('/map_bicycle.html')
def image_bicycle():
    try:
        path = os.path.join('static', 'map', 'map_bicycle.html')
        return send_file(path, cache_timeout=0, add_etags=False)
    except Exception:
        raise ImportError("Could not load map at 'static/map/map_bicycle.html'")


@app.route('/map_car.html')
def image_car():
    try:
        path = os.path.join('static', 'map', 'map_car.html')
        return send_file(path, cache_timeout=0, add_etags=False)
    except Exception:
        raise ImportError("Could not load map at 'static/map/map_car.html'")


@app.route('/map_velib.html')
def image_velib():
    try:
        path = os.path.join('static', 'map', 'map_velib.html')
        return send_file(path, cache_timeout=0, add_etags=False)
    except Exception:
        raise ImportError("Could not load map at 'static/map/map_velib.html'")


@app.route('/map_transit.html')
def image_transit():
    try:
        path = os.path.join('static', 'map', 'map_transit.html')
        return send_file(path, cache_timeout=0, add_etags=False)
    except Exception:
        raise ImportError("Could not load map at 'static/map/map_transit.html'")


@app.template_filter('format_time')
def convert_time(second):
    if second > 60:
        minut = second // 60
        second = second % 60
        if minut > 60:
            hour = minut // 60
            minut = minut % 60
            return "{} h {} min".format(hour, minut)
        else:
            if second > 30:
                minut += 1
            return "{} min".format(minut)
    else:
        return "{} sec".format(second)


@app.template_filter('format_dist')
def convert_time(meters):
    if meters > 1000:
        kmeters = meters // 1000
        meters = meters % 1000
        return "{} kilomètres et {} mètres".format(kmeters, meters)
    else:
        return "{} mètres".format(meters)


@app.template_filter('format_address')
def convert_adress(address):
    list_address = address.split('+')
    list_address.remove('paris')
    new_list_address = []
    for mot in list_address:
        try:
            mot = int(mot)
        except Exception:
            mot = mot[0].upper() + mot[1:]
        new_list_address.append(str(mot))
    new_address = " ".join(new_list_address)
    return new_address


if __name__ == '__main__':

    app.run(debug=True, port=5000)

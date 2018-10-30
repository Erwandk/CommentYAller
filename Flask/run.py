#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'eke, axel, gab'

from user_api import secret_key

from flask import Flask, request, render_template, url_for, redirect, send_file

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
            if form.pos_init == "None%C2None":
                print(u'La position GPS de l utilisateur est introuvable', 'error')
            else:
                print(u'Les données envoyées sont incorrectes', 'error')
            return render_template('main_getzere.html')
        return redirect(url_for('trajet', pos_init=form.pos_init, pos_final=form.pos_final,
                                bagage=form.bagage, elevation=form.elevation))

    elif request.method == 'GET':
        return render_template('main_getzere.html')

    else:
        raise NotImplementedError("This method is not implemented !")


@app.route('/map_foot.html')
def image_foot():
    try:
        return send_file('static/map/map_foot.html', cache_timeout=0, add_etags=False)
    except Exception:
        raise ImportError("Could not load map at 'static/map/map_foot.html'")


@app.route('/map_bicycle.html')
def image_bicycle():
    try:
        return send_file('static/map/map_bicycle.html', cache_timeout=0, add_etags=False)
    except Exception:
        raise ImportError("Could not load map at 'static/map/map_bicycle.html'")


@app.route('/map_car.html')
def image_car():
    try:
        return send_file('static/map/map_car.html', cache_timeout=0, add_etags=False)
    except Exception:
        raise ImportError("Could not load map at 'static/map/map_car.html'")


@app.route('/map_velib.html')
def image_velib():
    try:
        return send_file('static/map/map_velib.html', cache_timeout=0, add_etags=False)
    except Exception:
        raise ImportError("Could not load map at 'static/map/map_velib.html'")


@app.route('/map_transit.html')
def image_transit():
    try:
        return send_file('static/map/map_transit.html', cache_timeout=0, add_etags=False)
    except Exception:
        raise ImportError("Could not load map at 'static/map/map_transit.html'")


@app.route('/trajet?<pos_init>&<pos_final>&<bagage>&<elevation>')
def trajet(pos_init, pos_final, bagage, elevation):
    """
    page des résultats
    """
    trip = Trip(pos_init, pos_final, bagage, elevation)
    trip_types = ['trip_foot', 'trip_bicycle', 'trip_car', 'trip_velib', 'trip_transit']
    maps = []
    for types in trip_types:
        maps.append(Maps(trip=trip, trip_type=types))
    return render_template('trajet_getzere.html', trip=trip)


if __name__ == '__main__':

    app.run(debug=True, port=5000)

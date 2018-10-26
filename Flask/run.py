#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'eke, axel, gab'

from user_api import secret_key

from flask import Flask, request, render_template, url_for, redirect, session, send_file

from Flask.class_formulary import Formulary
from Trip.class_trip import Trip
from APIs.class_InfoUser import InfoUser

from Trip.class_carte import Carte
import folium


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

@app.route('/carte.html')
def image():
    print("test test")
    return send_file('static/carte.html', cache_timeout=0, add_etags=False)

@app.route('/trajet?<pos_init>&<pos_final>&<bagage>&<elevation>', methods=['GET', 'POST'])
def trajet(pos_init, pos_final, bagage, elevation):
    """
    page des résultats
    """
    if request.method == 'GET':
        trip = Trip(pos_init, pos_final, bagage, elevation)
        print("trip_type dans def trajet:{}:".format(trip.recommendation))
        carte = Carte(trip, trip_type=trip.recommendation)
        carte.get_map()
        return render_template('trajet_getzere.html', trip=trip, carte=carte)

    if request.method == 'POST':
        type_trip = request.form.get('type_trip')
        print('type_trip: {}'.format(type_trip))
        # trip = session.pop('trip')
        # TODO : en attendant de trouver comment stocker trip, on le ré-appelle ici !
        trip = Trip(pos_init, pos_final, bagage, elevation)

        carte = Carte(trip, type_trip)
        return render_template('trajet_getzere.html', trip=trip, carte=carte)
    else:
        raise NotImplementedError("This method is not implemented !")

if __name__ == '__main__':

    app.run(debug=True, port=5000)

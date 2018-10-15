#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'eke, axel, gab'

from user_api import secret_key
from flask import Flask, request, render_template, flash, url_for, redirect

from Flask.class_formulary import Formulary
from Trip.class_trip import Trip

app = Flask(__name__)
app.secret_key = secret_key


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    racine de notre site web
    """
    if request.method == 'POST':
        form = Formulary(request.form)
        if not form.check_data:
            flash(u'Les données envoyées sont incorrectes', 'error')
            return render_template('main_getzere.html')
        return redirect(url_for('trajet', pos_init=form.pos_init, pos_final=form.pos_final))

    elif request.method == 'GET':
        return render_template('main_getzere.html')

    else:
        return "Cette methode n'est pas implémentée..."


@app.route('/trajet?<pos_init>&<pos_final>')
def trajet(pos_init, pos_final):
    """
    page des résultats
    """
    trip = Trip(pos_init, pos_final)
    return render_template('trajet_getzere.html', trip=trip)


if __name__ == '__main__':

    app.run(debug=True, port=5000)

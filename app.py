"""
meubles = [
    {'id':1,'nom':'klippan', 'prix':'50.20', 'dateFabrication':'2020-06-06', 'couleur':'rouge', 'materiaux' :'bois', 'typeMeuble_id':1},
    {'id': 2, 'nom':'malm', 'prix':'12.00', 'dateFabrication':'2020-06-06', 'couleur':'vert', 'materiaux' :'acier', 'typeMeuble_id':2},
    {'id': 3, 'nom':'besta', 'prix':'14.36', 'dateFabrication':'2020-06-06', 'couleur':'jaune', 'materiaux' :'bois', 'typeMeuble_id':3},
    {'id': 4, 'nom':'billy', 'prix':'24.59', 'dateFabrication':'2020-06-06', 'couleur':'bleu', 'materiaux' :'verre', 'typeMeuble_id':4},
    {'id': 5, 'nom':'friheten', 'prix':'42.21', 'dateFabrication':'2020-06-06', 'couleur':'ebene', 'materiaux' :'acier', 'typeMeuble_id':1},
    {'id': 6, 'nom':'brimnes', 'prix':'11.11', 'dateFabrication':'2019-06-06', 'couleur':'magenta', 'materiaux' :'alumonium', 'typeMeuble_id':2},
    {'id':7,'nom':'la commode du luxe', 'prix':'35.21', 'dateFabrication':'2019-06-06', 'couleur':'voilet', 'materiaux' :'marbre', 'typeMeuble_id':3},
    {'id':8,'nom':'lack', 'prix':'32.25', 'dateFabrication':'2019-12-06', 'couleur':'gris', 'materiaux' :'acier', 'typeMeuble_id':4},
    {'id':9,'nom':'vilme', 'prix':'52.36', 'dateFabrication':'2019-12-26', 'couleur':'satin', 'materiaux' :'bois', 'typeMeuble_id':1},
]

type_meubles = [
            {'id':1,'libelle':'canape'},
            {'id':2,'libelle':'lit'},
            {'id':3,'libelle':'commode'},
            {'id':4,'libelle':'armoire'},
]
"""


#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

import pymysql.cursors

app = Flask(__name__)
app.secret_key = 'une cle(token) : grain de sel(any random string)'

def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host="localhost",
            user="tsiouan",
            password="2212",
            database="BDD_tsiouan",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_accueil():
    return render_template('layout.html')

@app.route('/type-meubles/show')
def show_type_meuble():
    mycursor = get_db().cursor()
    sql = """SELECT type_meuble.*
             FROM type_meuble
             ORDER BY type_meuble.id_type_meuble"""

    mycursor.execute(sql)
    type_meuble = mycursor.fetchall()
    return render_template('type_meubles/show_type_meubles.html', type_meuble=type_meuble)

@app.route('/type-meubles/add', methods=['GET'])
def add_type_meuble():
    return render_template('type_meubles/add_type_meubles.html')

@app.route('/type-meubles/add', methods=['POST'])
def valid_add_type_meuble():
    mycursor = get_db().cursor()
    libelle = request.form.get('libelle', '')
    sql = """INSERT INTO type_meuble(libelle)
             VALUES (%s);"""

    mycursor.execute(sql, [libelle])
    get_db().commit()
    message = u'type ajouté , libellé :' + libelle
    flash(message, 'alert-success')
    return redirect('/type-meubles/show')

@app.route('/type-meubles/delete', methods=['GET'])
def delete_type_meuble():
    mycursor = get_db().cursor()
    id = request.args.get('id', '')

    sql = """DELETE FROM type_meuble
             WHERE id_type_meuble = %s;"""

    mycursor.execute(sql, [id])
    get_db().commit()
    message = u'un type de meuble supprimé, id : ' + id
    flash(message, 'alert-warning')
    return redirect('/type-meubles/show')

@app.route('/type-meubles/edit', methods=['GET'])
def edit_type_meuble():
    mycursor = get_db().cursor()
    id = request.args.get('id', '')

    sql = """SELECT type_meuble.*
             FROM type_meuble
             WHERE type_meuble.id_type_meuble = %s;"""

    mycursor.execute(sql, [id])
    type_meuble = mycursor.fetchone()
    return render_template('type_meubles/edit_type_meubles.html', type_meuble=type_meuble)

@app.route('/type-meubles/edit', methods=['POST'])
def valid_edit_type_meuble():
    mycursor = get_db().cursor()
    id = request.form.get('id', '')
    libelle = request.form.get('libelle', '')

    sql = """UPDATE type_meuble
             SET libelle = %s
             WHERE id_type_meuble = %s;"""

    mycursor.execute(sql, [libelle, id])
    get_db().commit()
    message = u'type de meuble modifié, id : ' + id + ' libelle : ' + libelle
    flash(message, 'alert-warning')
    return redirect('/type-meubles/show')

@app.route('/meubles/show')
def show_meubles():
    mycursor = get_db().cursor()

    sql = """SELECT meuble.*, type_meuble.*
             FROM meuble
             LEFT JOIN type_meuble ON meuble.type_meuble_id = type_meuble.id_type_meuble
             ORDER BY meuble.id_meuble"""

    mycursor.execute(sql)
    meuble = mycursor.fetchall()
    return render_template('meubles/show_meubles.html', meuble=meuble)

@app.route('/meubles-cards/show')
def show_meubles_cards():
    mycrusor = get_db().cursor()

    sql = """ SELECT * FROM meubles"""
    sql2 = """ SELECT * FROM type_meuble"""

    mycrusor.execute(sql)
    meubles = mycrusor.fetchall()

    mycrusor.execute(sql2)
    types_meubles = mycrusor.fetchall()

    return render_template('meubles_cards/show_meubles_cards.html', meuble=meubles, type_meubles=types_meubles)

@app.route('/meubles/add', methods=['GET'])
def add_meubles():
    mycursor = get_db().cursor()

    sql = """SELECT type_meuble.*
             FROM type_meuble"""

    mycursor.execute(sql)
    type_meuble = mycursor.fetchall()
    return render_template('meubles/add_meubles.html', type_meubles=type_meuble)

@app.route('/meubles/add', methods=['POST'])
def valid_add_meubles():
    mycursor = get_db().cursor()

    nom = request.form.get('nom', '')
    type_meubles_id = request.form.get('type_meubles_id', '')
    prix = request.form.get('prix', '')
    date_fabrication = request.form.get('dateFabrication', '')
    couleur = request.form.get('couleur', '')
    materiaux = request.form.get('materiaux', '')

    sql = """INSERT INTO meuble(nom_meuble, type_meuble_id, prix, dateFabrication, couleur, materiaux)
             VALUES(%s, %s, %s, %s, %s, %s)"""

    mycursor.execute(sql, [nom, type_meubles_id, prix, date_fabrication, couleur, materiaux])
    get_db().commit()

    message = u'Meuble ajouté , Nom: ' + nom + ' - Type Meuble Id: ' + type_meubles_id + ' - Prix: ' + prix + ' - Date Fabrication: ' + date_fabrication + ' - Couleur: ' + couleur + ' - Materiaux: ' + materiaux
    flash(message, 'alert-success')
    return redirect('/meubles/show')

@app.route('/meubles-cards/add', methods=['GET'])
def add_meubles_cards():
    return render_template('/meubles_cards/add_meubles_cards.html', type_meubles=type_meubles)

@app.route('/meubles-cards/add', methods=['POST'])
def valid_add_meubles_cards():
    nom = request.form.get('nom', '')
    type_meubles_id = request.form.get('type_meubles_id', '')
    prix = request.form.get('prix', '')
    date_fabrication = request.form.get('dateFabrication', '')
    couleur = request.form.get('couleur', '')
    materiaux = request.form.get('materiaux', '')
    image = request.form.get('image', '')
    print(u'Meuble ajouté , Nom: ', nom, ' - Type Meuble Id: ', type_meubles_id, ' - Prix: ', prix, ' - Date Fabrication: ', date_fabrication, ' - Couleur: ', couleur, ' - Materiaux: ', materiaux)
    message = u'Meuble ajouté , Nom: ' + nom + ' - Type Meuble Id: ' + type_meubles_id + ' - Prix: ' + prix + ' - Date Fabrication: ' + date_fabrication + ' - Couleur: ' + couleur + ' - Materiaux: ' + materiaux
    flash(message, 'alert-success')
    return redirect('/meubles-cards/show')

@app.route('/meubles/delete', methods=['GET'])
def delete_meubles():
    id = request.args.get('id', '')
    message = u'un meuble supprimé, id : ' + id
    flash(message, 'alert-warning')
    return redirect('/meubles/show')

@app.route('/meubles-cards/delete', methods=['GET'])
def delete_meubles_cards():
    id = request.args.get('id', '')
    message = u'un meuble supprimé, id : ' + id
    flash(message, 'alert-warning')
    return redirect('/meubles-cards/show')

@app.route('/meubles/edit', methods=['GET'])
def edit_meubles():
    id = request.args.get('id', '')
    meuble = meubles[int(id)-1]
    return render_template('meubles/edit_meubles.html', meubles=meuble, type_meubles=type_meubles)

@app.route('/meubles/edit', methods=['POST'])
def valid_edit_meubles():
    nom = request.form.get('nom', '')
    type_meubles_id = request.form.get('type_meubles_id', '')
    prix = request.form.get('prix', '')
    date_fabrication = request.form.get('dateFabrication', '')
    couleur = request.form.get('couleur', '')
    materiaux = request.form.get('materiaux', '')
    image = request.form.get('image', '')
    print(u'Meuble ajouté , Nom: ', nom, ' - Type Meuble Id: ', type_meubles_id, ' - Prix: ', prix, ' - Date Fabrication: ', date_fabrication, ' - Couleur: ', couleur, ' - Materiaux: ', materiaux)
    message = u'Meuble ajouté , Nom: ' + nom + ' - Type Meuble Id: ' + type_meubles_id + ' - Prix: ' + prix + ' - Date Fabrication: ' + date_fabrication + ' - Couleur: ' + couleur + ' - Materiaux: ' + materiaux
    flash(message, 'alert-success')
    return redirect('/meubles/show')
    flash(message, 'alert-success')


@app.route('/meubles-cards/edit', methods=['GET'])
def edit_meubles_cards():
    id = request.args.get('id', '')
    meuble = meubles[int(id)-1]
    return render_template('meubles_cards/edit_meubles_cards.html', meubles=meuble, type_meubles=type_meubles)

@app.route('/meubles-cards/edit', methods=['POST'])
def valid_edit_meubles_cards():
    nom = request.form.get('nom', '')
    type_meubles_id = request.form.get('type_meubles_id', '')
    prix = request.form.get('prix', '')
    date_fabrication = request.form.get('dateFabrication', '')
    couleur = request.form.get('couleur', '')
    materiaux = request.form.get('materiaux', '')
    image = request.form.get('image', '')
    print(u'Meuble ajouté , Nom: ', nom, ' - Type Meuble Id: ', type_meubles_id, ' - Prix: ', prix, ' - Date Fabrication: ', date_fabrication, ' - Couleur: ', couleur, ' - Materiaux: ', materiaux)
    message = u'Meuble ajouté , Nom: ' + nom + ' - Type Meuble Id: ' + type_meubles_id + ' - Prix: ' + prix + ' - Date Fabrication: ' + date_fabrication + ' - Couleur: ' + couleur + ' - Materiaux: ' + materiaux
    flash(message, 'alert-success')
    return redirect('/meubles-cards/show')
    flash(message, 'alert-success')

if __name__ == '__main__':
    app.run()
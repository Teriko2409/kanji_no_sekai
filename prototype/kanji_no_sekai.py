import json
import time
import random
import threading
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from kanji_no_sekai_memokanji import *
from kanji_no_sekai_paper import *
from datetime import date, timedelta, datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ndio3290fn0r043ç%)=BNde'


@app.route('/', methods=['GET', 'POST'])
def menu():
    if request.method == 'POST':
        id_player = request.form.get('id_player')
        level = request.form.get('level')

        if id_player:
            session['player_id'] = id_player
            session['level'] = level

            print('Menu : Kanji no Sekai')
            print(f"Player ID : {id_player}")
            print(f"Level: {level}")

            return redirect(url_for('category_menu'))

    return render_template("kanji_no_sekai_menu_login.html")


@app.route('/category')
def category_menu():
    return render_template("kanji_no_sekai_menu_category.html", player_id=session.get('player_id'),
                           level=session.get('level'))


@app.route('/choice_game_distinction')
def choice_game_distinction():
    return render_template("kanji_no_sekai_game_choice_distinction.html", player_id=session.get('player_id'),
                           level=session.get('level'))


@app.route('/memokanji')
def memokanji_launcher():
    return memokanji()


@app.route('/memokanji_data')
def memokanji_data_launcher():
    return memokanji_data()


@app.route("/update_kanjis", methods=["POST"])
def update_kanjis_launcher():
    data = request.get_json()
    kanji_list = data.get("kanjis")
    player_id = session.get("player_id")

    update_memokanji(player_id, kanji_list)

    return jsonify({"status": "success"})


@app.route('/choice_game_meaning')
def choice_game_meaning():
    return render_template("kanji_no_sekai_game_choice_meaning.html", player_id=session.get('player_id'),
                           level=session.get('level'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

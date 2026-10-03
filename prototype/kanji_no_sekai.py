import json
import time
import random
import threading
from flask import Flask, jsonify, render_template, request, redirect, url_for,session
import mysql.connector
from datetime import date, timedelta,datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ndio3290fn0r043ç%)=BNde'

@app.route('/', methods=['GET', 'POST'])
def menu():
    if request.method == 'POST':
        id_player = request.form.get('id_player')
        level = request.form.get('level')

        if id_player:
            print(f"ID: {id_player}")

            print(f"Level: {level}")
            session['player_id'] = id_player
            session['level'] = level

            return redirect(url_for('choice_game'))

    return render_template("kanji_no_sekai_menu_login.html")

@app.route('/choice-game')
def choice_game():

    if 'player_id' not in session:
        return redirect(url_for('menu'))
    return render_template("kanji_no_sekai_menu_choice_game.html", player_id=session['player_id'],level = session['level'] )

#mini-jeux

#memokanji

@app.route('/memokanji')
def memokanji():
    if 'player_id' not in session:
        return redirect(url_for('menu'))
    return render_template("kanji_no_sekai_memokanji.html", player_id=session['player_id'], level = session['level'])

def download_json_data(json_file_path="memokanji.json", nb_groupes=4):

    with open(json_file_path, encoding="utf-8") as f:
        kanji_data = json.load(f)

    level_jlpt_str = session['level']

    level_jlpt_int = int(level_jlpt_str)

    groupes_eligibles = [item for item in kanji_data if item["level"] >= level_jlpt_int]

    nb = min(nb_groupes, len(groupes_eligibles))
    groupes_choisis = random.sample(groupes_eligibles, nb)

    json_data_sort_by_jlpt = []
    for item in groupes_choisis:
        kanjis = item["kanji"][:]
        random.shuffle(kanjis)
        json_data_sort_by_jlpt.append(kanjis[0])
        json_data_sort_by_jlpt.append(kanjis[1])

    kanji_list = json_data_sort_by_jlpt + json_data_sort_by_jlpt
    random.shuffle(kanji_list)

    return kanji_list

@app.route("/memokanji_data")
def memokanji_data():
    try:
        return jsonify(download_json_data())
    except FileNotFoundError:
        return jsonify([])


#Kanji Passport, please



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


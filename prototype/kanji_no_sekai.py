import json
import random
import threading
from flask import Blueprint,Flask, render_template, request, redirect, url_for, session,jsonify
from datetime import date, timedelta, datetime
from kanji_no_sekai_fun import fun
from kanji_no_sekai_bombu import bombu
from kanji_no_sekai_sabakKan import sabakkan
from kanji_no_sekai_ji_KanRun import kanrun
from kanji_no_sekai_infinite import infinite
from kanji_no_sekai_paper import paper
from kanji_no_sekai_memokanji import memokanji
from kanji_no_sekai_kankey import kankey
from kanji_no_sekai_kanter import kanter

def read_session(chemin_fichier) -> str:

    try:
        with open(chemin_fichier, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
            return first_line
    except FileNotFoundError:
        print(f"Error File Not Found: '{chemin_fichier}'")
        return ""
    except Exception as error_message:
        print(f"Error: {error_message}")
        return ""

app = Flask(__name__)
app.config['SECRET_KEY'] = read_session("sessionKey")

#Routes for minigames

app.register_blueprint(fun)

app.register_blueprint(bombu)

app.register_blueprint(sabakkan)

app.register_blueprint(kanrun)

app.register_blueprint(infinite)

app.register_blueprint(paper)

app.register_blueprint(memokanji)

app.register_blueprint(kankey)

app.register_blueprint(kanter)

@app.route('/', methods=['GET', 'POST'])
def menu():
    if request.method == 'POST':
        id_player = request.form.get('id_player')
        level = request.form.get('level')

        if request.form.get('mute') == '1':
            session['mute'] = 1
        else:
            session['mute'] = 0

        mute = session['mute']

        if id_player:
            session['player_id'] = id_player
            session['level'] = level

            print('Menu : Kanji no Sekai')
            print(f"Player ID : {id_player}")
            print(f"Level: {level}")
            print(f"Mute: {mute}")


            return redirect(url_for('category_menu'))

    return render_template("kanji_no_sekai_menu_login.html")

# template category
@app.route('/category')
def category_menu():
    return render_template("kanji_no_sekai_menu_category.html",
                           player_id=session.get('player_id'),
                           level=session.get('level'),
                           mute=session.get('mute'))

# templates mini-games

@app.route('/choice_game_reading')
def choice_game_reading():
    return render_template("kanji_no_sekai_game_choice_reading.html",
                           player_id=session.get('player_id'),
                           level=session.get('level'),
                           mute=session.get('mute'))
@app.route('/choice_game_writing')
def choice_game_writing():
    return render_template("kanji_no_sekai_game_choice_writing.html",
                           player_id=session.get('player_id'),
                           level=session.get('level'),
                           mute=session.get('mute'))

@app.route('/choice_game_meaning')
def choice_game_meaning():
    return render_template("kanji_no_sekai_game_choice_meaning.html",
                           player_id=session.get('player_id'),
                           level=session.get('level'),
                           mute=session.get('mute'))

@app.route('/choice_game_distinction')
def choice_game_distinction():
    return render_template("kanji_no_sekai_game_choice_distinction.html",
                           player_id=session.get('player_id'),
                           level=session.get('level'),
                           mute=session.get('mute'))

@app.route('/choice_game_usage')
def choice_game_usage():
    return render_template("kanji_no_sekai_game_choice_usage.html",
                           player_id=session.get('player_id'),
                           level=session.get('level'),
                           mute=session.get('mute'))

# Player data
@app.route("/player_save", methods=["POST"])
def player_save():
    data = request.get_json()
    kanji_list = data.get("kanjis", [])
    player_id = session.get("player_id")

    if player_id:
        player_id = int(player_id)

        with open("players_data.json", "r", encoding="utf-8") as file:
            players = json.load(file)

        player = next((p for p in players if p.get("id") == player_id), None)
        if not player:
            return

        if "kanjis:" in player:
            del player["kanjis:"]

        kanji_current = player.get("kanjis", [])
        new_kanjis = list(set(kanji_current + kanji_list))
        player["kanjis"] = new_kanjis

        with open("players_data.json", "w", encoding="utf-8") as f:
            json.dump(players, f, ensure_ascii=False, indent=2)

@app.route('/player_data')
def player_data():
    if 'level' not in session:
        return jsonify([])
    try:
        current_player_id = session['player_id']
        current_player_id_int = int(current_player_id)
        with open('players_data.json', 'r', encoding='utf-8') as file:
            players = json.load(file)

        for player in players:
            if player.get('id') == current_player_id_int:
                kanjis = player.get('kanjis', [])
                print(kanjis)

        return jsonify(kanjis)
    except (FileNotFoundError, ValueError):
        return jsonify([])

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug=True)
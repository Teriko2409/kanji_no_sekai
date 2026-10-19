import json
import random
import threading
from flask import Flask, render_template, request, redirect, url_for, session
from kanji_no_sekai_paper import *
from kanji_no_sekai_memokanji import memokanji
from datetime import date, timedelta, datetime

def read_session(chemin_fichier) -> str:

    try:
        with open(chemin_fichier, "r", encoding="utf-8") as f:
            premiere_ligne = f.readline().strip()
            return premiere_ligne
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{chemin_fichier}' est introuvable.")
        return ""
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
        return ""

app = Flask(__name__)
app.config['SECRET_KEY'] = read_session("sessionKey")


#Routes for minigames + KanjiDex

app.register_blueprint(memokanji)

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
    return render_template("kanji_no_sekai_menu_category.html",
                           player_id=session.get('player_id'),
                           level=session.get('level'))

@app.route('/choice_game_reading')
def choice_game_reading():
    return render_template("kanji_no_sekai_game_choice_reading.html",
                           player_id=session.get('player_id'),
                           level=session.get('level'))
@app.route('/choice_game_writing')
def choice_game_writing():
    return render_template("kanji_no_sekai_game_choice_writing.html",
                           player_id=session.get('player_id'),
                           level=session.get('level'))

@app.route('/choice_game_meaning')
def choice_game_meaning():
    return render_template("kanji_no_sekai_game_choice_meaning.html",
                           player_id=session.get('player_id'),
                           level=session.get('level'))

@app.route('/choice_game_distinction')
def choice_game_distinction():
    return render_template("kanji_no_sekai_game_choice_distinction.html",
                           player_id=session.get('player_id'),
                           level=session.get('level'))

@app.route('/choice_game_usage')
def choice_game_usage():
    return render_template("kanji_no_sekai_game_choice_usage.html",
                           player_id=session.get('player_id'),
                           level=session.get('level'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
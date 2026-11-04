import json
from flask import Blueprint,Flask, render_template, request, redirect, url_for, session,jsonify
from kanji_no_sekai_fun import fun
from kanji_no_sekai_bombu import bombu
from kanji_no_sekai_sabakKan import sabakkan
from kanji_no_sekai_ji_KanRun import kanrun
from kanji_no_sekai_infinite import infinite
from kanji_no_sekai_paper import paper
from kanji_no_sekai_memokanji import memokanji
from kanji_no_sekai_kankey import kankey
from kanji_no_sekai_kanter import kanter
from kanji_no_sekai_kanjidex import kanjidex
from kanji_no_sekai_function import print_player_info, read_session_key, player_data_get, player_data_save


app = Flask(__name__)
app.config['SECRET_KEY'] = read_session_key("sessionKey")

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

app.register_blueprint(kanjidex)

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

            print_player_info(game_name='KNS Menu',player_id=id_player, level=level, mute=mute)

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
@app.route('/player_data', methods=['GET'])
def player_data_launcher():

    current_player_id = session['player_id']

    return player_data_get(int(current_player_id))

@app.route("/player_save", methods=["POST"])
def player_save_launcher():
    data = request.get_json()

    kanji_list = data.get("kanjis", [])
    player_id = session.get("player_id")

    return player_data_save(kanji_list=kanji_list, player_id=int(player_id))

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug=True)
from flask import Blueprint, Flask, render_template, request, redirect, url_for, session, jsonify
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
from kanji_no_sekai_function import print_player_info, read_session_key, player_data_get, player_data_save, \
    players_data_reset_all, id_checking, id_generating

app = Flask(__name__)
app.config['SECRET_KEY'] = read_session_key("sessionKey")

# Routes for minigames

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


@app.route('/')
def menu():
    #players_data_reset_all()

    return redirect(url_for('login'))

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():

    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')

        id_generating(name=name, password=password)

        return render_template("kanji_no_sekai_menu_login.html")


    return render_template("kanji_no_sekai_sign_in.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None

    if request.method == 'POST':

        name = request.form.get('name')
        password = request.form.get('password')

        if name and password:

            player_found, player_id = id_checking(name, password)

            if player_found == True:

                level = request.form.get('level')

                session['mute'] = 1 if request.form.get('mute') == '1' else 0
                mute = session['mute']

                session['tuto'] = 1 if request.form.get('tuto') == '1' else 0
                tuto = session['tuto']

                session['player_id'] = player_id
                session['level'] = level

                print_player_info(game_name='KNS Menu', player_id=player_id, level=level, mute=mute, tuto=tuto)

                return redirect(url_for('category_menu'))
            elif player_found == False:

                error_message = "Player not found"

    return render_template("kanji_no_sekai_menu_login.html", error_message=error_message)

# template category
@app.route('/category')
def category_menu():
    return render_template("kanji_no_sekai_menu_category.html")


# templates mini-games

@app.route('/choice_game_reading')
def choice_game_reading():
    return render_template("kanji_no_sekai_game_choice_reading.html")


@app.route('/choice_game_writing')
def choice_game_writing():
    return render_template("kanji_no_sekai_game_choice_writing.html")


@app.route('/choice_game_meaning')
def choice_game_meaning():
    return render_template("kanji_no_sekai_game_choice_meaning.html")


@app.route('/choice_game_distinction')
def choice_game_distinction():
    return render_template("kanji_no_sekai_game_choice_distinction.html")


@app.route('/choice_game_usage')
def choice_game_usage():
    return render_template("kanji_no_sekai_game_choice_usage.html")

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



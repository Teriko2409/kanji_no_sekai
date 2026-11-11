from flask import Blueprint, Flask, jsonify, render_template, request, redirect, url_for, session
from kanji_no_sekai_function import print_player_info

bombu = Blueprint('bombu', __name__)


@bombu.route('/bombu')
def bombu_launcher():
    id_player = session['player_id']
    level = session['level']
    mute = session['mute']
    tuto = session['tuto']

    print_player_info(game_name='KNS Bombu', player_id=id_player, level=level, mute=mute, tuto=tuto)

    return render_template("kanji_no_sekai_bombu.html", player_id=id_player, level=level, mute=mute)


@bombu.route('/bombu_data')
def data_launcher():

    if 'level' not in session:
        return jsonify([])

    try:
        data = download_json_data_bombu(level_jlpt=session['level'])
        return jsonify(data)
    except (FileNotFoundError, ValueError):
        return jsonify([])

def download_json_data_bombu(level_jlpt):

    return 0
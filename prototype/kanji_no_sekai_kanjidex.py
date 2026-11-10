import json
from flask import Blueprint, Flask, jsonify, render_template, request, redirect, url_for, session
from kanji_no_sekai_function import print_player_info

kanjidex = Blueprint('kanjidex', __name__)

@kanjidex.route('/kanjidex')
def launcher():

    id_player = session['player_id']
    level = session['level']
    mute = session['mute']

    print_player_info(game_name='Kanjidex', player_id=id_player, level=level, mute=mute)


    return render_template("kanji_no_sekai_kanjidex.html",
                           player_id=session['player_id'],
                           level=session['level'],
                           mute=session['mute'])


@kanjidex.route('/kanjidex_data', methods=['GET'])
def kanjidex_data():

    player_id = int(session.get('player_id', 0))

    try:
        with open("kanji_no_sekai_players_data.json", "r", encoding="utf-8") as file:
            players = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        players = []

    player = next((p for p in players if p.get("id") == player_id), None)

    kanjis_list = player.get("kanjis", [])

    kanjidex = []

    def get_kanji_color(learned_time):
        if learned_time == 1:
            return "#d3d3d3"
        elif learned_time == 2 or learned_time == 3:
            return "#E7FF4D"
        elif learned_time == 4 or learned_time == 5:
            return "#ffe94d"
        elif learned_time == 6 or learned_time == 7:
            return "#F0AC0A"
        elif learned_time == 8 or learned_time == 9:
            return "#F04B0A"
        elif learned_time == 10:
            return "#FF0000"

    for item in kanjis_list:
        if isinstance(item, dict):
            k = item.get("kanji")
            t = item.get("learned_time", 1)
            kanjidex.append({
                "kanji": k,
                "learned_time": t,
                "color": get_kanji_color(t)
            })
        elif isinstance(item, str):
            kanjidex.append({
                "kanji": item,
                "learned_time": 1,
                "color": "#d3d3d3"
            })

    return jsonify(kanjidex), 200

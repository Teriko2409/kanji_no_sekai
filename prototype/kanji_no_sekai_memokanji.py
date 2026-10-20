import json
import random
from flask import Blueprint, render_template, redirect, url_for, session, jsonify, request

memokanji = Blueprint('memokanji', __name__)


def download_json_data(level_jlpt, json_file_path="memokanji.json"):
    nombre = 4

    with open(json_file_path, encoding="utf-8") as memokanji_file:
        kanji_data = json.load(memokanji_file)

    level_jlpt_int = int(level_jlpt)

    kanji_level = [
        item for item in kanji_data if item.get("level") >= level_jlpt_int
    ]

    kanji_four = random.sample(kanji_level, nombre)
    kanji_8 = []

    for item in kanji_four:
        kanjis = item["kanji"][:]
        random.shuffle(kanjis)
        kanji_8.append(kanjis[0])
        kanji_8.append(kanjis[1])

    kanji_list = kanji_8 + kanji_8
    return kanji_list


def update_memokanji(player_id, kanji_list):
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


@memokanji.route('/memokanji')
def launcher():
    if 'player_id' not in session:
        return redirect(url_for('menu'))

    return render_template("kanji_no_sekai_memokanji.html",
                           player_id=session['player_id'],
                           level=session['level'])


@memokanji.route('/memokanji_data')
def data_launcher():
    if 'level' not in session:
        return jsonify([])
    try:
        data = download_json_data(level_jlpt=session['level'])
        return jsonify(data)
    except (FileNotFoundError, ValueError):
        return jsonify([])


@memokanji.route('/memokanji_player_data')
def player_data_launcher():

    current_player_id = session['player_id']
    current_player_id_int = int(current_player_id)
    with open('players_data.json', 'r', encoding='utf-8') as file:
        players = json.load(file)

    for player in players:
        if player.get('player_id') == current_player_id_int:
            kanjis = player.get('kanjis', [])

            return jsonify(kanjis)


@memokanji.route("/update_kanjis", methods=["POST"])
def update_kanjis():
    data = request.get_json()
    kanji_list = data.get("kanjis", [])
    player_id = session.get("player_id")

    if player_id:
        update_memokanji(player_id, kanji_list)

    return jsonify({"status": "success"})
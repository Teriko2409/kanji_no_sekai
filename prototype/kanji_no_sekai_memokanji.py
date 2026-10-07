import json
import random
from flask import render_template, redirect, url_for, session, jsonify


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

def memokanji():
    if 'player_id' not in session:
        return redirect(url_for('menu'))

    return render_template("kanji_no_sekai_memokanji.html", player_id=session['player_id'], level=session['level'])

def memokanji_data():
    if 'level' not in session:
        return jsonify([])
    try:
        data = download_json_data(level_jlpt=session['level'])
        return jsonify(data)
    except FileNotFoundError:
        return jsonify([])

def update_memokanji(player_id, kanji_list):
    player_id = int(player_id)

    with open("players_data.json", "r", encoding="utf-8") as file:
        players = json.load(file)


    player = next((p for p in players if p.get("id") == player_id))

    if "kanjis:" in player:
        del player["kanjis:"]

    kanji_current = player.get("kanjis", [])

    new = list(set(kanji_current + kanji_list))
    player["kanjis"] = new

    with open("players_data.json", "w", encoding="utf-8") as f:
        json.dump(players, f, ensure_ascii=False, indent=2)

    return 0
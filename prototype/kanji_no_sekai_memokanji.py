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


@memokanji.route('/memokanji')
def launcher():

    if 'player_id' not in session:
        return redirect(url_for('menu'))

    return render_template("kanji_no_sekai_memokanji.html",
                           player_id=session['player_id'],
                           level=session['level'],
                           mute=session['mute'])

@memokanji.route('/memokanji_data')
def data_launcher():

    data = download_json_data(level_jlpt=session['level'])
    return jsonify(data)



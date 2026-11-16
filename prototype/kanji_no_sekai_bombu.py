import json,random
from flask import Blueprint, Flask, jsonify, render_template, request, redirect, url_for, session
from kanji_no_sekai_function import print_player_info, easter_egg_bombu

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
        zones, bombe_resultat = download_json_data_bombu()

        return jsonify({
            "zones": zones,
            "kanjis": bombe_resultat
        })
    except (FileNotFoundError, ValueError):
        return jsonify([])


def download_json_data_bombu(json_file_path="kanji_no_sekai_bombu.json"):
    with open(json_file_path, encoding="utf-8") as bombu_file:
        kanji_data = json.load(bombu_file)

    hiragana_list = []
    bombe_list = []
    bombe_resultat = []

    for hiragana in kanji_data:
        hiragana_list.extend(hiragana.get('zones', []))
        bombe_list.append(hiragana)

    hiragana_list_unique = list(set(hiragana_list))

    if len(hiragana_list_unique) >= 3:
        zones = random.sample(hiragana_list_unique, 3)
    else:
        zones = hiragana_list_unique

    for bombe in bombe_list:
        zones_du_kanji = bombe.get('zones', [])

        if any(z in zones_du_kanji for z in zones):

            bombe_resultat.append(bombe)

    random.shuffle(bombe_resultat)

    return easter_egg_bombu(zones=zones,bombu=bombe_resultat)
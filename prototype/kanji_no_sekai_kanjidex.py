import json
import time
import random
import threading
from flask import Blueprint, Flask, jsonify, render_template, request, redirect, url_for, session
from datetime import date, timedelta, datetime
from kanji_no_sekai_function import print_player_info

kanjidex = Blueprint('kanjidex', __name__)

@kanjidex.route('/kanjidex')
def launcher():

    id_player = session['player_id']
    level = session['level']
    mute = session['mute']

    print_player_info(game_name='Kanjidex', player_id=id_player, level=level, mute=mute)

    download_json_data()

    return render_template("kanji_no_sekai_kanjidex.html",
                           player_id=session['player_id'],
                           level=session['level'],
                           mute=session['mute'])

def download_json_data(json_file_path="players_data.json"):

    with open(json_file_path, encoding="utf-8") as kanjidex_file:
        kanji_data = json.load(kanjidex_file)

    kanji_learned = []




    return 0
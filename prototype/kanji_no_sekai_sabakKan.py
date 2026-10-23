import json
import time
import random
import threading
from flask import Blueprint, Flask, jsonify, render_template, request, redirect, url_for, session
from datetime import date, timedelta, datetime

sabakkan = Blueprint('sabakkan', __name__)

@sabakkan.route('/sabakkan')
def sabakkan_launcher():

    if 'player_id' not in session:
        return redirect(url_for('menu'))

    id_player = session['player_id']
    level = session['level']

    print('Menu : KNS sabakkan')
    print(f"Player ID : {id_player}")
    print(f"Level: {level}")

    return render_template(
        "kanji_no_sekai_sabakkan.html",
        player_id=id_player,
        level=level,

    )
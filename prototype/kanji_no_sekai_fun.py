import json
import time
import random
import threading
from flask import Blueprint, Flask, jsonify, render_template, request, redirect, url_for, session
from datetime import date, timedelta, datetime
from kanji_no_sekai_function import print_player_info
fun = Blueprint('fun', __name__)


@fun.route('/fun')
def fun_launcher():

    if 'player_id' not in session:
        return redirect(url_for('menu'))

    id_player = session['player_id']
    level = session['level']
    mute = session['mute']

    print_player_info('KNS Fun beat',id_player=id_player, level=level, mute=mute)


    return render_template("kanji_no_sekai_fun.html",player_id=id_player,level=level, mute=mute)
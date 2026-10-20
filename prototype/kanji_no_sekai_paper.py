import json
import time
import random
import threading
from flask import Blueprint, Flask, jsonify, render_template, request, redirect, url_for, session
from datetime import date, timedelta, datetime

paper = Blueprint('paper', __name__)


@paper.route('/paper')
def paper_launcher():
    if 'player_id' not in session:
        return redirect(url_for('menu'))

    return render_template("kanji_no_sekai_paper.html",
                           player_id=session['player_id'],
                           level=session['level'])

@paper.route('/paper_data')
def data_launcher():
    if 'level' not in session:
        data = download_json_data_paper(level_jlpt=session['level'])
        return jsonify(data)
    try:
        return jsonify([])
    except (FileNotFoundError, ValueError):
        return jsonify([])


def download_json_data_paper(level_jlpt, json_file_path="paperkanji.json"):
    number_kanji = 6
    level_jlpt_int = int(level_jlpt)

    false_kanji_number = random.randint(0, (number_kanji - 1))
    true_kanji_number = number_kanji - false_kanji_number

    with open(json_file_path, encoding="utf-8") as paperkanji_file:
        kanji_data = json.load(paperkanji_file)


        kanji_level = [item for item in kanji_data if item.get("level") >= level_jlpt_int]


        true_kanji_list = random.sample(kanji_level, true_kanji_number)
        true_kanji_list_clean = [
            {k: v for k, v in item.items() if not k.endswith(("_f"))}
            for item in true_kanji_list
        ]

        for kanji in true_kanji_list_clean:
            kanji.pop("level", None)
            kanji["correct"] = True


        false_kanji_list = [item for item in kanji_level if item not in true_kanji_list]


        false_kanji_selection = random.sample(false_kanji_list, false_kanji_number)

        possibility_attribut = [
            ("profile", "profile_f"),
            ("onyomi", "onyomi_f"),
            ("kunyomi", "kunyomi_f"),
            ("radical", "radical_f"),
            ("vocabulary", "vocabulary_f")
        ]

        false_kanji_list_clean = []

        for kanji in false_kanji_selection:


            false_number_attribut = random.randint(1, 2)
            possibility_attribut_choice = random.sample(possibility_attribut, false_number_attribut)
            kanji.pop("level", None)
            kanji["correct"] = False


            for normal, faux in possibility_attribut_choice:
                if faux in kanji:
                    kanji[normal] = kanji[faux]


            for _, faux in possibility_attribut:
                kanji.pop(faux, None)


            false_kanji_list_clean.append(kanji)


        final_game_cards = true_kanji_list_clean + false_kanji_list_clean

        random.shuffle(final_game_cards)

        print(json.dumps(final_game_cards, indent=4, ensure_ascii=False))

        return final_game_cards
import json, random
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, session

sabakkan = Blueprint('sabakkan', __name__)

@sabakkan.route('/sabakkan')
def sabakkan_launcher():

    if 'player_id' not in session:
        return redirect(url_for('menu'))

    id_player = session['player_id']
    level = session['level']
    mute = session['mute']

    print('Menu : KNS SabakKan')
    print(f"Player ID : {id_player}")
    print(f"Level: {level}")

    if mute == 0:
        print("Music : ON")
    else:
        print("Music : OFF")

    return render_template("kanji_no_sekai_sabakkan.html",player_id=id_player,level=level, mute=mute)

@sabakkan.route('/sabakkan_data')
def data_launcher():

    if 'level' not in session:
        return jsonify([])

    try:
        data = download_json_data_sabakkan()
        return jsonify(data)
    except (FileNotFoundError, ValueError):
        return jsonify([])
def download_json_data_sabakkan(json_file_path="sabakkan.json"):

    with open(json_file_path, encoding="utf-8") as paperkanji_file:
        kanji_json = json.load(paperkanji_file)

        kanjis = kanji_strokes_recup(kanji_json, 2)

        for kanji in kanjis:
            if kanji["strokes"] < 0:
                kanji["color"] = "red"
            else:
                if kanji["strokes"] > 0:
                    kanji["color"] = "green"

        kanjis.append({
            "kanji": "乙",
            "color": "orange",
            "strokes": 0
        })

        kanjis.append({
            "kanji": "一",
            "color": "orange",
            "strokes": 0
        })

        return kanjis

@sabakkan.route('/sabakkan_result', methods=['POST'])
def sabakkan_result():
    data = request.get_json()
    hand_play = data.get('hand_play')
    hand_bot = data.get('hand_bot')

    resultat = resultat_comparatif_player_bot(hand_play, hand_bot)

    return jsonify(resultat)

def resultat_comparatif_player_bot(hand_play, hand_bot):

    verdict_final = 'PlaceHolder'

    player_resultat = resultat_hand(hand_play)

    bot_resultat = resultat_hand(hand_bot)


    if player_resultat['hand_type'] == '完零':
        verdict_final = message_verdict(add_message= "完零",winner='Player')

    elif bot_resultat['hand_type'] == '完零':
        verdict_final = message_verdict(add_message="完零", winner='Bot')

    elif bot_resultat['hand_type'] == '零' and not player_resultat['hand_type'] == '零':
        verdict_final = message_verdict(add_message="零", winner='Bot')

    elif player_resultat['hand_type'] == '零' and not bot_resultat['hand_type'] == '零':
        verdict_final = message_verdict(add_message="零", winner='Player')

    elif player_resultat['hand_type'] == '超' and not bot_resultat['hand_type'] == '超':
        verdict_final = message_verdict(add_message="超 from the Player", winner='Bot')

    elif bot_resultat['hand_type'] == '超' and not player_resultat['hand_type'] == '超':
        verdict_final = message_verdict(add_message="超 from the Bot", winner='Player')

    elif bot_resultat['hand_type'] == '超' == player_resultat['hand_type'] == '超':
        verdict_final = message_verdict(add_message="", winner='')

    else:
        player_gap_to_zero = (abs(0 - player_resultat['score']))

        bot_gap_to_zero = (abs(0 - bot_resultat['score']))

        if bot_gap_to_zero > player_gap_to_zero:

            verdict_final = message_verdict(add_message="The score", winner='Player')

        elif player_gap_to_zero > bot_gap_to_zero:

            verdict_final = message_verdict(add_message="The score", winner='Bot')

        elif bot_gap_to_zero == player_gap_to_zero:

            if bot_resultat["big_number"] > player_resultat["big_number"]:
                verdict_final = message_verdict(add_message=f'The Big Number : Bot {bot_resultat["big_number"]} / Player {player_resultat["big_number"]}', winner='Bot')

            if bot_resultat["big_number"] < player_resultat["big_number"]:
                verdict_final = message_verdict(add_message=f'The Big Number : Player {player_resultat["big_number"]} / Bot {bot_resultat["big_number"]}', winner='Player')

            if bot_resultat["big_number"] == player_resultat["big_number"]:
                    verdict_final = message_verdict(add_message= "", winner = '')


    resultat = {

        "player_label": player_resultat['hand_type'],
        "bot_label": bot_resultat['hand_type'],
        "verdict": f'{verdict_final}'
    }

    return resultat

def message_verdict(add_message, winner):

    if winner == 'Player':
        message = f'Player Win by {add_message}'
    elif winner == 'Bot':
        message = f'丸さん Win by {add_message}'
    else:
        message = 'Drew'
    return message

def joker(joker_number, score):
    turn = 0
    while turn < joker_number:
        if score <= 0:
            score += 1
        else:
            score -= 1
        turn += 1

    return score
def resultat_hand(hand):

    hand_type = 'Placehorlder'
    seifu = 0
    score = 0
    hand_length = len(hand)
    big_number = 0

    for i in hand:

        score += int(i['strokes'])
        big_number += abs(int(i['strokes']))

        if i['kanji'] == "一" or i['kanji'] == "乙":
            seifu += 1


    score_with_joker = joker(joker_number=seifu, score=score)

    if hand_length == 2 and seifu == 2:
        hand_type = "完零"
    else:
        if score_with_joker == 0 and not (seifu == hand_length):
            hand_type = "零"

        if (-4 <= score_with_joker <= 4) and score_with_joker != 0:
            if score_with_joker > 0:
                hand_type = f'{score_with_joker}正'
            else:
                hand_type = f'{abs(score_with_joker)}負'

        if (-4 > score_with_joker or score_with_joker > 4):
            hand_type = "超"


    resultat = {
        "hand_type": hand_type,
        "score": score_with_joker,
        "big_number": big_number
    }

    return resultat
def kanji_strokes_recup(kanji_file, number_strokes):

    number_category = 3
    if number_strokes > 10:
        return []

    kanji_positif = []
    kanji_negatif = []

    for i in kanji_file:
        if i.get('strokes') == number_strokes:
            kanji_positif.append(i)

        if i.get('strokes') == (-number_strokes):
            kanji_negatif.append(i)

    kanji_positif_3 = random.sample(kanji_positif, number_category)
    kanji_negatif_3 = random.sample(kanji_negatif, number_category)

    kanji_cartes = kanji_positif_3 + kanji_negatif_3

    return kanji_cartes + kanji_strokes_recup(kanji_file, number_strokes + 1)


@sabakkan.route('/sabakkan_bot_action', methods=['POST'])
def sabakkan_bot_action():
    data = request.get_json()

    bot_hand = data.get("bot_hand", [])

    turn = data.get("turn")

    bot_boom_used = data.get("bot_boom_used", False)

    action = "nothing"

    card_index_to_discard = None

    bot_action_probability = random.random()


    if turn > 2 and bot_action_probability < 0.10:
        action = "stop"

    elif not bot_boom_used and bot_action_probability and turn > 2 < 0.15:
        action = "kanboomu"

    elif len(bot_hand) < 1 or bot_action_probability < 0.35:
        action = "draw"

    elif len(bot_hand) > 2 or bot_action_probability < 0.40:
        action = "discard"
        card_index_to_discard = random.randint(0, len(bot_hand) - 1)

    print(f'{action}')
    return jsonify({
        "action": action,
        "card_index_to_discard": card_index_to_discard
    })
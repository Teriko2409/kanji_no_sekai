import json
from flask import jsonify
from datetime import datetime
def print_player_info(game_name='Placeholder', player_id=0, level=0, mute=0):

    now = datetime.now()

    print(f"Player ID : {player_id}")
    print(f"Game : {game_name}")
    print(f"Level: {level}")
    print("Date :", now.strftime("%d/%m/%Y"))
    print("Time :", now.strftime("%H:%M:%S"))

    if mute == 0:
        print("Music : ON")
    else:
        print("Music : OFF")

def read_session_key(chemin_fichier) -> str:

    try:
        with open(chemin_fichier, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
            return first_line
    except FileNotFoundError:
        print(f"Error File Not Found: '{chemin_fichier}'")
        return ""
    except Exception as error_message:
        print(f"Error: {error_message}")
        return ""

def player_data_get(player_id = 0):

    try:
        current_player_id = player_id
        current_player_id_int = int(current_player_id)

        with open('players_data.json', 'r', encoding='utf-8') as file:
            players = json.load(file)

        for player in players:
            if player.get('id') == current_player_id_int:
                kanjis = player.get('kanjis', [])
                print(kanjis)
                return jsonify(kanjis), 200

        return jsonify([]), 200

    except (FileNotFoundError, ValueError):
        return jsonify([]), 200

def player_data_save(kanji_list,player_id = 0 ):

    with open("players_data.json", "r", encoding="utf-8") as file:
        players = json.load(file)

        player = next((p for p in players if p.get("id") == player_id), None)

        if "kanjis:" in player:
            del player["kanjis:"]

        kanji_current = player.get("kanjis", [])
        new_kanjis = list(set(kanji_current + kanji_list))
        player["kanjis"] = new_kanjis

        with open("players_data.json", "w", encoding="utf-8") as f:
            json.dump(players, f, ensure_ascii=False, indent=2)


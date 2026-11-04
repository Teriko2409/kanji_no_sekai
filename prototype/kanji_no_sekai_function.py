import json
from flask import jsonify
from datetime import datetime
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


def player_data_get(player_id=0):
    try:
        with open('players_data.json', 'r', encoding='utf-8') as file:
            players = json.load(file)

        for player in players:
            if player.get('id') == player_id:
                kanjis_data = player.get('kanjis', [])


                if isinstance(kanjis_data, dict):
                    kanjis = list(kanjis_data.keys())

                elif isinstance(kanjis_data, list) and len(kanjis_data) > 0 and isinstance(kanjis_data[0], dict):
                    kanjis = [item.get("kanji") for item in kanjis_data if "kanji" in item]

                else:
                    kanjis = kanjis_data

                return jsonify(kanjis), 200

        return jsonify([]), 200

    except (FileNotFoundError, ValueError):
        return jsonify([]), 200
def player_data_save(kanji_list, player_id=0):

    try:
        with open("players_data.json", "r", encoding="utf-8") as file:
            players = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        players = []

    player = next((p for p in players if p.get("id") == player_id), None)
    if not player:
        return jsonify({"status": "error", "message": "Player not found"}), 404

    if "kanjis:" in player:
        del player["kanjis:"]

    kanji_current = player.get("kanjis", [])

    kanji_dict = {}
    for item in kanji_current:
        if isinstance(item, str):
            kanji_dict[item] = 1
        elif isinstance(item, dict):
            k = item.get("kanji")
            t = item.get("learned_time", 1)
            if k:
                kanji_dict[k] = min(t, 10)


    for kanji in kanji_list:
        current_time = kanji_dict.get(kanji, 0)
        if current_time < 10:
            kanji_dict[kanji] = current_time + 1
        else:
            kanji_dict[kanji] = 10

    player["kanjis"] = [{"kanji": k, "learned_time": t} for k, t in kanji_dict.items()]

    with open("players_data.json", "w", encoding="utf-8") as f:
        json.dump(players, f, ensure_ascii=False, indent=2)

    return jsonify([])
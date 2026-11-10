import json,secrets,hashlib,random

from flask import jsonify
from datetime import datetime

def id_generating(name="", password=""):

    players_id_list = []


    with open("anymous", "r", encoding="utf-8") as file:
        players = file.readlines()

    name_hashed = hashlib.sha256(name.encode('utf-8')).hexdigest()

    password_hashed = hashlib.sha256(password.encode('utf-8')).hexdigest()

    for player in players:
        players_id_list.append(int(player.split('/')[1].strip()))

    if len(players_id_list) == 0:
        max_id = 0
    else:
        max_id = max(players_id_list)

    new_id = max_id + random.randint(1, 100)

    new_player = f"{name_hashed}|{password_hashed}/{new_id} "

    with open("anymous", "a", encoding="utf-8") as file:
        file.write(new_player + "\n")

    with open("players_data.json", "r", encoding="utf-8") as file:
        players = json.load(file)

    new_player_json = {
            "id": new_id,

        }

    players.append(new_player_json)

    with open("players_data.json", "w", encoding="utf-8") as f:
        json.dump(players, f, ensure_ascii=False, indent=2)

    return 0

def id_checking(name="", password=""):

    player_id = 0
    player_is_existed = False

    with open("anymous", "r", encoding="utf-8") as file:
        players = file.readlines()


    name_hashed = hashlib.sha256(name.encode('utf-8')).hexdigest()

    password_hashed = hashlib.sha256(password.encode('utf-8')).hexdigest()

    for player_line in players:

        player_line = player_line.strip()
        if not player_line:
            continue

        parties_pipe = player_line.split('|')

        if len(parties_pipe) < 2:
            continue

        stored_name_hash = parties_pipe[0].strip()

        rest = parties_pipe[1]
        parties_slash = rest.split('/')
        stored_password_hash = parties_slash[0].strip()

        if name_hashed == stored_name_hash:
            if password_hashed == stored_password_hash:

                if len(parties_slash) > 1:
                    player_id = int(parties_slash[1].strip())
                    player_is_existed = True


    return player_is_existed, player_id

def players_data_reset_all():


    with open("players_data.json", "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=2)

    with open("anymous", "w", encoding="utf-8") as file:
        file.write("")

    return 0
def read_session_key(file_path) -> str:

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
            if first_line:
                return first_line
    except FileNotFoundError:
        print(f"Error File Not Found: '{file_path}'\nCreated a new file and Key in ({file_path})")

    new_key = secrets.token_hex(32)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_key)
    return new_key

def print_player_info(game_name='Placeholder', player_id=0, level=0, mute=0, tuto =0):

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

    if tuto == 0:
        print("Tuto : ON")
    else:
        print("Tuto : OFF")

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
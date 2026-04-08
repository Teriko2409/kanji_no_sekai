extends Control

const MODEL_CARTE = preload("res://mini_jeu/MemoKanji/cartes.tscn")

const json_url = preload("res://mini_jeu/MemoKanji/kanji_data_memokanji.json")

@onready var structure = $structure_gameboard

func _ready() -> void:
	var kanji_list = downloaod_json_data()
	
	for i in kanji_list:
		create_cartes(i)

func create_cartes(text_parameter: String) -> void:
	
	var new_carte = MODEL_CARTE.instantiate()
	
	structure.add_child(new_carte)
	var label = new_carte.get_node("kanji_wrote")
	label.text = text_parameter
	
		
func downloaod_json_data() -> Array:
	
	const json_data = json_url.data
	const level_jlpt = 5

	
	var json_data_sort_by_jlpt = []
	
	"""var kanji_list = []"""
	var kanji_list = ["一", "二", "三", "四","日", "月", "火", "水", "木", "金", "土", "山", "上", "下", "左", "右"  ]
	
		
	return kanji_list

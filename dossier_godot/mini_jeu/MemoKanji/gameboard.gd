extends Control

const MODEL_CARTE = preload("res://mini_jeu/MemoKanji/cartes.tscn")

@onready var grille = $GridContainer


func _ready() -> void:
	var mes_kanjis = ["Salut ", "Laura"]
	
	for kanji in mes_kanjis:
		creer_une_carte(kanji)

func creer_une_carte(texte_du_kanji: String) -> void:
	var nouvelle_carte = MODEL_CARTE.instantiate()
	
	grille.add_child(nouvelle_carte)
	var mon_label = nouvelle_carte.get_node("kanji_wrote")
	
	if mon_label:
		mon_label.text = texte_du_kanji

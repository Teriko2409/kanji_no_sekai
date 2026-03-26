extends Control

const MODEL_CARTE = preload("res://mini_jeu/MemoKanji/cartes.tscn")

@onready var grille = $GridContainer


# Le jeu démarre ici !
func _ready() -> void:
	var mes_kanjis = []
	
	for kanji in mes_kanjis:
		creer_une_carte(kanji)


# Notre "machine" qui fabrique et range la carte
func creer_une_carte(texte_du_kanji: String) -> void:
	# a. On clone le modèle
	var nouvelle_carte = MODEL_CARTE.instantiate()
	
	# b. On l'envoie dans la grille (le GridContainer la range tout seul !)
	grille.add_child(nouvelle_carte)
	

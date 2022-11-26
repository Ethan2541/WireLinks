from readingTools import *
from writingTools import *
from trame import *
from liste_trames import *

class Main2:

	def main():
		print("Bienvenue dans WireLinks")
		print("Quel est le nom du fichier que vous souhaitez analyser ? ", end="")
		file_name = input()
		trames = get_frames(file_name)
		for i in range(len(trames)):
			TrameList(Trame(i+1, trames[i]))

		TrameList.afficher_info_imp_gui()
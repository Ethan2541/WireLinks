import sys
from readingTools import *
from writingTools import *
from trame import *
from liste_trames import *

def main():
	print("Bienvenue dans WireLinks")
	print("Quel est le nom du fichier que vous souhaitez analyser ? ", end="")
	file_name = input()
	trames = get_frames(file_name)
	for i in range(len(trames)):
		TrameList(Trame(i+1, trames[i]))
	
	TrameList.afficher_info_imp()

	print("Si vous souhaitez de l'aide tapez /help")

	while True:
		buffer = input()
		if(buffer == "/help"):
			print("exit(): vous permet de quitter le programme\n\
afficher (n: int): affiche la trame numéro (n)\n\
afficher: affiche les informaions importantes de toutes les trames\n\
filtre (f: str): affiche les informations importantes avec les filtres données\n\
liste de filtres:\n\
\tip.src==(a.b.c.d (int.int.int.int)): filtre les trames dont l'adresse ip source est (a.b.c.d)\n\
\tip.dst==(a.b.c.d (int.int.int.int)): filtre les trames dont l'adresse ip destination est (a.b.c.d)\n\
\tmac.src==(a:b:c:d:e:f (int:int:int:int:int:int)): filtre les trames dont l'adresse mac source est (a:b:c:d:e:f)\n\
\tmac.dst==(a:b:c:d:e:f (int:int:int:int:int:int)): filtre les trames dont l'adresse mac destination est (a:b:c:d:e:f)\n\
\tport.src==(a) (int)): filtre les trames dont le port source (a)\n\
\tport.dst==(a) (int)): filtre les trames dont le port destination (a)\n\
\tproto==(a) (protcole)): filtre les trames qui utilisent le protocole (a)\n\
\t\tListe des protocoles supportés: ipv4, ipv6, arp, icmp, tcp, udp, igmp,\n\
\t\t\tegp, igp, xtp, rsv, http, https, smtp, pop, imap, ftp, ssh, dns, dhcp, rdp.\
\t\tVous pouvez bien évidement combiner un protocole réseaux avec un transport et un application.\
\tVous pouvez combiner pluisieurs filtres comme ceci: filtre1 && filtre2.\
")


		elif(buffer[:6] == "filtre"):
			filtre = TrameList.filtre(buffer[7:])
			if(len(filtre) == 0):
				print("aucune trame ne correspond au filtre")
			else:
				for i in filtre:
					i.afficher_info_imp()

				entree_non_correcte = True
				while entree_non_correcte:
					print("Voulez vous enregistrer l'analyse des trames filtrés ?(O/N) ", end="")
					yn = input()
					if(yn.upper() == "O" or yn.upper() == "OUI"):
						print("Comment voulez vous nommer le fichier ? ", end="")
						file_name = input()
						print("La voulez vous dans un fichier pdf ou texte ?(P/T) ", end="")
						pt = input()
						if(pt.upper() == "P" or pt.upper() == "PDF"):
							create_pdf(file_name, filtre)
							entree_non_correcte = False
						elif(pt.upper() == "T" or pt.upper() == "TEXTE"):
							enregistrer_texte(file_name, filtre)
							entree_non_correcte = False
						else:
							print("Malheureusement votre entrée est incorecte")
					elif(yn.upper() == "N" or yn.upper() == "NON"):
						entree_non_correcte = False
					else:
						print("Malheureusement votre entrée est incorecte")

		elif(buffer == "afficher"):
			TrameList.afficher_info_imp()

		elif(buffer[:8] == "afficher"):
			try:
				TrameList.printT(int(buffer[9:].replace("(", "").replace(" ", "").replace(")", ""), 10))
			except ValueError as ve:
				print(f"Vous avez entré {buffer[9:]} {[ve]}")

		elif(buffer == "exit()"):
			entree_non_correcte = True
			while entree_non_correcte:
				print("Voulez vous enregistrer l'analyse des trames ?(O/N) ", end="")
				yn = input()
				if(yn.upper() == "O" or yn.upper() == "OUI"):
					print("La voulez vous dans un fichier pdf ou texte ?(P/T) ", end="")
					pt = input()
					if(pt.upper() == "P" or pt.upper() == "PDF"):
						print("Comment voulez vous nommer le fichier ? ", end="")
						create_pdf(f"{input()}.pdf", TrameList.get_liste())
						entree_non_correcte = False
					elif(pt.upper() == "T" or pt.upper() == "TEXTE"):
						print("Comment voulez vous nommer le fichier ? ", end="")
						enregistrer_texte(f"{input()}.txt", TrameList.get_liste())
						entree_non_correcte = False
					else:
						print("Malheureusement votre entrée est incorecte")
				elif(yn.upper() == "N" or yn.upper() == "NON"):
					entree_non_correcte = False
				else:
					print("Malheureusement votre entrée est incorrecte")

			print("copyright Ethan et Paul le magicien")
			break

		else:
			print("Commande non comprises\nTapez /help pour voir les commandes dispo")

main()

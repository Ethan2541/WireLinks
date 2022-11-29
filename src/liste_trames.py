from trame import *

proto_reseaux = ["IPv4", "IPv6", "ARP"]
proto_reseaux_code = ["080", "86DD", "0806"]
proto_transport = ["ICMP", "TCP", "UDP", "IGMP", "EGP", "IGP", "XTP", "RSVP"]
proto_transport_code = ["06", "01","02", "08", "09", "11", "24", "2D"]
proto_application = ["HTTP", "HTTPS", "DNS", "DHCP", "SMTP", "IMAP", "POP", "SSH", "RDP", "FTP"]

class TrameList:
	liste_trames = []

	def __init__(self, trame):
		self.liste_trames.append(trame)

	def set_liste(new_list):
		TrameList.liste_trames = new_list

	def get_liste():
		return TrameList.liste_trames

	def filtre_ip_src(ip):
		liste_filtre = []
		for i in TrameList.liste_trames:
			if(i.get_ethernet().get_type_eth2() == "IPv4"):
				if(i.get_ip().get_src() == ip):
					liste_filtre.append(i)
			elif(i.get_ethernet().get_type_eth2() == "ARP"):
				if(i.get_ip().get_ip_src() == ip):
					liste_filtre.append(i)
		return liste_filtre

	def filtre_ip_dst(ip):
		liste_filtre = []
		for i in TrameList.liste_trames:
			if(i.get_ethernet().get_type_eth2() == "IPv4"):
				if(i.get_ip().get_dst() == ip):
					liste_filtre.append(i)
			elif(i.get_ethernet().get_type_eth2() == "ARP"):
				if(i.get_ip().get_ip_dst() == ip):
					liste_filtre.append(i)
		return liste_filtre

	def filtre_port_src(port):
		liste_filtre = []
		for i in TrameList.liste_trames:
			try:
				if(i.get_ethernet().get_type_eth2() == "IPv4"):
					if(i.get_ip().get_proto2() == "TCP" or i.get_ip().get_proto2() == "UDP"):
						if(int(i.get_transport().get_port_src(), 16) == int(port)):
							liste_filtre.append(i)
			except ValueError:
				print("Veillez entrer un nombre entier valide")
		return liste_filtre

	def filtre_port_dst(port):
		liste_filtre = []
		for i in TrameList.liste_trames:
			try:
				if(i.get_ethernet().get_type_eth2() == "IPv4"):
					if(i.get_ip().get_proto2() == "TCP" or i.get_ip().get_proto2() == "UDP"):
						if(int(i.get_transport().get_port_dst(), 16) == int(port)):
							liste_filtre.append(i)
			except ValueError:
				print("Veillez entrer un nombre entier valide")
		return liste_filtre

	def filtre_mac_src(mac):
		liste_filtre = []
		for i in TrameList.liste_trames:
			if(i.get_ethernet().get_src() == mac):
				liste_filtre.append(i)
		return liste_filtre

	def filtre_mac_dst(mac):
		liste_filtre = []
		for i in TrameList.liste_trames:
			if(i.get_ethernet().get_dst() == mac):
				liste_filtre.append(i)
		return liste_filtre

	def filtre_protcole_reseaux(protocole):
		liste_filtre = []
		for i in TrameList.liste_trames:
			if(i.get_ip().get_typ() == protocole.upper()):
				liste_filtre.append(i)
		return liste_filtre

	def filtre_protcole_reseaux_code(protocole):
		liste_filtre = []
		for i in TrameList.liste_trames:
			if(i.get_ethernet().get_type_eth2() == protocole.upper()):
				liste_filtre.append(i)
		return liste_filtre

	def filtre_protcole_transport(protocole):
		liste_filtre = []
		for i in TrameList.liste_trames:
			if(i.get_transport() != None and i.get_transport().get_typ() == protocole.upper()):
				liste_filtre.append(i)
		return liste_filtre

	def filtre_protcole_transport_code(protocole):
		liste_filtre = []
		for i in TrameList.liste_trames:
			if(i.get_ip().get_proto() == protocole.upper()):
				liste_filtre.append(i)
		return liste_filtre

	def filtre_protcole_application(protocole):
		liste_filtre = []
		for i in TrameList.liste_trames:
			if(i.get_transport().get_appli() == protocole.upper()):
				liste_filtre.append(i)
		return liste_filtre

	def intersection(lst1, lst2):
		return list(set(lst1) & set(lst2))

	def exclu(lst1, lst2):
		return list(set(lst1) - set(lst2))

	def union(lst1, lst2):
		return list(set(lst1).union(set(lst2)))

	def filtre(str_filtre):
		str_filtre.replace("\"", "")
		str_filtre.replace("(", "")
		str_filtre.replace(")", "")
		str_filtre.replace(" ", "")
		liste_filtre = TrameList.liste_trames
		liste_filtre_tmp = []
		taille_str = len(str_filtre)
		debut_filtre = 0
		debut_attribut = 0
		fin_attribut = 0
		i = 0
		while i < taille_str:
			while i < taille_str:
				if(str_filtre[i:i+2] == "==" or str_filtre[i:i+2] == "!=" or str_filtre[i:i+2] == "<>"):
					filtre = str_filtre[debut_filtre:i]
					operat = str_filtre[i:i+2]
					debut_attribut = i+2
					i += 2
					break	
			
				elif(i >= taille_str-1):
					i += 1

				else:
					i += 1

			while i < taille_str:
				if(i == taille_str-1 or str_filtre[i:i+2] == "&&" or str_filtre[i:i+2] == "||"):
					if(i != taille_str-1):
						attribut = str_filtre[debut_attribut:i]
						concat = str_filtre[i:i+2]
					else:
						attribut = str_filtre[debut_attribut:i+1]
						concat = "fin"
					debut_filtre = i+4
					print(concat)
					break
			
				i += 1

			if(i >= taille_str):
				break

			elif(filtre.lower() == "ip.src"):
				liste_filtre_tmp = TrameList.filtre_ip_src(attribut)
				print(attribut)
				print("je suis l'ip.src")
				print(len(liste_filtre_tmp))

			elif(filtre.lower() == "ip.dst"):
				liste_filtre_tmp = TrameList.filtre_ip_dst(attribut)

			elif(filtre.lower() == "port.src"):
				liste_filtre_tmp = TrameList.filtre_port_src(attribut)

			elif(filtre.lower() == "port.dst"):
				liste_filtre_tmp = TrameList.filtre_port_dst(attribut)

			elif(filtre.lower() == "mac.src"):
				liste_filtre_tmp = TrameList.filtre_mac_src(attribut)

			elif(filtre.lower() == "mac.dst"):
				liste_filtre_tmp = TrameList.filtre_mac_dst(attribut)

			elif(filtre.lower() == "proto"):

				if(attribut.upper() in proto_reseaux or (attribut[:2].upper() == "0X" and attribut[2:] in proto_reseaux_code)):

					if(attribut.upper() in proto_reseaux):
						liste_filtre_tmp = TrameList.filtre_protcole_reseaux(attribut)
					
					elif(attribut[2:] in proto_reseaux_code):
						liste_filtre_tmp = TrameList.filtre_protcole_reseaux_code(attribut)

					else:
						print("Ce protocole n'est malheureusement pas supporté: ", attribut)
    						
				elif(attribut.upper() in proto_transport or (attribut[:2].upper() == "0X" and attribut[2:] in proto_reseaux_code)):

					if(attribut.upper() in proto_transport):
						liste_filtre_tmp = TrameList.filtre_protcole_transport(attribut)

					elif(attribut[2:] in proto_transport_code):
						liste_filtre_tmp = TrameList.filtre_protcole_transport_code(attribut)

					elif(attribut.upper() in proto_application):
						liste_filtre_tmp = TrameList.filtre_protcole_application(attribut)

					else:
						print("Ce protocole n'est malheureusement pas supporté: ", attribut)
						i += 3
						continue

			else:
				print("Filtre non reconnu. Regardez le filtres disponibles dans la doc")
				return []

			if(operat == "=="):
				if(concat == "&&"):
					liste_filtre = TrameList.intersection(liste_filtre, liste_filtre_tmp)
				elif(concat == "||"):
					liste_filtre = TrameList.union(liste_filtre, liste_filtre_tmp)
				elif(concat == "fin"):
					liste_filtre = TrameList.intersection(liste_filtre, liste_filtre_tmp)
				else:
					print("erreur d'opération")
				i += 3

			elif(operat == "<>" or operat == "!="):
				if(concat == "&&"):
					liste_filtre = TrameList.intersection(liste_filtre, liste_filtre_tmp)
				elif(concat == "||"):
					liste_filtre = TrameList.union(liste_filtre, liste_filtre_tmp)
				elif(concat == "fin"):
					liste_filtre = TrameList.intersection(liste_filtre, liste_filtre_tmp)
				else:
					print("erreur d'opération")
				i += 3
			
			else:
				print("Filtre non reconnu. Regardez le filtres disponibles dans la doc")
				return []

		return liste_filtre

	def afficher():
		if(len(TrameList.get_liste()) == 0):
			print("Trace vide")
		else:
			for i in TrameList.get_liste():
				print(i)

	def afficher_info_imp():
		if(len(TrameList.get_liste()) == 0):
			print("Trace vide")
		else:
			for i in TrameList.get_liste():
				i.afficher_info_imp()

	"""def afficher_info_imp_gui():
		if(len(TrameList.get_liste()) == 0):
			print("Trace vide")
		else:
			for i in TrameList.get_liste():
				return i.afficher_info_imp_gui())"""


	def get_trame(iden):
		if(iden <= len(TrameList.get_liste())):
			return TrameList.get_liste()[iden-1]

	def printT(iden):
		if(iden <= len(TrameList.get_liste())):
			print(TrameList.get_liste()[iden-1])
		else:
			print("Identifiant non existant")
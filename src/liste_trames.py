from tkinter import messagebox as mb
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



	# MAC Filters
	def filtre_mac_src(mac):
		liste_filtre = []

		for i in TrameList.liste_trames:
			if (i.get_ethernet().get_src() == mac):
				liste_filtre.append(i)

		return liste_filtre


	def filtre_mac_dst(mac):
		liste_filtre = []

		for i in TrameList.liste_trames:
			if (i.get_ethernet().get_dst() == mac):
				liste_filtre.append(i)

		return liste_filtre



	# IP Filters
	def filtre_ip_src(ip):
		liste_filtre = []

		for i in TrameList.liste_trames:

			if (i.get_ethernet().get_type_eth2() == "IPv4"):
				if (i.get_ip().get_src() == ip):
					liste_filtre.append(i)

			elif (i.get_ethernet().get_type_eth2() == "ARP"):
				if (i.get_ip().get_ip_src() == ip):
					liste_filtre.append(i)

		return liste_filtre


	def filtre_ip_dst(ip):
		liste_filtre = []
		for i in TrameList.liste_trames:
			if (i.get_ethernet().get_type_eth2() == "IPv4"):
				if (i.get_ip().get_dst() == ip):
					liste_filtre.append(i)

			elif (i.get_ethernet().get_type_eth2() == "ARP"):
				if (i.get_ip().get_ip_dst() == ip):
					liste_filtre.append(i)
		return liste_filtre



	# Port Filters
	def filtre_port_src(port):
		liste_filtre = []

		for i in TrameList.liste_trames:
			try:
				if (i.get_ethernet().get_type_eth2() == "IPv4"):
					if (i.get_ip().get_proto2() == "TCP" or i.get_ip().get_proto2() == "UDP"):
						if (int(i.get_transport().get_port_src(), 16) == int(port)):
							liste_filtre.append(i)

			except ValueError:
				mb.showerror("Error", "Please enter a valid number")

		return liste_filtre


	def filtre_port_dst(port):
		liste_filtre = []

		for i in TrameList.liste_trames:
			try:
				if (i.get_ethernet().get_type_eth2() == "IPv4"):
					if (i.get_ip().get_proto2() == "TCP" or i.get_ip().get_proto2() == "UDP"):
						if (int(i.get_transport().get_port_dst(), 16) == int(port)):
							liste_filtre.append(i)

			except ValueError:
				mb.showerror("Error", "Please enter a valid number")

		return liste_filtre



	# Protocol Filters
	def filtre_protocole_reseaux(protocole):
		liste_filtre = []

		for i in TrameList.liste_trames:
			if (i.get_ip().get_typ() == protocole.upper()):
				liste_filtre.append(i)

		return liste_filtre


	def filtre_protocole_reseaux_code(protocole):
		liste_filtre = []

		for i in TrameList.liste_trames:
			if(i.get_ethernet().get_type_eth2() == protocole.upper()):
				liste_filtre.append(i)

		return liste_filtre


	def filtre_protocole_transport(protocole):
		liste_filtre = []
		for i in TrameList.liste_trames:
			if (i.get_transport() != None and i.get_transport().get_typ() == protocole.upper()):
				liste_filtre.append(i)
		return liste_filtre


	def filtre_protocole_transport_code(protocole):
		liste_filtre = []
		for i in TrameList.liste_trames:
			if (i.get_ip().get_proto() == protocole.upper()):
				liste_filtre.append(i)
		return liste_filtre


	def filtre_protocole_application(protocole):
		liste_filtre = []
		for i in TrameList.liste_trames:
			if (i.get_transport().get_appli() == protocole.upper()):
				liste_filtre.append(i)
		return liste_filtre



	# Sets Operations
	def intersection(lst1, lst2):
		return list(set(lst1) & set(lst2))

	def exclu(lst1, lst2):
		return list(set(lst1) - set(lst2))

	def union(lst1, lst2):
		return list(set(lst1).union(set(lst2)))



	# Filters Handling
	def filtre(str_filtre):
		str_filtre = str_filtre.replace("\"", "")
		str_filtre = str_filtre.replace("(", "")
		str_filtre = str_filtre.replace(")", "")
		str_filtre = str_filtre.replace(" ", "")

		liste_filtre = TrameList.liste_trames
		liste_filtre_tmp = []

		taille_str = len(str_filtre)

		debut_filtre = 0
		debut_attribut = 0
		fin_attribut = 0
		next_concat = ""
		concat = ""
		i = 0


		# Parser
		while i < taille_str:
			concat = next_concat

			while i < taille_str:

				if (str_filtre[i:i+2] == "==" or str_filtre[i:i+2] == "!=" or str_filtre[i:i+2] == "<>"):
					filtre = str_filtre[debut_filtre:i]
					operat = str_filtre[i:i+2]
					debut_attribut = i+2
					i += 2
					break	
			
				elif (i >= taille_str-1):
					i += 1

				else:
					i += 1


			while i < taille_str:

				if (i == taille_str-1 or str_filtre[i+1:i+3] == "&&" or str_filtre[i+1:i+3] == "||"):
					attribut = str_filtre[debut_attribut:i+1]

					if (i != taille_str-1):
						next_concat = str_filtre[i+1:i+3]
					else:
						next_concat = ""
					debut_filtre = i+3
					break
			
				i += 1


			# Type of Filter
			if (i >= taille_str):
				break

			elif (filtre.lower() == "ip.src"):
				liste_filtre_tmp = TrameList.filtre_ip_src(attribut)

			elif (filtre.lower() == "ip.dst"):
				liste_filtre_tmp = TrameList.filtre_ip_dst(attribut)

			elif (filtre.lower() == "port.src"):
				liste_filtre_tmp = TrameList.filtre_port_src(attribut)

			elif (filtre.lower() == "port.dst"):
				liste_filtre_tmp = TrameList.filtre_port_dst(attribut)

			elif (filtre.lower() == "mac.src"):
				liste_filtre_tmp = TrameList.filtre_mac_src(attribut)

			elif (filtre.lower() == "mac.dst"):
				liste_filtre_tmp = TrameList.filtre_mac_dst(attribut)

			elif (filtre.lower() == "proto"):

				if(attribut.upper() in proto_reseaux or (attribut[:2].upper() == "0X" and attribut[2:] in proto_reseaux_code)):

					if (attribut.upper() in proto_reseaux):
						liste_filtre_tmp = TrameList.filtre_protocole_reseaux(attribut)
					
					elif (attribut[2:] in proto_reseaux_code):
						liste_filtre_tmp = TrameList.filtre_protocole_reseaux_code(attribut)

					else:
						mb.showerror("Error", "Invalid Protocol: ", attribut)
    						
				elif (attribut.upper() in proto_transport or (attribut[:2].upper() == "0X" and attribut[2:] in proto_reseaux_code)):

					if (attribut.upper() in proto_transport):
						liste_filtre_tmp = TrameList.filtre_protocole_transport(attribut)
					elif (attribut[2:] in proto_transport_code):
						liste_filtre_tmp = TrameList.filtre_protocole_transport_code(attribut)
					elif (attribut.upper() in proto_application):
						liste_filtre_tmp = TrameList.filtre_protocole_application(attribut)
					else:
						mb.showerror("Error", "Invalid Protocol: ", attribut)
						i += 3
						continue

			else:
				mb.showerror("Error", "The filter you have typed is not valid")
				return []


			# Operator ==
			if(operat == "=="):
				if (concat == "&&" or concat == ""):
					liste_filtre = TrameList.intersection(liste_filtre, liste_filtre_tmp)

				elif (concat == "||"):
					liste_filtre = TrameList.union(liste_filtre, liste_filtre_tmp)

				else:
					mb.showerror("Error", "Operation not supported")
				i += 3


			# Operator != and <>
			elif(operat == "<>" or operat == "!="):
				if (concat == "&&" or concat == ""):
					liste_filtre = TrameList.intersection(liste_filtre, TrameList.exclu(liste_filtre, liste_filtre_tmp))

				elif (concat == "||"):
					liste_filtre = TrameList.union(liste_filtre, TrameList.exclu(liste_filtre, liste_filtre_tmp))

				else:
					mb.showerror("Error", "Operation not supported")
				i += 3

		return liste_filtre
	


	def afficher_info_imp_gui():
		if (len(TrameList.get_liste()) == 0):
			mb.showinfo("Info", "Empty File or No Valid Frame was Found")

		else:
			for i in TrameList.get_liste():
				return i.afficher_info_imp_gui()



	def get_trame(iden):
		if (iden <= len(TrameList.get_liste())):
			return TrameList.get_liste()[iden-1]
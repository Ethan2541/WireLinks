from ethernet import *
from reseau.ip import *
from reseau.arp import *
from transport.tcp import *
from transport.udp import *
from transport.icmp import *
from transport.igmp import *
from application.httpm import *
from exceptions import *

class Trame:
	"""Classe contenant la trame.
	Chaque couche de la trame correspond à un objet.
	"""
	def __init__(self, iden, trame):
		self.iden = iden
		self.taille = len(trame)/2
		self.ethernet = Ethernet(trame)
		if(self.ethernet.get_type_eth2() == "IPV4"):
			self.ip = Ip(self.ethernet.get_data(), self.ethernet.get_type_eth2())

			if(self.ip.get_data() != None):

				if(self.ip.get_proto2() == "TCP"):
					self.transport = Tcp(self.ip.get_proto2(), self.ip.get_data())

					if(self.transport.get_data() != None):

						if(self.transport.get_appli() == "HTTP"):
							self.http = Http(self.transport.get_data())

							if(self.http.get_data() != None):
								self.data = self.http.get_data()

							else:
								self.data = None

						else:
							self.http = None
							if(self.transport.get_data() != None):
								self.data = self.transport.get_data()

					else:
						self.http = None
						self.data = None

				elif(self.ip.get_proto2() == "UDP"):
					self.transport = Udp(self.ip.get_proto2(), self.ip.get_data())

					if(self.transport.get_data() != None):

						if(self.transport.get_appli() == "HTTP"):
							self.http = Http(self.transport.get_data())

							if(self.http.get_data() != None):
								self.data = self.http.get_data()

							else:
								self.data = None

						else:
							self.http = None
							if(self.transport.get_data() != None):
								self.data = self.transport.get_data()

					else:
						self.http = None
						self.data = None

				elif(self.ip.get_proto2() == "ICMP"):
					self.transport = Icmp(self.ip.get_proto2(), self.ip.get_data())
					if(self.transport.get_data() != None and self.transport.get_data() != ""):
						self.data = self.transport.get_data()
					self.http = None

				elif(self.ip.get_proto2() == "IGMP"):
					self.transport = Igmp(self.ip.get_proto2(), self.ip.get_data())
					if(self.transport.get_data() != None and self.transport.get_data() != ""):
						self.data = self.transport.get_data()
					self.http = None
					
				else:
					
					erreur_type("transport", self.ip.get_proto2(), self.iden)
					self.transport = None
					self.http = None
					self.data = None

			else:
				self.transport = None
				self.http = None
				self.data = None

		elif(self.ethernet.get_type_eth2() == "ARP"):
			self.ip = Arp(self.ethernet.get_data(), self.ethernet.get_type_eth2())
			self.transport = None
			self.http = None
			self.data = None
		elif(self.ethernet.get_type_eth2() == "RARP"):
			self.ip = Arp(self.ethernet.get_data(), self.ethernet.get_type_eth2())
			self.transport = None
			self.http = None
			self.data = None

		else:
			erreur_type("réseau", self.ethernet.get_type_eth2(), self.iden)
			self.ip = None
			self.transport = None
			self.http = None
			self.data = None

	def get_iden(self):
		return self.iden

	def get_taille(self):
		return self.taille

	def get_ethernet(self):
		return self.ethernet

	def get_ip(self):
		return self.ip

	def get_transport(self):
		return self.transport

	def get_http(self):
		return self.http

	def get_data(self):
		return self.data

	def afficher_info_imp(self):
		if(self.ip != None and self.ethernet.get_type_eth2() == "IPV4"):
			chaine = f"{self.get_iden()} ({int(self.get_taille())}octets): {self.get_ip().get_src()}\
------->{self.get_ip().get_dst()}\n"
			for j in range(len(chaine)):
				if(chaine[j] == ">"):
					chaine += (j-5) * " " + self.get_ip().get_proto2()
					break
			print(chaine)
		
		elif(self.ip != None and self.ethernet.get_type_eth2() == "ARP"):
			chaine = f"{self.get_iden()} ({int(self.get_taille())}octets): {self.get_ip().get_ip_src()}\
------->{self.get_ip().get_ip_dst()}\n"
			for j in range(len(chaine)):
				if(chaine[j] == ">"):
					chaine += (j-5) * " " + "ARP"
					break
			print(chaine)

		else:
			print("Trame numéro ",self.iden, "non lisible")

	def afficher_info_imp_gui(self):
		chaine = ""
		if(self.ethernet != None):
			chaine += "  #{0:04d}     {1:<20}     {2:<20}".format(self.iden, self.ethernet.get_src(), self.ethernet.get_dst())
			if(self.ip != None and self.ethernet.get_type_eth2() == "IPV4"):
				chaine += "     {0:<18}     {1:<18}".format(self.ip.get_src(), self.ip.get_dst())
				if(self.transport != None and self.ip.get_proto2() == "TCP" or self.ip.get_proto2() == "UDP"):
					chaine += "     {0:<9}     {1:<8}    {2:<9}".format(self.transport.get_port_src(), self.transport.get_port_dst(), self.ip.get_proto2())
				else:
					chaine += "            {0:<9}".format(self.ip.get_proto2())

			elif(self.ip != None and self.ethernet.get_type_eth2() == "ARP" or self.ethernet.get_type_eth2() == "RARP"):
				chaine += "     {0:<18}     {1:<18}           {2:<18}".format(self.ip.get_ip_src(), self.ip.get_ip_dst(), self.ethernet.get_type_eth2())
			return chaine
		else:
			return f"Trame numéro {self.iden} non lisible"

	def __str__(self):
		chaine =  f"Trame numéro {self.iden} (taille: {int(self.taille)}octets)\
		\n{str(self.ethernet)}"
		if(self.ip != None):
			chaine += f"\n{str(self.ip)}\n"

		if(self.transport != None):
			chaine += f"\n{str(self.transport)}\n"

		if(self.http != None):
			chaine += f"\n{str(self.http)}\n"

		if(self.data != None):
			chaine += f"\nData:\n{self.data}\n" 

		return chaine


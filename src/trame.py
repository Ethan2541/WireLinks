from ethernet import *
from ip import *
from arp import *
from tcp import *
from udp import *
from icmp import *
from igmp import *
from httpm import *

class Trame:
	"""Frame Object Class.
	Each layer is associated to an OSI-layer.
	"""

	def __init__(self, iden, trame):
		self.iden = iden
		self.taille = len(trame)/2
		self.ethernet = Ethernet(trame)

		if (self.ethernet.get_type_eth2() == "IPv4"):
			self.ip = Ip(self.ethernet.get_data(), self.ethernet.get_type_eth2())

			# IP
			if (self.ip.get_data() != None):

				# TCP
				if (self.ip.get_proto2() == "TCP"):
					self.transport = Tcp(self.ip.get_proto2(), self.ip.get_data())

					if (self.transport.get_data() != None):

						# HTTP within TCP segment
						if (self.transport.get_appli() == "HTTP"):
							self.http = Http(self.transport.get_data())

							if (self.http.get_data() != None):
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


				# UDP
				elif (self.ip.get_proto2() == "UDP"):
					self.transport = Udp(self.ip.get_proto2(), self.ip.get_data())

					if (self.transport.get_data() != None):

						# HTTP within UDP datagram
						if (self.transport.get_appli() == "HTTP"):
							self.http = Http(self.transport.get_data())

							if (self.http.get_data() != None):
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


				# ICMP
				elif (self.ip.get_proto2() == "ICMP"):
					self.transport = Icmp(self.ip.get_proto2(), self.ip.get_data())

					if (self.transport.get_data() != None and self.transport.get_data() != ""):
						self.data = self.transport.get_data()
					self.http = None


				# IGMP
				elif (self.ip.get_proto2() == "IGMP"):
					self.transport = Igmp(self.ip.get_proto2(), self.ip.get_data())

					if (self.transport.get_data() != None and self.transport.get_data() != ""):
						self.data = self.transport.get_data()
					self.http = None
					

				else:
					# type_error("Transport", self.ip.get_proto2(), self.iden)
					self.transport = None
					self.http = None
					self.data = None

			else:
				self.transport = None
				self.http = None
				self.data = None

		elif (self.ethernet.get_type_eth2() == "ARP"):

			self.ip = Arp(self.ethernet.get_data(), self.ethernet.get_type_eth2())
			self.transport = None
			self.http = None
			self.data = None


		elif (self.ethernet.get_type_eth2() == "RARP"):
			self.ip = Arp(self.ethernet.get_data(), self.ethernet.get_type_eth2())
			self.transport = None
			self.http = None
			self.data = None


		else:
			# type_error("Network", self.ethernet.get_type_eth2(), self.iden)
			self.ip = None
			self.transport = None
			self.http = None
			self.data = None


		if self.data != None:
			self.data = "Data:\n\n" + self.data



	# Getters
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



	def afficher_info_imp_gui(self):
		fixedlen = 25
		chaine = ""
		if (self.ethernet != None):
			chaine += ("   {:<4d}" + (8 - len(str(self.iden))) * " " + "{:<20s}" + (fixedlen - len(self.ethernet.get_src())) * " " + "{:<20s}" + (fixedlen - len(self.ethernet.get_dst())) * " ").format(self.iden, self.ethernet.get_src(), self.ethernet.get_dst())
			
			if (self.ip != None and self.ethernet.get_type_eth2() == "IPv4"):
				chaine += ("{:<15s}" + (fixedlen - len(self.ip.get_src())) * " " + "{:<15s}" + (fixedlen - len(self.ip.get_dst())) * " ").format(self.ip.get_src(), self.ip.get_dst())
				
				if (self.transport != None and self.ip.get_proto2() == "TCP" or self.ip.get_proto2() == "UDP"):
					chaine += ("{:<10s}" + (fixedlen - len(self.ip.get_proto2())) * " " + "{:<8d}" + (fixedlen - len(str(int(self.transport.get_port_src(), 16)))) * " " + "{:<8d}" + (fixedlen - len(str(int(self.transport.get_port_dst(), 16)))) * " ").format(self.ip.get_proto2(), int(self.transport.get_port_src(), 16), int(self.transport.get_port_dst(), 16))
					chaine += "Len={} ".format(int(self.get_taille()))

					if (self.ip.get_proto2() == "TCP"):
						if(self.transport.get_syn() == "1"):
							chaine += "SYN "
						if(self.transport.get_ack() == "1"):
							chaine += "ACK "
						if(self.transport.get_fin() == "1"):
							chaine += "FIN "
						if(self.transport.get_psh() == "1"):
							chaine += "PSH "
						if(self.transport.get_urg() == "1"):
							chaine += "URG "
						if(self.transport.get_rst() == "1"):
							chaine += "RST "

						chaine += "Seq=0x{} Ack=0x{}".format(self.transport.get_seq_num(), self.transport.get_ack_num())

					if (self.http != None):
						chaine += f"  {self.http.get_version() } "

						if (self.http.get_method() == None):
							chaine += f"{self.http.get_code()} {self.http.get_msg()}"

						else:
							chaine += f"{self.http.get_method()} {self.http.get_url()}"


				elif (self.transport != None and self.transport.get_typ()=="ICMP"):
					chaine += ("{:<10s}" + (fixedlen - len(self.ip.get_proto2())) * " ").format(self.ip.get_proto2())
					chaine += (2 * fixedlen + 15) * " "
					chaine += "Len={}".format(int(self.get_taille()))

					chaine += f"   {self.transport.get_typ_icmp2()}   "

					if (self.transport.get_typ_icmp() == "08" or self.transport.get_typ_icmp() == "00" or self.transport.get_typ_icmp() == "11" or self.transport.get_typ_icmp() == "12" or self.transport.get_typ_icmp() == "0D" or self.transport.get_typ_icmp() == "0E"):
						if (self.transport.get_typ_icmp() == "08" or self.transport.get_typ_icmp() == "00"):
							chaine += " (ping)"

						elif (self.transport.get_typ_icmp() == "11" or self.transport.get_typ_icmp() == "12"):
								chaine += f" Mask={int(self.transport.get_subnet_mask()[:2], 16)}.{int(self.transport.get_subnet_mask()[2:4], 16)}.{int(self.transport.get_subnet_mask()[4:6], 16)}.{int(self.transport.get_subnet_mask()[6:8], 16)}"

						elif (self.transport.get_typ_icmp() == "0D" or self.transport.get_typ_icmp() == "0E"):
								chaine += f" Original TimeStamp={int(self.transport.get_orig_timestamp(), 16)}  Received TimeStamp={int(self.transport.get_recv_timestamp(), 16)}\
										Transport Timstamp={int(self.transport.get_tran_timestamp(), 16)}"

						chaine += f"   ID=0x{self.transport.get_id()}   Seq=0x{self.transport.get_seq_num()}  TTL={self.ip.get_ttl()}"

				elif (self.transport != None and self.transport.get_typ()=="IGMP"):
					chaine += ("{:<10s}" + (fixedlen - len(self.ip.get_proto2())) * " ").format(self.ip.get_proto2())
					chaine += (2 * fixedlen + 15) * " "
					chaine += "Len={}".format(int(self.get_taille()))

					chaine += f"  IGMP {self.transport.get_type_igmp2()}  Address: {self.transport.get_class_ip()}"

				else:
					chaine += ("{:<10s}" + (fixedlen - len(self.ip.get_proto2())) * " ").format(self.ip.get_proto2())
					chaine += (2 * fixedlen + 15) * " "
					chaine += "Len={}".format(int(self.get_taille()))

			elif (self.ip != None and self.ethernet.get_type_eth2() == "ARP" or self.ethernet.get_type_eth2() == "RARP"):
				chaine += ("{:<15s}" + (fixedlen - len(self.ip.get_ip_src())) * " " + "{:<15s}" + (fixedlen - len(self.ip.get_ip_dst())) * " " + "{:<10s}" + (fixedlen - len(self.ethernet.get_type_eth2())) * " ").format(self.ip.get_ip_src(), self.ip.get_ip_dst(), self.ethernet.get_type_eth2())
				chaine += (2 * fixedlen + 15) * " "

				if (self.ip.get_op() == "0001"):
					chaine += f" Who has {self.ip.get_ip_dst()}? Tell {self.ip.get_ip_src()} "

				elif (self.ip.get_op() == "0002"):
					chaine += f" {self.ip.get_ip_src()} is at {self.ip.get_eth_src()} "

				chaine += "Len={}".format(int(self.get_taille()))

		else:
			return f"Frame #{self.iden:04} Unreadable"

		return chaine



	def flow_graph(self):
		chaine = ""
		if (self.ip != None and self.ip.typ=="IPv4"):
			chaine = f"{self.iden}  {self.ip.get_src()} -------"
			
			if (self.transport != None and self.transport.get_typ() == "TCP"):
				chaine += " |"
				if (self.http != None):
						chaine += f"{self.http.get_version() } "

						if (self.http.get_method() == None):
							chaine += f"{self.http.get_code()} {self.http.get_msg()} "

						else:
							chaine += f"{self.http.get_method()} {self.http.get_url()} "

				else:
					chaine += "TCP "

				chaine += f"{str(int(self.transport.get_port_src(), 16))} -> {str(int(self.transport.get_port_dst(), 16))} Len={str(int(self.transport.get_thl(), 16) * 4)}"
				
				if(self.transport.get_syn() == "1"):
					chaine += " SYN "
				if(self.transport.get_ack() == "1"):
					chaine += " ACK "
				if(self.transport.get_fin() == "1"):
					chaine += " FIN "
				if(self.transport.get_psh() == "1"):
					chaine += " PSH "
				if(self.transport.get_urg() == "1"):
					chaine += " URG "
				if(self.transport.get_rst() == "1"):
					chaine += " RST "
				chaine += f" Seq=0x{int(self.transport.get_seq_num(), 16)} Ack=0x{int(self.transport.get_ack_num(), 16)}| "

			elif (self.transport != None and self.transport.get_typ() == "UDP"):
				chaine += " |"

				if (self.http != None):
						chaine += f"{self.http.get_version() } "

						if (self.http.get_method() == None):
							chaine += f"{self.http.get_code()} {self.http.get_msg()} "

						else:
							chaine += f"{self.http.get_method()} {self.http.get_url()} "

				else:
					chaine += "UDP "
				chaine += f"{str(int(self.transport.get_port_src(), 16))} -> {str(int(self.transport.get_port_dst(), 16))} "
				chaine += f"Len={str(int(self.transport.get_length(), 16))}| "

			elif (self.transport != None and self.transport.get_typ()=="ICMP"):
				chaine += " |"
				chaine += f"ICMP {self.transport.get_typ_icmp2()}"
				if(self.transport.get_typ_icmp() == "08" or self.transport.get_typ_icmp() == "00" or self.transport.get_typ_icmp() == "11" or self.transport.get_typ_icmp() == "12" or self.transport.get_typ_icmp() == "0D" or self.transport.get_typ_icmp() == "0E"):
					if(self.transport.get_typ_icmp() == "08" or self.transport.get_typ_icmp() == "00"):
						chaine += " (ping)  "
					elif(self.transport.get_typ_icmp() == "11" or self.transport.get_typ_icmp() == "12"):
							chaine += " Mask={self.transport.get_subnet_mask()}"
					elif(self.transport.get_typ_icmp() == "0D" or self.transport.get_typ_icmp() == "0E"):
							chaine += " Original TimeStap={self.transport.get_orig_timestap()}  Received TimeStap={self.transport.get_recv_timestap()}\
									Transport Timstamp={self.transport.get_tran_timestamsp()}"
					chaine += "id=0x{self.transport.get_id()}   seq={self.transport.get_seq_num()}  ttl={self.ip.get_ttl()}"

				chaine += "  | "

			elif (self.transport != None and self.transport.get_typ()=="IGMP"):
				chaine += " |"
				chaine += f"IGMP"
				chaine += "| "
			
			chaine += f"-------> {self.ip.get_dst()}"

		elif (self.ip != None and self.ip.get_typ() == "ARP"):
			chaine += f"{self.iden}  {self.ip.get_ip_src()} -------"
			chaine += " |"
			chaine += f"ARP Type={self.ip.get_op2()}"

			if (self.ip.get_op() == "0001"):
				chaine += f" Who has {self.ip.get_ip_dst()}? Tell {self.ip.get_ip_src()}"

			elif (self.ip.get_op() == "0002"):
				chaine += f" {self.ip.get_ip_src()} is at {self.ip.get_eth_src()}"

			chaine += f"| -------> {self.ip.get_ip_dst()}"

		return chaine



	# String
	def __str__(self):
		chaine =  f"Length: {int(self.taille)} bytes)\
		\n{str(self.ethernet)}"
		if(self.ip != None):
			chaine += f"\n{str(self.ip)}\n"

		if(self.transport != None):
			chaine += f"\n{str(self.transport)}\n"

		if(self.http != None):
			chaine += f"\n{str(self.http)}\n"

		if(self.data != None):
			chaine += f"\n{str(self.data)}\n" 

		return chaine


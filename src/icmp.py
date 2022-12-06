from tcp import *
from udp import *
from ip import *

class Icmp:

	def __init__(self, typ, frame):
		# Parsing the default header fields
		self.typ = typ
		self.typ_icmp = frame[:2]
		self.code = frame[2:4]
		self.chk = frame[4:8]
		self.data = frame[8:]
		
		# Different Cases
		if ((self.typ_icmp == "08" or self.typ_icmp == "00") and self.code == "00"):
			self.id = frame[8:12]
			self.seq_num = frame[12:16]
			self.options = frame[16:]


		elif ((self.typ_icmp == "11" or self.typ_icmp == "12") and self.code == "00"):
			self.id = frame[8:12]
			self.seq_num = frame[12:16]
			self.subnet_mask = frame[16:24]


		elif ((self.typ_icmp == "0D" or self.typ_icmp == "0E") and self.code == "00"):
			self.id = frame[8:12]
			self.seq_num = frame[12:16]
			self.orig_timestap = frame[16:24]
			self.rec_timestap = frame[24:32]
			self.tran_timestap = frame[32:40]


		elif (self.typ_icmp == "03"):
			self.unused = frame[8:16]
			self.ip = Ip(frame[16:], "IPv4")

			if (self.ip.get_proto2() == "TCP"):
				self.transport = Tcp(self.ip.get_data())

			elif (self.ip.get_proto2() == "UDP"):
				self.transport = Udp(self.ip.get_data())


		elif (self.typ_icmp == "0B"):
			self.unused = frame[8:16]
			self.ip = Ip(frame[16:], "IPv4")

			if (self.ip.get_proto2() == "TCP"):
				self.transport = Tcp(self.ip.get_data())
			elif (self.ip.get_proto2() == "UDP"):
				self.transport = Udp(self.ip.get_data())

		self.determine_type()



	def determine_type(self):
		if (self.typ_icmp == "08"):
			self.typ_icmp2 = "Echo Request"

		elif (self.typ_icmp == "00"):
			self.typ_icmp2 = "Echo Reply"

		elif (self.typ_icmp == "11"):
			self.typ_icmp2 = "Address Mask Request"

		elif (self.typ_icmp == "12"):
			self.typ_icmp2 = "Address Mask Reply"

		elif (self.typ_icmp == "0D"):
			self.typ_icmp2 = "Timestamp"

		elif (self.typ_icmp == "0E"):
			self.typ_icmp2 = "Timestamp Reply"

		elif (self.typ_icmp == "03"):
			self.typ_icmp2 = "Destination Unreachable"

		elif (self.typ_icmp == "0B"):
			self.typ_icmp2 = "Time Exceeded"

		else:
			self.typ_icmp2 = "Type Inconnue"



	# Getters
	def get_typ(self):
		return self.typ

	def get_typ_icmp(self):
		return self.typ_icmp

	def get_typ_icmp2(self):
		return self.typ_icmp2

	def get_code(self):
		return self.code

	def get_chk(self):
		return self.chk

	def get_data(self):
		return self.data

	def get_id(self):
		return self.id

	def get_seq_num(self):
		return self.seq_num

	def get_options(self):
		return self.options

	def get_subnet_mask(self):
		return self.subnet_mask

	def get_orig_timestap(self):
		return self.orig_timestap

	def get_rec_timestap(self):
		return self.rec_timestap

	def get_tran_timestap(self):
		return self.tran_timestap

	def get_unused(self):
		return self.unused

	def get_ip(self):
		return self.ip

	def get_transport(self):
		self.transport



	# String
	def __str__(self):
		chaine = f"{self.typ}:\
		\n\tType: {self.typ_icmp2}({int(self.typ_icmp, 16)})\
		\n\tCode: {self.code}\
		\n\tChecksum: 0x{self.chk}"
		
		if ((self.typ_icmp == "08" or self.typ_icmp == "00") and self.code == "00"):
			chaine += f"\n\tIdentifier: 0x{self.id}\
			\n\tSequence Number: 0x{self.seq_num}"

			if (self.options != "" and self.options != None):
				chaine += f"\n\tOptions: {self.options}"

		elif ((self.typ_icmp == "11" or self.typ_icmp == "12") and self.code == "00"):
			chaine += f"\n\tIdentifier: 0x{self.id}\
			\n\tSequence Number: 0x{self.seq_num}\
			\n\tSubnet Mask: {int(self.subnet_mask[:2], 16)}.{int(self.subnet_mask[2:4], 16)}.{int(self.subnet_mask[4:6], 16)}.{int(self.subnet_mask[6:8], 16)}"
		
		elif ((self.typ_icmp == "0D" or self.typ_icmp == "0E") and self.code == "00"):
			chaine += f"\n\tIdentifier: 0x{self.id}\
			\n\tSequence Number: 0x{self.seq_num}\
			\n\tOriginal Timestamp: 0x{self.orig_timestap}\
			\n\tReceive Timestamp: 0x{self.orig_timestap}\
			\n\tTransport Timestamp: 0x{self.tran_timestap}"
		
		elif (self.typ_icmp == "03"):
			chaine += f"\n\tUnused: 0x{self.unused}\
			\n\tIP Header: {self.ip}"
			
			if (self.ip.get_proto2() == "TCP"):
				chaine += f"TCP: {self.transport}"
			elif (self.ip.get_proto2() == "UDP"):
				chaine += f"UDP: {self.transport}"

		return chaine
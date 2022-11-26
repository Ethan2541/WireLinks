import sys

sys.path.append("/home/alolop/fac/L3/LU3IN033/projet/code/reseau")
sys.path.append("/home/alolop/fac/L3/LU3IN033/projet/code/transport")

from ip import *
from tcp import *
from udp import *

class Icmp:
	def __init__(self, typ, trame):
		self.typ = typ
		self.typ_icmp = trame[:2]
		self.code = trame[2:4]
		self.chk = trame[4:8]
		self.data = trame[8:]
		
		if((self.typ_icmp == "08" or self.typ_icmp == "00") and self.code == "00"):
			self.id = trame[8:12]
			self.seq_num = trame[12:16]
			self.options = trame[16:]
		elif((self.typ_icmp == "11" or self.typ_icmp == "12") and self.code == "00"):
			self.id = trame[8:12]
			self.seq_num = trame[12:16]
			self.subnet_mask = trame[16:24]
		elif((self.typ_icmp == "0D" or self.typ_icmp == "0E") and self.code == "00"):
			self.id = trame[8:12]
			self.seq_num = trame[12:16]
			self.orig_timestap = trame[16:24]
			self.rec_timestap = trame[24:32]
			self.tran_timestap = trame[32:40]
		elif(self.typ_icmp == "03"):
			self.unused = trame[8:16]
			self.ip = Ip(trame[16:], "IPV4")
			if(self.ip.get_proto2() == "TCP"):
				self.transport = Tcp(self.ip.get_data())
			if(self.ip.get_proto2() == "UDP"):
				self.transport = Udp(self.ip.get_data())
		elif(self.typ_icmp == "0B"):
			self.unused = trame[8:16]
			self.ip = Ip(trame[16:], "IPV4")
			if(self.ip.get_proto2() == "TCP"):
				self.transport = Tcp(self.ip.get_data())
			elif(self.ip.get_proto2() == "UDP"):
				self.transport = Udp(self.ip.get_data())

		self.determine_type()

	def determine_type(self):
		if(self.typ_icmp == "08"):
			self.typ_icmp2 = "Echo"
		elif(self.typ_icmp == "00"):
			self.typ_icmp2 = "Echo Reply"
		elif(self.typ_icmp == "11"):
			self.typ_icmp2 = "Address Mask Request"
		elif(self.typ_icmp == "12"):
			self.typ_icmp2 = "Address Mask Reply"
		elif(self.typ_icmp == "0D"):
			self.typ_icmp2 = "Timestamp"
		elif(self.typ_icmp == "0E"):
			self.typ_icmp2 = "Timestamp Reply"
		elif(self.typ_icmp == "03"):
			self.typ_icmp2 = "Destination Unreachable"
		elif(self.typ_icmp == "0B"):
			self.typ_icmp2 = "Time Exceeded"

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
		if(self.id != None):
			return self.id
		return None

	def get_seq_num(self):
		if(self.seq_num != None):
			return self.seq_num
		return None

	def get_options(self):
		if(self.options != None):
			return self.options
		return None

	def get_subnet_mask(self):
		if(self.subnet_mask != None):
			return self.subnet_mask
		return None

	def get_orig_timestap(self):
		if(self.orig_timestap != None):
			return self.orig_timestap
		return None

	def get_rec_timestap(self):
		if(self.rec_timestap != None):
			return self.rec_timestap
		return None

	def get_tran_timestap(self):
		if(self.tran_timestap != None):
			return self.tran_timestap
		return None

	def get_unused(self):
		if(self.unused != None):
			return self.unused
		return None

	def get_ip(self):
		if(self.ip != None):
			return self.ip
		return None

	def get_transport(self):
		if(self.transport != None):
			return self.transport
		return None

	def __str__(self):
		chaine = f"{self.typ}:\
		\n\tType message: {self.typ_icmp2}({int(self.typ_icmp, 16)})\
		\n\tCode: {self.code}\
		\n\tChecksum: 0x{self.chk}"
		
		if((self.typ_icmp == "08" or self.typ_icmp == "00") and self.code == "00"):
			chaine += f"\n\tIdentifier: 0x{self.id}\
			\n\tSequence Number: 0x{self.seq_num}"
			if(self.options != "" and self.options != None):
				chaine += f"\n\tOptions: {self.options}"
		elif((self.typ_icmp == "11" or self.typ_icmp == "12") and self.code == "00"):
			chaine += f"\n\tIdentifier: 0x{self.id}\
			\n\tSequence Number: 0x{self.seq_num}\
			\n\tSubnet Mask: {int(self.subnet_mask[:2], 16)}.{int(self.subnet_mask[2:4], 16)}.{int(self.subnet_mask[4:6], 16)}.{int(self.subnet_mask[6:8], 16)}"
		elif((self.typ_icmp == "0D" or self.typ_icmp == "0E") and self.code == "00"):
			chaine += f"\n\tIdentifier: 0x{self.id}\
			\n\tSequence Number: 0x{self.seq_num}\
			\n\tOriginal Timestamp: 0x{self.orig_timestap}\
			\n\tReceive Timestamp: 0x{self.orig_timestap}\
			\n\tTransport Timestamp: 0x{self.tran_timestap}"
		elif(self.typ_icmp == "03"):
			chaine += f"\n\tUnused: 0x{self.unused}\
			\n\tIp Header: {self.ip}"
			if(self.ip.get_proto2() == "TCP"):
				chaine += f"Tcp: {self.transport}"
			elif(self.ip.get_proto2() == "UDP"):
				chaine += f"Tcp: {self.transport}"
		return chaine
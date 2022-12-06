class Arp:
	
	def __init__(self, frame, typ):
		self.typ = typ

		self.hard = frame[:4]
		self.prot = frame[4:8]

		self.hsize = frame[8:10]
		self.psize = frame[10:12]

		self.op = frame[12:16]

		self.eth_src = f"{frame[16:18]}:{frame[18:20]}:{frame[20:22]}:{frame[22:24]}:{frame[24:26]}:{frame[26:28]}"
		self.ip_src = f"{int(frame[28:30], 16)}.{int(frame[30:32], 16)}.{int(frame[32:34], 16)}.{int(frame[34:36], 16)}"
		
		self.eth_dst = f"{frame[36:38]}:{frame[38:40]}:{frame[40:42]}:{frame[42:44]}:{frame[44:46]}:{frame[46:48]}"
		self.ip_dst = f"{int(frame[48:50], 16)}.{int(frame[50:52], 16)}.{int(frame[52:54], 16)}.{int(frame[54:56], 16)}"


		if (self.op == "0001"):
			self.op2 = "Request"
		elif (self.op == "0002"):
			self.op2 = "Reply"
		elif (self.op == "0003"):
			self.op2 = "Request"
		elif (self.op == "0004"):
			self.op2 = "Reply"
		else:
			self.op2 = None


		if (self.hard == "0001"):
			self.hard2 = "Ethernet"
		elif (self.hard == "0002"):
			self.hard2 = "Experimental Ethernet"
		else:
			self.hard2 = "indéterminé"


		if (self.prot == "0800"):
			self.prot2 = "IPv4"
		elif (self.prot == "86DD"):
			self.prot2 = "IPv6"
		elif (self.prot == "0806"):
			self.prot2 = "ARP"
		elif (self.prot == "8035"):
			self.prot2 = "RARP"
		else:
			self.prot2 = "Unknown"



	# Getters
	def get_typ(self):
		return self.typ
	
	def get_hard(self):
		return self.hard

	def get_prot(self):
		return self.prot

	def get_prot2(self):
		return self.prot2

	def get_hsize(self):
		return self.hsize

	def get_psize(self):
		return self.psize

	def get_op(self):
		return self.op

	def get_op2(self):
		return self.op2

	def get_eth_src(self):
		return self.eth_src

	def get_ip_src(self):
		return self.ip_src

	def get_eth_dst(self):
		return self.eth_dst

	def get_ip_dst(self):
		return self.ip_dst



	# String
	def __str__(self):
		return f"{self.typ}:\
		\n\tHardware: {self.hard2}(0x{self.hard})\
		\n\tProtocol: {self.prot2}(0x{self.prot})\
		\n\tHardware Length: {int(self.hsize, 16)}\
		\n\tProtocol Length: {int(self.psize, 16)}\
		\n\tOperation: {self.op2}(0x{self.op})\
		\n\tSender Hardware Address: {self.eth_src}\
		\n\tSender Protocol Address: {self.ip_src}\
		\n\tTarget Hardware Address: {self.eth_dst}\
		\n\tTarget Protocol Address: {self.ip_dst}"
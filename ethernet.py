class Ethernet:
	def __init__(self, trame):
		self.dst = f"{trame[:2]}:{trame[2:4]}:{trame[4:6]}:{trame[6:8]}:{trame[8:10]}:{trame[10:12]}"
		self.src = f"{trame[12:14]}:{trame[14:16]}:{trame[16:18]}:{trame[18:20]}:{trame[20:22]}:{trame[22:24]}"
		self.type_eth = trame[24:28]
		self.data = trame[28:]
		if(self.type_eth == "0800"):
			self.type_eth2 = "IPV4"
		elif(self.type_eth == "86DD"):
			self.type_eth2 = "IPV6"
		elif(self.type_eth == "0806"):
			self.type_eth2 = "ARP"
		elif(self.type_eth == "8035"):
			self.type_eth2 = "RARP"
		else:
			self.type_eth2 = "indéterminé"
		
		

	def get_dst(self):
		return self.dst

	def get_src(self):
		return self.src

	def get_type_eth(self):
		return self.type_eth

	def get_type_eth2(self):
		return self.type_eth2

	def get_data(self):
		return self.data

	def __str__(self):
		return f"Ethernet:\
		\n\tAdresse destination: {self.dst}\
		\n\tAdresse source: {self.src}\
		\n\tType de protocole: {self.type_eth2} (0x{self.type_eth})"
class Ethernet:

	def __init__(self, frame):
		
		# Parser
		self.dst = f"{frame[:2]}:{frame[2:4]}:{frame[4:6]}:{frame[6:8]}:{frame[8:10]}:{frame[10:12]}"
		self.src = f"{frame[12:14]}:{frame[14:16]}:{frame[16:18]}:{frame[18:20]}:{frame[20:22]}:{frame[22:24]}"
		self.type_eth = frame[24:28]
		self.data = frame[28:]

		# Type
		if (self.type_eth == "0800"):
			self.type_eth2 = "IPv4"
		elif (self.type_eth == "86DD"):
			self.type_eth2 = "IPv6"
		elif (self.type_eth == "0806"):
			self.type_eth2 = "ARP"
		elif (self.type_eth == "8035"):
			self.type_eth2 = "RARP"
		else:
			self.type_eth2 = "Unknown"
		
		
	# Getters
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


	# String
	def __str__(self):
		return f"Ethernet:\
		\n\tDestination Address: {self.dst}\
		\n\tSource Address: {self.src}\
		\n\tType: {self.type_eth2} (0x{self.type_eth})"
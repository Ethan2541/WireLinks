class Http:
	def __init__(self, trame):
		self.fin_http = 0
		self.http = ""

		for i in range(0, len(trame), 2):
			if(trame[i:i+8] == "0D0A0D0A"):
				self.fin_http = i+2
				break
			else:
				self.http += chr(int(trame[i:i+2], 16))

		self.data = "".join(chr(int(trame[i:i+2], 16)) for i in range(self.fin_http+4, len(trame), 2))
		
		if(self.data.replace(" ", "").replace("\n", "") == ""):
			self.data = None


	# Getters
	def get_http(self):
		return self.http

	def get_data(self):
		return self.data


	# String
	def __str__(self):
		return f"HTTP:\n\n{self.http}"
class Http:
	
	def __init__(self, frame):
		# Parser
		self.code = None
		self.msg = None
		self.version = None
		self.url = None
		self.version = None
		self.method = None
		self.fin_http = 0
		self.http = ""


		for i in range(0, len(frame), 2):

			if(frame[i:i+8] == "0D0A0D0A"):
				self.fin_http = i+2
				break
			else:
				self.http += chr(int(frame[i:i+2], 16))


		self.data_ascii = frame[self.fin_http+4:]
		self.data = "".join(chr(int(frame[i:i+2], 16)) for i in range(self.fin_http+4, len(frame), 2))
		

		if(self.data.replace(" ", "").replace("\n", "") == ""):
			self.data = None
		

		# Fields initialization
		self.header()



	def header(self):
		fin_version = 0
		fin_code = 0

		# Reply
		if (self.http[:4] == "HTTP"):	

			# Version
			for i in range(len(self.http)):
				if (self.http[i] == " "):
					self.version = self.http[:i]
					fin_version = i
					break

			# Code
			for i in range(fin_version+1, len(self.http)):
				if (self.http[i] == " "):
					self.code = self.http[fin_version+1:i]
					fin_code = i
					break

			# Message
			for i in range(fin_code+1, len(self.http)):
				if (self.http[i] == "\r"):
					self.msg = self.http[fin_code+1:i]
					break

		# Request
		else:

			# Method
			for i in range(len(self.http)):
				if (self.http[i] == " "):
					self.method = self.http[:i]
					fin_version = i
					break

			# Code
			for i in range(fin_version+1, len(self.http)):
				if (self.http[i] == " "):
					self.url = self.http[fin_version+1:i]
					fin_code = i
					break

			# Version
			for i in range(fin_code+1, len(self.http)):
				if (self.http[i] == "\r"):
					self.version = self.http[fin_code+1:i]
					break



	# Getters
	def get_http(self):
		return self.http

	def get_data(self):
		return self.data
	
	def get_data_ascii(self):
		return self.data_ascii

	def get_version(self):
		return self.version
	
	def get_method(self):
		return self.method

	def get_url(self):
		return self.url

	def get_code(self):
		return self.code

	def get_msg(self):
		return self.msg



	# String
	def __str__(self):
		return f"HTTP:\n\n{self.http}"
class Igmp:

	def __init__(self, typ, frame):
		# Parsing the default header fields
		self.typ = typ
		self.version = frame[0]
		self.type_igmp = frame[1]
		self.unused = frame[2:4]
		self.chk = frame[4:8]
		self.class_ip = f"{int(frame[8:10], 16)}.{int(frame[10:12], 16)}.{int(frame[12:14], 16)}.{int(frame[14:16], 16)}"
		self.data = frame[16:]



	# Getters
	def get_typ(self):
		return self.typ

	def get_version(self):
		return self.version

	def get_type_igmp(self):
		return self.type_igmp

	def get_unused(self):
		return self.unused

	def get_chk(self):
		return self.chk

	def get_class_ip(self):
		return self.class_ip

	def get_data(self):
		return self.data



	# String
	def __str__(self):
		return f"{self.typ}:\
		\n\tIGMP Version: {self.version}\
		\n\tIGMP Type: {self.type_igmp}\
		\n\tChecksum: 0x{self.chk}\
		\n\tGroup Address: {self.class_ip}"

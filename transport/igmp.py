class Igmp:
	def __init__(self, typ, trame):
		self.typ = typ
		self.version = trame[0]
		self.type_igmp = trame[1]
		self.unused = trame[2:4]
		self.chk = trame[4:8]
		self.class_ip = f"{int(trame[8:10], 16)}.{int(trame[10:12], 16)}.{int(trame[12:14], 16)}.{int(trame[14:16], 16)}"
		self.data = trame[16:]

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

	def __str__(self):
		return f"{self.typ}:\
		\n\tIGMP Version: {self.version}\
		\n\tIGMP Type: {self.type_igmp}\
		\n\tChecksum: 0x{self.chk}\
		\n\tClass D Ip address: {self.chk}"

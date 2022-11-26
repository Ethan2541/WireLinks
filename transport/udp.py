class Udp:
	def __init__(self, typ, trame):
		self.typ = typ
		self.port_src = trame[:4]
		self.port_dst = trame[4:8]
		self.length = trame[8:12]
		self.chk = trame[12:16]
		self.data = trame[16:]
		if(self.data == ""):
			self.data = None
		if(self.port_src=="0050" or self.port_dst=="0050"):
			self.appli = "HTTP"
		elif(self.port_src=="0019" or self.port_dst=="00019"):
			self.appli = "SMTP"
		elif(self.port_src=="008F" or self.port_dst=="0008F"):
			self.appli = "IMAP"
		elif(self.port_src=="006E" or self.port_dst=="006E"):
			self.appli = "POP"
		elif(self.port_src=="0035" or self.port_dst=="0035"):
			self.appli = "DNS"
		elif(self.port_src=="01BB" or self.port_dst=="01BB"):
			self.appli = "HTTPS"
		elif(self.port_src=="0043" or self.port_dst=="0043"):
			self.appli = "DHCP"
		elif(self.port_src=="0016" or self.port_dst=="0016"):
			self.appli = "SSH"
		elif(self.port_src=="0D3D" or self.port_dst=="0D3D"):
			self.appli = "RDP"
		elif(self.port_src=="0014" or self.port_dst=="0014" or self.port_src=="0015" or self.port_dst=="0015"):
			self.appli = "FTP"
		else:
			self.appli = "Non reconnu"

	def get_typ(self):
		return self.typ

	def get_port_dst(self):
		return self.port_dst

	def get_port_src(self):
		return self.port_src

	def get_length(self):
		return self.length

	def get_chk(self):
		return self.chk

	def get_data(self):
		return self.data

	def get_appli(self):
		return self.appli

	def __str__(self):
		return f"{self.typ}:\n\tPort source: {int(self.port_src, 16)}\
		\n\tPort destination: {int(self.port_dst, 16)}\
		\n\tChecksum: 0x{self.chk}\
		\n\tApplication utilisé: {self.appli}"
class Tcp:
	def __init__(self, typ, trame):
		self.typ = typ
		self.port_src = trame[:4]
		self.port_dst = trame[4:8]
		self.seq_num = trame[8:16]
		self.ack_num = trame[16:24]
		self.thl = trame[24]
		self.reserved = str(hex(int(trame[25:28], 16) >> 6))
		self.urg = str((int(trame[25:28], 16) & 32) >> 5)
		self.ack = str((int(trame[25:28], 16) & 16) >> 4)
		self.psh = str((int(trame[25:28], 16) & 8) >> 3)
		self.rst = str((int(trame[25:28], 16) & 4) >> 2)
		self.syn = str((int(trame[25:28], 16) & 2) >> 1)
		self.fin = str(int(trame[25:28], 16) & 1)
		self.window = trame[28:32]
		self.chk = trame[32:36]
		self.up = trame[36:40]
		opt_length = int(self.thl, 16)*8 - 40
		self.opt = trame[40:40+opt_length]
		if (trame[40+opt_length:] != ""):
			self.data = trame[40+opt_length:]
		else:
			self.data = None

		if (self.port_src=="0050" or self.port_dst=="0050"):
			self.appli = "HTTP"
		elif (self.port_src=="0019" or self.port_dst=="00019"):
			self.appli = "SMTP"
		elif (self.port_src=="008F" or self.port_dst=="0008F"):
			self.appli = "IMAP"
		elif (self.port_src=="006E" or self.port_dst=="006E"):
			self.appli = "POP"
		elif (self.port_src=="0035" or self.port_dst=="0035"):
			self.appli = "DNS"
		elif (self.port_src=="01BB" or self.port_dst=="01BB"):
			self.appli = "HTTPS"
		elif (self.port_src=="0043" or self.port_dst=="0043"):
			self.appli = "DHCP"
		elif (self.port_src=="0016" or self.port_dst=="0016"):
			self.appli = "SSH"
		elif (self.port_src=="0D3D" or self.port_dst=="0D3D"):
			self.appli = "RDP"
		elif (self.port_src=="0014" or self.port_dst=="0014" or self.port_src=="0015" or self.port_dst=="0015"):
			self.appli = "FTP"
		else:
			self.appli = "Unknown"


	# Getters
	def get_typ(self):
		return self.typ

	def get_port_dst(self):
		return self.port_dst

	def get_port_src(self):
		return self.port_src

	def get_seq_num(self):
		return self.seq_num

	def get_ack_num(self):
		return self.ack_num

	def get_thl(self):
		return self.thl

	def get_reserved(self):
		return self.reserved

	def get_urg(self):
		return self.urg

	def get_ack(self):
		return self.ack

	def get_psh(self):
		return self.psh

	def get_rst(self):
		return self.rst

	def get_syn(self):
		return self.syn

	def get_fin(self):
		return self.fin

	def get_window(self):
		return self.window

	def get_chk(self):
		return self.chk

	def get_up(self):
		return self.up

	def get_opt(self):
		return self.opt

	def get_data(self):
		return self.data

	def get_appli(self):
		return self.appli


	# String
	def __str__(self):
		return f"{self.typ}:\n\tSource Port: {int(self.port_src, 16)}\
		\n\tDestination Port: {int(self.port_dst, 16)}\
		\n\tSequence Number: {int(self.seq_num, 16)}\
		\n\tACK Number: {int(self.ack_num, 16)}\
		\n\tTHL: {int(self.thl, 16)*4}\
		\n\tReserved: {self.reserved}\
		\n\tURG: {self.urg}\
		\n\tACK: {self.ack}\
		\n\tPSH: {self.psh}\
		\n\tRST: {self.rst}\
		\n\tSYN: {self.syn}\
		\n\tFIN: {self.fin}\
		\n\tWindow: {int(self.window, 16)}\
		\n\tChecksum: 0x{self.chk}\
		\n\tUrgent pointer: {int(self.up, 16)}\
		\n\tApplication: {self.appli}"
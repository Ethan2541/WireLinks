class Ip:

	def __init__(self, frame, typ):
		# Parsing the default header fields
		self.typ = typ

		self.version = frame[0]
		self.ihl = frame[1]
		self.tos = frame[2:4]
		self.ttlength = frame[4:8]

		self.iden = frame[8:12]
		self.flags = int(frame[12], 16) >> 1
		self.res = str((self.flags & 0b100) >> 1)
		self.df = str((self.flags & 0b010) >> 1)
		self.mf = str((self.flags & 0b001) >> 1)
		self.fragoff = str(int(frame[13:16], 16) << 1)

		self.ttl = frame[16:18]
		self.proto = frame[18:20]


		# Determining the correct protocol
		if (self.proto == "06"):
			self.proto2 = "TCP"
		elif (self.proto == "01"):
			self.proto2 = "ICMP"
		elif (self.proto == "02"):
			self.proto2 = "IGMP"
		elif (self.proto == "08"):
			self.proto2 = "EGP"
		elif (self.proto == "09"):
			self.proto2 = "IGP"
		elif (self.proto == "11"):
			self.proto2 = "UDP"
		elif (self.proto == "24"):
			self.proto2 = "XTP"
		elif (self.proto == "2D"):
			self.proto2 = "RSVP"
		else:
			self.proto2 = "Unknown"


		self.chk = frame[20:24]

		self.src = f"{int(frame[24:26], 16)}.{int(frame[26:28], 16)}.{int(frame[28:30], 16)}.{int(frame[30:32], 16)}"
		
		self.dst = f"{int(frame[32:34], 16)}.{int(frame[34:36], 16)}.{int(frame[36:38], 16)}.{int(frame[38:40], 16)}"
		

		# Options
		self.opt_length = int(self.ihl, 16)*8 - 40
		self.opt = frame[40:40+self.opt_length]
		self.options()

		if(frame[40+self.opt_length:] != ""):
			self.data = frame[40+self.opt_length:]
		else:
			self.data = None



	def options(self):
		self.opt_det = []
		len_opt = 0
		next_opt = 0
		nb_opt = 0

		while (next_opt != self.opt_length):

			if (self.opt[next_opt:next_opt+2] == "00"):
				self.opt_det.append({"Name": "End Of List (0x00)"})
				next_opt = self.opt_length
				nb_opt = nb_opt + 1


			elif (self.opt[next_opt:next_opt+2] == "01"):

				self.opt_det.append({"Name": "No-Operation (0x01)", "Len":1})
				next_opt = next_opt+2
				nb_opt = nb_opt + 1


			elif(self.opt[next_opt:next_opt+2] == "07"):

				len_opt = int(self.opt[next_opt+2:next_opt+4], 16)
				self.opt_det.append({"Name": "Record Route (0x07)", "Len":len_opt})
				self.opt_det[nb_opt]["Pointer"] = self.opt[next_opt+4:next_opt+6]
				self.opt_det[nb_opt]["IP"] = []

				for i in range(next_opt+6, next_opt+len_opt, 8):
					ip_buffer = self.opt[i: i+8]
					self.opt_det[nb_opt]["IP"].append(f"{int(ip_buffer[0:2], 16)}.{int(ip_buffer[2:4], 16)}.{int(ip_buffer[4:6], 16)}.{int(ip_buffer[6:8], 16)}")

				next_opt = next_opt + len_opt * 2
				nb_opt = nb_opt + 1


			elif (self.opt[next_opt:next_opt+2] == "44"):

				len_opt = int(self.opt[next_opt+2:next_opt+4], 16)
				self.opt_det.append({"Name": "Timestamp (0x44)", "Len":len_opt})
				self.opt_det[nb_opt]["Pointer"] = self.opt[next_opt+4:next_opt+6]
				self.opt_det[nb_opt]["OF"] = str(int(self.opt[next_opt+6:next_opt+8], 16) & 0xF0)
				self.opt_det[nb_opt]["FL"] = str(int(self.opt[next_opt+6:next_opt+8], 16) & 0x0F)
				self.opt_det[nb_opt]["Time"] = []
				
				for i in range(next_opt + 6, next_opt + len_opt, 8):
					self.opt_det[nb_opt]["Time"].append(self.opt[i: i+8])

				next_opt = next_opt+len_opt*2
				nb_opt = nb_opt + 1


			elif (self.opt[next_opt:next_opt+2] == "83"):

				len_opt = int(self.opt[next_opt+2:next_opt+4], 16)
				self.opt_det.append({"Name": "Loose Source Route (0x83)", "Len":len_opt})
				self.opt_det[nb_opt]["Pointer"] = self.opt[next_opt+4:next_opt+6]
				self.opt_det[nb_opt]["IP"] = []

				for i in range(next_opt+6, next_opt+len_opt, 8):
					ip_buffer = self.opt[i: i+8]
					self.opt_det[nb_opt]["IP"].append(f"{int(ip_buffer[0:2], 16)}.{int(ip_buffer[2:4], 16)}.{int(ip_buffer[4:6], 16)}.{int(ip_buffer[6:8], 16)}")

				next_opt = next_opt + len_opt * 2
				nb_opt = nb_opt + 1


			elif (self.opt[next_opt:next_opt+2] == "89"):

				len_opt = int(self.opt[next_opt+2:next_opt+4], 16)
				self.opt_det.append({"Name": "Strict Source Route (0x89)", "Len":len_opt})
				self.opt_det[nb_opt]["Len"] = len_opt
				self.opt_det[nb_opt]["Pointer"] = self.opt[next_opt+4:next_opt+6]
				self.opt_det[nb_opt]["IP"] = []
				
				for i in range(next_opt+6, next_opt+len_opt, 8):
					ip_buffer = self.opt[i: i+8]
					self.opt_det[nb_opt]["IP"].append(f"{int(ip_buffer[0:2], 16)}.{int(ip_buffer[2:4], 16)}.{int(ip_buffer[4:6], 16)}.{int(ip_buffer[6:8], 16)}")

				next_opt = next_opt + len_opt * 2
				nb_opt = nb_opt + 1


			else:
				len_opt = int(self.opt[next_opt+2:next_opt+4], 16)
				self.opt_det.append({"Other": self.opt[next_opt:next_opt+len_opt*2]})
				next_opt = next_opt + len_opt*2

		self.nb_opt = nb_opt



	# Getters
	def get_typ(self):
		return self.typ

	def get_dst(self):
		return self.dst

	def get_src(self):
		return self.src

	def get_version(self):
		return self.version

	def get_ihl(self):
		return self.ihl

	def get_tos(self):
		return self.tos

	def get_ttlength(self):
		return self.ttlength

	def get_iden(self):
		return self.iden

	def get_flags(self):
		return self.flags

	def get_fragoff(self):
		return self.fragoff

	def get_ttl(self):
		return self.ttl

	def get_proto(self):
		return self.proto

	def get_proto2(self):
		return self.proto2

	def get_chk(self):
		return self.chk

	def get_opt(self):
		return self.opt

	def get_data(self):
		return self.data

	def get_opt_det(self):
		return self.opt_det

	def get_nb_opt(self):
		return self.nb_opt



	# String
	def __str__(self):
		chaine = f"IPv{self.version}:\
		\n\tSource Address: {self.src}\
		\n\tDestination Address: {self.dst}\
		\n\tProtocol: {self.proto2} ({int(self.proto, 16)})\
		\n\tIHL: {int(self.ihl, 16)*4} bytes (0x{self.ihl})\
		\n\tToS: 0x{self.tos}\
		\n\tTotal Length: {int(self.ttlength, 16)}\
		\n\tIdentifier: 0x{self.iden}\
		\n\tFlags:   R: {self.res}   DF: {self.df}   MF: {self.mf}\
		\n\tFragment Offset: 0x{self.fragoff}\
		\n\tTTL: {int(self.ttl, 16)}\
		\n\tHeader Checksum: 0x{self.chk}\
		\n\tNumber of Options: {self.nb_opt}"
		
		if (self.nb_opt > 0):
			chaine += f"\n\tOptions:\n\t\t"

			for i in range(len(self.opt_det)):

				for key, value in self.opt_det[i].items():
					chaine += f"{key} = {value}   "
				chaine += "\n\t\t"

		return chaine

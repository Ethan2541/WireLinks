class Dns:
	def __init__(self, typ, trame):
		self.typ = typ
		self.port_src = trame[:4]
		self.port_dst = trame[4:8]
		self.length = trame[8:12]
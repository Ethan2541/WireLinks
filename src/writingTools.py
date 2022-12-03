import os
from fpdf import FPDF
from trame import *
from liste_trames import *

class PDF(FPDF):
	def header(self):
		self.set_font("Helvetica", "B", size = 20)
		self.set_line_width(1)
		self.image(os.path.join(os.path.dirname(__file__), "../icons/logo.png"), 10, 8, 15)
		self.cell(0, 10, "FLOW CHART", new_x = "LMARGIN", new_y = "NEXT", align = "C", border = "B")
		self.ln(8)

	def footer(self):
		self.set_y(-15)
		self.set_font("Helvetica", size = 10)
		self.cell(0, 10, f"{self.page_no()}/{{nb}}", align = "R")

	def print_cell(self, trame):
		content = trame.flow_graph()

		self.set_font("Helvetica", size = 10)
		self.set_fill_color(255, 255, 255)

		if (trame.ip != None and trame.ip.typ=="IPv4"):
			if (trame.transport != None and trame.transport.get_typ() == "TCP"):
				self.set_fill_color(228, 255, 199)
				
			elif (trame.transport != None and trame.transport.get_typ() == "UDP"):
				self.set_fill_color(218, 238, 255)

			elif (trame.transport != None and trame.transport.get_typ()=="ICMP"):
				self.set_fill_color(252, 224, 255)

			elif (trame.transport != None and trame.transport.get_typ()=="IGMP"):
				self.set_fill_color(254, 255, 208)


		elif (trame.ip != None and trame.ip.get_typ() == "ARP"):
			self.set_fill_color(250, 240, 215)


		self.cell(0, 10, txt = content, new_x = "LMARGIN", fill = 1)
		self.ln(8)
		

def create_pdf(filename, trame_liste):
	pdf = PDF(orientation = "L", unit = "mm", format = "A4")
	pdf.set_title("FLOW CHART")
	pdf.set_author("WireLinks 1.0.0")

	pdf.add_page()
	pdf.set_auto_page_break(auto = True, margin = 15)

	for trame in trame_liste:
		pdf.print_cell(trame)
		
	if not filename.endswith(".pdf"):
		filename += ".pdf"	

	pdf.output(filename)

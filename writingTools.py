from fpdf import FPDF
from liste_trames import *
from trame import *

class PDF(FPDF):
	def header(self):
		self.set_font("Helvetica", "B", size = 20)
		self.set_line_width(1)
		self.cell(0, 10, "FRAMES ANALYSIS", new_x = "LMARGIN", new_y = "NEXT", align = "C", border = "B")
		self.ln(20)

	def footer(self):
		self.set_y(-15)
		self.set_font("Helvetica", size = 10)
		self.cell(0, 10, f"{self.page_no()}/{{nb}}", align = "R")

	def print_frame_title(self, trame):
		self.set_font("Helvetica", "B", size = 14)
		self.cell(0, 10, txt = "TRAME #{0:04d}".format(trame.get_iden()), new_x = "LMARGIN", new_y = "NEXT")
		self.ln = 10

	"""def print_ethernet(self, trame):
		self.set_draw_color(46, 59, 67)
		self.set_font("Helvetica", "B", size = 12)
		self.set_line_width(1)
		self.multi_cell(0, 10, txt = str(trame.get_ethernet()), border = "L", new_x="LMARGIN")
		self.ln = 5

	def print_ip(self, trame):
		self.set_draw_color(46, 59, 67)
		self.set_font("Helvetica", "B", size = 12)
		self.set_line_width(1)
		self.multi_cell(0, 10, txt = str(trame.get_ip()), border = "L", new_x="LMARGIN")
		self.ln = 5

	def print_transport(self, trame):
		self.set_draw_color(46, 59, 67)
		self.set_font("Helvetica", "B", size = 12)
		self.set_line_width(1)
		self.multi_cell(0, 10, txt = str(trame.get_transport()), border = "L")
		self.ln = 5

	def print_http(self, trame):
		self.set_draw_color(46, 59, 67)
		self.set_font("Helvetica", "B", size = 12)
		self.set_line_width(1)
		self.multi_cell(0, 10, txt = str(trame.get_http()), border = "L")
		self.ln = 5

	def print_data(self, trame):
		self.set_draw_color(46, 59, 67)
		self.set_font("Helvetica", "B", size = 12)
		self.set_line_width(1)
		self.multi_cell(0, 10, txt = str(trame.get_data()), border = "L")
		self.ln = 5"""

	def print_frame(self, trame):
		self.set_draw_color(46, 59, 67)
		self.set_font("Helvetica", "B", size = 12)
		self.set_line_width(1)
		self.multi_cell(0, 10, txt = str(trame), border = "L", new_x="LMARGIN")
		self.ln = 5
		
		"""if(trame.get_ethernet() != None):
			self.print_ethernet(trame)
			if(trame.get_ip() != None):
				self.print_ip(trame)
				if(trame.get_transport() != None):
					self.print_transport(trame)
				if(trame.get_http() != None):
					self.print_http(trame)
					if(trame.get_data() != None):
						self.print_data(trame)"""


def create_pdf(filename, trame_liste):
	pdf = PDF(orientation = "P", unit = "mm", format = "A4")
	pdf.set_title("FRAMES ANALYSIS")
	pdf.set_author("WireLinks 1.0.0")

	pdf.add_page()
	pdf.set_auto_page_break(auto = True, margin = 15)

	for trame in trame_liste:
		pdf.print_frame_title(trame)
		pdf.print_frame(trame)

	if filename.endswith(".pdf"):
		pdf.output(filename)
	else:
		filename += ".pdf"
		pdf.output(filename)

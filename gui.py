from readingTools import *
from writingTools import *
from trame import *
from liste_trames import *
import os
import tkinter as tk
from tkinter import messagebox as mb
from tkinter import filedialog as fd
import tkinter.font as tkFont
import tkmacosx

try:
	from ctypes import windll
	windll.shcore.SetProcessDpiAwareness(1)
finally:

	root = tk.Tk()

	# Window's Parameters Configuration
	app_name = "WireLinks 1.0.0"
	dirname = os.path.dirname(__file__)

	window_width = 1280
	window_height = 720
	screen_width = root.winfo_screenwidth()
	screen_height = root.winfo_screenheight()

	center_x = int(screen_width / 2 - window_width / 2)
	center_y = int(screen_height / 2 - window_height / 2)

	root.title(app_name)

	root.minsize(720, 480)
	root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")


	# Fonts and Colors
	title_font = tkFont.Font(family = "Roboto Medium", size = 18)
	subtitle_font = tkFont.Font(family = "Roboto Medium", size = 13)
	text_font = tkFont.Font(family = "Roboto", size = 12)
	button_font = tkFont.Font(family = "Roboto Medium", size = 12)
	entry_font = tkFont.Font(family = "Roboto", size = 12, slant = "italic")

	menu_color = "#2e3b43"
	bg_color = "#26313c"
	frame_color = "#1d2730"
	entry_color = "#ffffff"
	hover_menu_color = "#5b524b"
	hover_listbox_color = "#5b524b"
	text_color = "#ffffff"


	root.configure(bg = bg_color)
	root.columnconfigure(1, weight = 2)
	root.rowconfigure(0, weight = 1)


	# Menu and Content Frames
	menu = tk.Frame(root, bg = menu_color)
	menu.grid(column = 0, row = 0, sticky = tk.NS)

	right_frame = tk.Frame(root)
	right_frame.grid(column = 1, row = 0, sticky = "new")
	right_frame.columnconfigure(0, weight = 1)
	right_frame.rowconfigure(0, weight = 1)
	right_frame.rowconfigure(1, weight = 10000)



	# Menu Buttons

	# Open File Dialog
	filetypes = [("Text Files (*.txt)", "*.txt")]
	def file_dialog_command():
		tracefile_name = fd.askopenfilename(title = "Choose your File", filetypes = filetypes, initialdir = dirname)
		print(tracefile_name)

	folder_icon = tk.PhotoImage(file = os.path.join(dirname, "icons/folder-open.png"))

	file_dialog = tkmacosx.Button(menu, bg = menu_color, fg = text_color, bd = 5, height = 80, width = 80, relief = tk.FLAT, 
									borderless = True, activebackground = menu_color, activeforeground = text_color, overbackground = hover_menu_color,
									focusthickness = 0, image = folder_icon, command = lambda: file_dialog_command())
	file_dialog.pack()


	# Export to PDF
	save_icon = tk.PhotoImage(file = os.path.join(dirname, "icons/save.png"))

	save_btn = tkmacosx.Button(menu, bg = menu_color, fg = text_color, bd = 5, height = 80, width = 80, relief = tk.FLAT, 
									borderless = True, activebackground = menu_color, activeforeground = text_color, overbackground = hover_menu_color,
									focusthickness = 0, image = save_icon)
	save_btn.pack()


	# Exit
	def exit_command():
		answer = mb.askyesno("Confirmation", "Are you sure that you want to quit {0} ?".format(app_name))
		if answer:
			root.destroy()

	exit_icon = tk.PhotoImage(file = os.path.join(dirname, "icons/exit.png"))

	exit_btn = tkmacosx.Button(menu, bg = menu_color, fg = text_color, bd = 5, height = 80, width = 80, relief = tk.FLAT, 
									borderless = True, activebackground = menu_color, activeforeground = text_color, overbackground = hover_menu_color,
									focusthickness = 0, image = exit_icon, command = lambda: exit_command())
	exit_btn.pack()
	


	# Entry for Filters
	def on_focus_in(entry):
		if entry.cget("state") == "disabled":
			entry.config(state = "normal", font = text_font)
			entry.delete(0, "end")

	def on_focus_out(entry, placeholder):
		if entry.get() == "":
			entry.insert(0, placeholder)
			entry.config(state = "disabled", font = entry_font)

	filterbar = tk.Entry(right_frame, bg = menu_color, disabledbackground = menu_color, fg = entry_color, 
								relief = tk.FLAT, disabledforeground = entry_color, bd = 0, font = entry_font)
	filterbar.insert(0, " Type your Filter")
	filterbar.configure(state = "disabled")
	filterbar.grid(row = 0, sticky = tk.EW)

	# Placeholder
	filterbar_focus_in = filterbar.bind("<Button-1>", lambda x: on_focus_in(filterbar))
	filterbar_focus_out = filterbar.bind("<FocusOut>", lambda x: on_focus_out(filterbar, " Type your Filter"))



	# Content
	content = tk.Frame(right_frame, bg = bg_color)
	content.grid(row = 1, sticky = tk.EW)

	content_title = tk.Label(content, bg = bg_color, font = title_font, fg = text_color, text = "FRAMES ANALYSIS")
	content_title.pack(pady = (50, 25))


	# List of Frames

	# Wrapper and Listbox
	frames_subtitle = tk.Label(content, bg = bg_color, font = subtitle_font, fg = text_color, text = "List of Frames")
	frames_subtitle.pack(padx = 125, anchor = "w")

	printable_frames_list = ["  #{0:04d}     {1:<17}     {2:<17}     {3:<15}     {4:<15}     {5:<8}     {6:<8}    {7:<9}".format(0, "MAC Src Address", "MAC Dst Address", "IP Src Address", "IP Dst Address", "Port Src", "Port Dst", "Protocole")]
	tk_printable_frames_list = tk.Variable(value = printable_frames_list)

	frames_wrapper = tk.Frame(content, relief = tk.GROOVE, highlightthickness = 4, highlightbackground = frame_color, 
										highlightcolor = menu_color)
	frames_wrapper.pack(padx = 50, pady = (10,25), fill = tk.BOTH)

	content_frames = tk.Listbox(frames_wrapper, bg = frame_color, fg = text_color, height = 10, listvariable = tk_printable_frames_list, 
										selectmode = tk.SINGLE, font = text_font, activestyle = "none", relief = tk.FLAT, highlightthickness = 0,
										selectbackground = hover_listbox_color)

	def ajouter_trame(trame):
		content_frames.insert(tk.END, trame)



	# Scrollbars
	frames_scrollbar = tk.Scrollbar(frames_wrapper, orient = "vertical", width = 15)
	frames_scrollbar.pack(side = "right", fill = "y")

	frames_scrollbar_hor = tk.Scrollbar(frames_wrapper, orient = "horizontal", width = 15)
	frames_scrollbar_hor.pack(side = "bottom", fill = "x")

	content_frames.config(yscrollcommand = frames_scrollbar.set)
	frames_scrollbar.config(command = content_frames.yview)

	content_frames.config(xscrollcommand = frames_scrollbar_hor.set)
	frames_scrollbar_hor.config(command = content_frames.xview)

	content_frames.pack(fill = tk.BOTH)



	# Details

	# Wrapper and Text Widget
	text_subtitle = tk.Label(content, bg = bg_color, font = subtitle_font, fg = text_color, text = "Details")
	text_subtitle.pack(padx = 125, anchor = "w")

	text_wrapper = tk.Frame(content, relief = tk.GROOVE, highlightthickness = 4, highlightbackground = frame_color, highlightcolor = menu_color)
	text_wrapper.pack(padx = 50, pady = (10,50), fill = tk.BOTH)

	content_text = tk.Text(text_wrapper, bg = frame_color, fg = text_color, height = screen_height, font = text_font,
		relief = tk.FLAT, highlightthickness = 0)


	# Scrollbars
	text_scrollbar = tk.Scrollbar(text_wrapper, orient = "vertical", width = 15)
	text_scrollbar.pack(side = "right", fill = "y")

	text_scrollbar_hor = tk.Scrollbar(text_wrapper, orient = "horizontal", width = 15)
	text_scrollbar_hor.pack(side = "bottom", fill = "x")

	content_text.config(yscrollcommand = text_scrollbar.set)
	text_scrollbar.config(command = content_text.yview)

	content_text.config(xscrollcommand = text_scrollbar_hor.set)
	text_scrollbar_hor.config(command = content_text.xview)

	content_text.pack(fill = tk.BOTH, side = "left", expand = tk.YES)


	# Labels

	content_text.tag_config("hidden", elide = True)

	# Ethernet II
	eth_button = tkmacosx.Button(content_text, bg = menu_color, fg = text_color, bd = 5, height = 25, relief = tk.FLAT, width = 225,
									borderless = True, activebackground = menu_color, activeforeground = text_color, overbackground = hover_menu_color,
									focusthickness = 0, font = button_font, text = "ETHERNET II")
	content_text.window_create(tk.END, window = eth_button)
	content_text.insert(tk.END, "   ")

	# IPv4
	ip_button = tkmacosx.Button(content_text, bg = menu_color, fg = text_color, bd = 5, height = 25, relief = tk.FLAT, width = 175,
									borderless = True, activebackground = menu_color, activeforeground = text_color, overbackground = hover_menu_color,
									focusthickness = 0, font = button_font, text = "IPv4")
	content_text.window_create(tk.END, window = ip_button)
	content_text.insert(tk.END, "   ")

	# TCP
	tcp_button = tkmacosx.Button(content_text, bg = menu_color, fg = text_color, bd = 5, height = 25, relief = tk.FLAT, width = 175,
									borderless = True, activebackground = menu_color, activeforeground = text_color, overbackground = hover_menu_color,
									focusthickness = 0, font = button_font, text = "TCP")
	content_text.window_create(tk.END, window = tcp_button)
	content_text.insert(tk.END, "   ")

	# HTTP
	http_button = tkmacosx.Button(content_text, bg = menu_color, fg = text_color, bd = 5, height = 25, relief = tk.FLAT, width = 175,
									borderless = True, activebackground = menu_color, activeforeground = text_color, overbackground = hover_menu_color,
									focusthickness = 0, font = button_font, text = "HTTP")
	content_text.window_create(tk.END, window = http_button)
	content_text.insert(tk.END, "   ")

	# DATA
	data_button = tkmacosx.Button(content_text, bg = menu_color, fg = text_color, bd = 5, height = 25, relief = tk.FLAT, width = 175,
									borderless = True, activebackground = menu_color, activeforeground = text_color, overbackground = hover_menu_color,
									focusthickness = 0, font = button_font, text = "DATA")
	content_text.window_create(tk.END, window = data_button)
	content_text.insert(tk.END, "\n\n")
	
	content_text.insert(.get_ethernet())

	#content_text.tag_add("hidden", "2.0", "4.0")
	content_text.config(state = "disabled")

	def test():
		content_text.tag_config("hidden", elide = False)

	content_text.tag_add("hidden_ethernet", "3.0", "7.0")

	def toggle_ethernet():
		content_text.config(state="enabled")
		content_text.tag_config("hidden_ethernet", elide = False)
		content_text.config(state = "disabled")

	def selected_item():

		#ma ligne commence à partir de la ligne 3

	# Traverse the tuple returned by
	# curselection method and print
	# corresponding value(s) in the listbox
		for i in listbox.curselection():
			print(listbox.get(i)) #correspond au numéro de la trame

	def toggle_elision():
		# cget returns string "1" or "0"
		if int(text.tag_cget('mytag', 'elide')):
			text.tag_config('mytag', elide=False)

		else:
			text.tag_config('mytag', elide=True)

	def main():
		print("Bienvenue dans WireLinks")
		print("Quel est le nom du fichier que vous souhaitez analyser ? ", end="")
		file_name = input()
		trames = get_frames(file_name)
		for i in range(len(trames)):
			TrameList(Trame(i+1, trames[i]))
		
		if(len(TrameList.get_liste()) == 0):
			print("Trace vide")
		else:
			for i in TrameList.get_liste():
				ajouter_trame(i.afficher_info_imp_gui())

	main()

	root.mainloop()
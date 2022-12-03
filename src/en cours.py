# Display Analysis
def display_analysis():
	chart_frame.place_forget()

analysis_icon = tk.PhotoImage(file = os.path.join(dirname, "../icons/list.png"))
analysis = tkmacosx.Button(menu, bg = menu_color, fg = text_color, bd = 5, height = 80, width = 80, relief = tk.FLAT, 
								borderless = True, activebackground = menu_color, activeforeground = text_color, overbackground = hover_menu_color,
								focusthickness = 0, image = analysis_icon, command = lambda: display_analysis())
analysis.pack()

# Display Chart
def display_chart():
	for i in TrameList.get_liste():
		chart_content.insert(tk.END, i.flow_graph())
	chart_frame.place(x = 0, y = 0, width = screen_width, height = screen_height)
	chart_content.pack(fill = tk.BOTH)

chart_icon = tk.PhotoImage(file = os.path.join(dirname, "../icons/chart.png"))
chart = tkmacosx.Button(menu, bg = menu_color, fg = text_color, bd = 5, height = 80, width = 80, relief = tk.FLAT, 
								borderless = True, activebackground = menu_color, activeforeground = text_color, overbackground = hover_menu_color,
								focusthickness = 0, image = chart_icon, command = lambda: display_chart())
chart.pack()






chart_frame = tk.Frame(right_frame, bg = bg_color)
chart_content = tk.Listbox(chart_frame, bg = frame_color, fg = text_color, height = 100, selectmode = tk.SINGLE, font = text_font, 
							activestyle = "none", relief = tk.FLAT, highlightthickness = 0, selectbackground = hover_listbox_color)

# Scrollbars
chart_scrollbar = tk.Scrollbar(chart_frame, orient = "vertical", width = 15)
chart_scrollbar.place(x = 0, y = 0)
chart_scrollbar_hor = tk.Scrollbar(chart_frame, orient = "horizontal", width = 15)
chart_scrollbar_hor.place(x = 0, y = 0, width = screen_width)

chart_content.config(yscrollcommand = chart_scrollbar.set)
chart_scrollbar.config(command = chart_content.yview)
chart_content.config(xscrollcommand = chart_scrollbar_hor.set)
chart_scrollbar_hor.config(command = chart_content.xview)

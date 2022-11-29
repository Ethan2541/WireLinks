def get_words_from_str(string):
	words_list = []
	str_buffer = ""

	for character in string:
		if character.isspace() and len(str_buffer) != 0:
			words_list.append(str_buffer)

		else:
			str_buffer += character

	return words_list



def define_filter(string):
	words_list = get_words_from_str(string)
	stack = []

	for word in words_list:
		stack.append(word)
		if len(stack) == 3:
			if stack[0] == "ip.src":
				if stack[1] == "==":
					print("ip.src == " + stack[2])
				elif stack[1] == "!=":
					print("ip.src == " + stack[2])

			elif stack[0] == "ip.dst":
				if stack[1] == "==":
					print("ip.dst == " + stack[2])
				elif stack[1] == "!=":
					print("ip.dst == " + stack[2])

			stack = []



define_filter("ip.src == 192.168.1.1")
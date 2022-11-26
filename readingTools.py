def is_not_valid_extension(filename: str) -> bool:
    """str -> bool
    returns True if the file extension is supported
    """

    return not filename.endswith(".txt")





def read_trace_lines(filename: str) -> list[str]:
    """str -> list[str]
    returns every line of the file "filename"
    """

    if is_not_valid_extension(filename):
        print("Invalid file extension")
        return []

    try:
        with open(filename, 'r') as trace:
            return trace.readlines()

    except (FileNotFoundError, PermissionError, OSError):
        print("Error opening file")
        return []





def is_not_hex(str_to_check: str) -> bool:
    """str -> bool
    returns if the input character is hexadecimal
    """

    for character in str_to_check:
        if character.upper() not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']:
            return True

    return False





def get_invalid_format_frames(lines: list[str]) -> set[int]:
    """list[str] -> set[int]
    returns the set of the indexes of the invalid frames
    """

    invalid_frames_indexes = []
    frame_index = 0
    hex_count = 0

    current_offset = 0
    previous_offset = 0

    current_byte_count = 0
    previous_byte_count = 0

    number_of_empty_lines = 0
    count_empty_lines = True

    for i in range(len(lines)):
        # Empty line
        if len(lines[i]) == 1 and lines[i][0] == '\n':
            if count_empty_lines:
                number_of_empty_lines += 1
            continue

        # The line should have at least an offset (4), three spaces (3), a byte (2) and the '\n' character (1)
        if len(lines[i]) < 9:
            invalid_frames_indexes.append(frame_index)
            continue
    
        space_count = 0
        count_empty_lines = False

        offset_str = ""
        for character in lines[i][:4]:
            if character.isspace():
                break
            offset_str += character

        current_offset = int(offset_str, 16)

        # If a new frame is beginning
        if current_offset == 0 and i != number_of_empty_lines:
            frame_index += 1
            previous_offset = 0
            previous_byte_count = 0


        for j in range(len(lines[i])):
            # Checking if the offset is represented by 4 hex digits
            if j < 4 and is_not_hex(lines[i][j]):
                invalid_frames_indexes.append(frame_index)

            # Checking if the offset is followed by three spaces
            if j >= 4 and j < 7 and not lines[i][j].isspace():
                invalid_frames_indexes.append(frame_index)


            if j >= 7:
                # A sequence of bytes should end when encountering at least 2 spaces in a row
                if lines[i][j].isspace():
                    space_count += 1

                    if space_count > 1:
                        break

                    # When encountering a space, the two previous characters should be two hex digits
                    if is_not_hex(lines[i][j-1]) or is_not_hex(lines[i][j-2]) or not lines[i][j-3].isspace():
                        invalid_frames_indexes.append(frame_index)

                    current_byte_count += 1

                else:
                    hex_count += 1
                    space_count = 0

                    if j == len(lines[i]) - 1:
                        if not lines[i][j-2].isspace():
                            invalid_frames_indexes.append(frame_index)


        # There should be an even number of hex characters as 1 byte = 2 hex
        if hex_count % 2 != 0:
            invalid_frames_indexes.append(frame_index)

        hex_count = 0


        # Checking if the offset sequence is valid
        # The current offset should be equal to the previous one + the number of data bytes of the previous line
        if current_offset != previous_offset + previous_byte_count:
            invalid_frames_indexes.append(frame_index)

        previous_offset = current_offset
        previous_byte_count = current_byte_count
        current_byte_count = 0

    return set(invalid_frames_indexes)





def delete_ascii_dump(lines: list[str]) -> list[str]:
    """list[str] -> list[str]
    returns the data without the possible ASCII dump
    """

    data_wo_dump = []
    space_count = 0
    str_buffer = ""

    for line in lines:
        # Adding the string buffer if it is not empty
        if len(str_buffer) != 0:
            data_wo_dump.append(str_buffer)
            str_buffer = ""

        # Invalid line
        if len(line) < 4:
            continue

        # Offset
        for character in line[:4]:
            str_buffer += character

        # Separating the offset from the byte sequence -> [offset1, bytesequence1, offset2, bytesequence2, ...]
        data_wo_dump.append(str_buffer)
        str_buffer = ""

        # Byte sequence and possible ASCII dump
        for character in line[7:]:
            # Getting to the ASCII dump
            if space_count > 1:
                space_count = 0
                break

            if character.isspace():
                space_count += 1

            else:
                str_buffer += character
                space_count = 0

    # Adding the very last string buffer
    if len(str_buffer) != 0:
        data_wo_dump.append(str_buffer)

    return data_wo_dump





def get_frames_list(frames_data: list[str]) -> list[str]:
    """list[str] -> list[str]
    returns a list of the byte sequence of each frame
    """

    frames_list = []
    str_buffer = ""

    for k in range(len(frames_data)):
        # The list's format should be as follows : [offset1, bytesequence1, offset2, bytesequence2, ...]
        if k % 2 != 0:
            str_buffer += frames_data[k]

        else:
            offset = int(frames_data[k], 16)

            if offset == 0 and len(str_buffer) != 0:
                frames_list.append(str_buffer.upper())
                str_buffer = ""

    # Adding the very last byte sequence
    if len(str_buffer) != 0:
        frames_list.append(str_buffer.upper())

    return frames_list





def delete_invalid_frames(invalid_frames_indexes: set[int], frames_list: list[str]) -> list[str]:
    """set[int] x list[str] -> list[str]
    returns the frames list without the invalid frames according to the invalid frames' list of indexes
    """

    valid_frames_list = []

    # Deleting the frames according to their index
    for k in range(len(frames_list)):
        if k not in invalid_frames_indexes:
            valid_frames_list.append(frames_list[k])

    return valid_frames_list





def get_frames(filename: str) -> list[str]:
    """str -> list[str]
    returns the frames' byte sequences of the file filename
    """

    data = read_trace_lines(filename)
    invalid_frames_indexes = get_invalid_format_frames(data)

    data = delete_ascii_dump(data)
    data = get_frames_list(data)
    data = delete_invalid_frames(invalid_frames_indexes, data)

    return data
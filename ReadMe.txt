Reading and Writing Tools :
	ReadingTools
	WritingTools

The module ReadingTools allows to read .txt files having frames formatted as follows :
	OFFSET   Hex Dump   (ASCII Dump)
Frames that do not respect this format are likely to be ignored.

The module WritingTools allows to output .pdf files that look similar to WireShark's Flow Graph.
It also leaves empty space rather than displaying frames with unsupported protocols.


Here is the list of the supported protocols :
	- Link-layer : Ethernet II (no preamble and no trailer)
	- Network-layer : IPv4, ARP, ICMP, IGMP
	- Transport-layer : TCP, UDP
	- Application-layer : HTTP

These protocols are implemented as classes, in eponym files. The latter all have a parser, getters
and str representation.


The file "trame.py" groups every protocol object to build a frame. It also implements several ways to
display a single frame.

The file "liste_trames.py" holds the frames list of the tracefile that is being analyzed. It also
implements filters handling.

Finally, the file "main.py" implements the GUI and runs the program.
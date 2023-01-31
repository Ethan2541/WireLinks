#WireLinks

Goal
---

WireLinks is a network traffic visualizer which is greatly inspired by WireShark. We created WireLinks as part of an end-of-term assignment for the `LU3IN033 - Computer Networking` course at _Sorbonne Université_.


How to run WireLinks ?
---

In order to run our program, you simply need to execute the file `main.py` with your Python interpreter.


Reading and Writing Tools
---

The module ReadingTools allows to read .txt files having frames formatted as follows:
	OFFSET   Hex Dump   (ASCII Dump)
Frames that do not respect this format are likely to be ignored.

The module WritingTools allows to output .pdf files, available in the "output" folder, that look similar to WireShark's Flow Graph. It also leaves empty space rather than displaying frames with unsupported protocols.

These modules are available in the "src" folder along the other modules.


Source Files
---

The file `trame.py` groups every protocol object to build a frame. It also implements several ways to display a single frame.

The file `liste_trames.py` holds the frames list of the tracefile that is being analyzed. It also implements filters handling.

Finally, the file `main.py` implements the GUI and runs the program.


Protocols
---

Here is the list of the supported protocols:
- Link-layer : `Ethernet II` (no preamble and no trailer)
- Network-layer : `IPv4`, `ARP`, `ICMP`, `IGMP`
- Transport-layer : `TCP`, `UDP`
- Application-layer : `HTTP`

These protocols are implemented as classes, in eponym files. The latter all have a parser, getters and str representation.


Samples
---

There is also some samples for you to test WireLinks. Please enjoy using our program!


Icons and Fonts
---

The "icons" folder has the required icons for the menu bar. You can also install the Roboto font available in the "fonts" folder for better experience.


Filter Options
---

There are different filter options that you can type in the filter bar on the top of the application to filter the frames.

Here they are:
- `ip.src` for the source ip address
- `ip.dst` for the ip destination address
- `mac.src` for the mac source address
- `mac.dst` for the mac destination address
- `port.src` for the port source address
- `port.dst` for the port destination address
- `proto` to look for a particular protocol

Then you have to give the type of operation you want: `==` or `<>` or `!=` (`<>` and `!=` are tha same)

Then you would give the value that you are searching for

| Value        | Format					|
| ------------ | -------------------------------------- |
| IP address   | 192.168.0.0				|
| MAC address  | FF:FF:FF:FF:FF:FF			|
| Port number  | decimal (ex: 80)			|
| Protocol     | name(ex: TCP) or hex number(ex: 0x06)	|

Here are the protocols our filters can recognize within a frame:
- `IPv4`
- `IPv6`
- `ARP`
- `ICMP`
- `TCP`
- `UDP`
- `IGMP`
- `EGP`
- `IGP`
- `XTP`
- `RSVP`
- `HTTP`
- `HTTPS`
- `DNS`
- `DHCP`
- `SMTP`
- `IMAP`
- `POP`
- `SSH`
- `RDP`
- `FTP`

Finally, you can provide a binary operator among: `&&` (and) and `||` (or) in order to use several filters at once.

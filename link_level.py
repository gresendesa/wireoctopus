import socket
import struct

class RawSocket:
	def __init__(self):
		self.conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))

	def read(self):
		return self.conn.recvfrom(65536)

class Ethernet:
	def __init__(self, raw_socket):
		self.raw_socket = raw_socket
		self.data = b''
		self.addr = b''
		
	#Lê bytes do socket na ordem de transmissão. Dados crus	
	def capture_bytes(self):
		self.data, self.addr = self.raw_socket.read()

	#Interpreta bytes do socket conforme a estrutura mostrada na página 349 do Kurose
	def get_frame(self):
		self.capture_bytes()
		dest_mac, src_mac, type = struct.unpack('! 6s 6s H', self.data[:14])
		return Ethernet.Frame(self.stringify_mac_addr(dest_mac), self.stringify_mac_addr(src_mac), socket.htons(type), self.data[14:])

	def frames(self):
		while 1:
			yield self.get_frame()

	def stringify_mac_addr(self, bytes_addr):
		str_addr = map('{:02x}'.format, bytes_addr)
		return ':'.join(str_addr).upper()

	class Frame:
		def __init__(self, dest, src, type, data):
			self.dest = dest
			self.src = src
			self.type = type
			self.data = data
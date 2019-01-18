import threading
import socket

class Node :

	def  __init__(self,NodeId,NodeHost,NodePort,clockwiseNeighbor,antiClockwiseNeighbor):
		
		# Base
		self.NodeId = NodeId
		self.NodeHost = NodeHost
		self.NodePort = NodePort
		self.clockwiseNeighbor = clockwiseNeighbor
		self.antiClockwiseNeighbor = antiClockwiseNeighbor
		
		# Message Handling
		self.sendBufferClockwise = []
		self.sendBufferAntiClockwise = []
		self.receiveBufferClockwise = []
		self.receiveBufferAntiClockwise = []

		# Connection Purpose
		self.endpoint = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.endpoint.bind((self.NodeHost,self.NodePort))
		self.clockwiseNeighborConnection = None
		self.antiClockwiseNeighborConnection = None


	def joinRing(self,clockwiseNeighbor,antiClockwiseNeighbor):
		

		self.clockwiseNeighborConnection = socket.socket()
		state = 0
		while state == 0 :
			try :
				self.clockwiseNeighborConnection.connect(('',clockwiseNeighbor))
			except :
				continue
			state = 1

		self.antiClockwiseNeighborConnection = socket.socket()

		state = 0
		while state == 0 :
			try :
				self.antiClockwiseNeighborConnection.connect(('',antiClockwiseNeighbor))
			except :
				continue
			state = 1
		
		print('Connections Established')
	
		

def sender(node) :

	node.endpoint.listen()
	node.endpoint.accept()
	node.endpoint.accept()


def launcher(nodeId,nodeHost,nodePort,clockwiseNeighbor,antiClockwiseNeighbor) :
	
	x = Node(nodeId,nodeHost,nodePort,clockwiseNeighbor,antiClockwiseNeighbor)
	t1 = threading.Thread(target=sender,args=(x,))
	t1.start()
	x.joinRing(clockwiseNeighbor,antiClockwiseNeighbor)
	t1.join()

	
if __name__ == "__main__" :

	n = int(input("Number of participants : "))
	threadlist = []
	for i in range(n):
		nodeId = int(input("Enter Node ID : "))
		nodeHost = 'localhost'
		nodePort = 9000+i
		if i != n-1 :
			clockwiseNeighbor = nodePort+1
		else :
			clockwiseNeighbor = 9000
		if i != 0 :
			antiClockwiseNeighbor = nodePort-1
		else :
			antiClockwiseNeighbor = 9000+n-1
		t = threading.Thread(target=launcher,args=(nodeId,nodeHost,nodePort,clockwiseNeighbor,antiClockwiseNeighbor,))
		threadlist.append(t)
		t.start()


	for t in threadlist :
		t.join()










		

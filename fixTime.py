import sys
import re
from socket import *
import threading
import time
import math
from collections import OrderedDict
from heapq import *
ip_address = "127.0.0.1"
sender_Name = sys.argv[1]
sender_Port = int(sys.argv[2])
config_file = open(sys.argv[3],'r')

socket_ = socket(AF_INET, SOCK_DGRAM)
socket_.bind(('', sender_Port))

neighbour_info = config_file.read().splitlines()
neighbour_info = neighbour_info[1:]#['B 2 2001', 'Z 5 5000']#remove number here
myGraph = dict()

# node_list=[]
dead_list=[] #nodes that are dead
#cost_list=[]
# port_list=[]
#node_list.append(s.split()[0])
#cost_list.append(float(s.split()[1]))
#port_list.append(int(s.split()[2]))
send_list = dict()
recv_list = dict()
port_to_name = dict()

def checkKey(key,dictionary):
	if key in dictionary.keys():
		return True
	else:
		return False

#returned  data does not contain the information send from this port
def makeDataPacket(send_to_port):
	data = ""

	for start in myGraph.keys():
		if start == port_to_name[send_to_port]:
			pass
		else:
			substr = start
			for dest in myGraph[start].keys():
				if dest == port_to_name[send_to_port]:
					pass
				else:
					substr = substr + " "+ dest + " " +myGraph[start][dest]
			data = data + substr + "\n"
	return data

#recieve the whole data package, separate line and put in graph
def updateNeighbour(myGraph,data):
	# print "data recieved:\n",data

	for eachLine in data.splitlines():
		nodeName = eachLine.split()[0] #A
		eachLine = eachLine.split()[1:] # B 2 2001

		for i in range(0,len(eachLine),2):

			if nodeName in myGraph.keys():
				if nodeName in myGraph[nodeName].keys():
					pass
			else:
				myGraph.setdefault(nodeName,dict())
			myGraph[nodeName][eachLine[i]]= eachLine[i+1]

	return myGraph


def getCost(start, dest):
	return myGraph[start][dest]



def dijkstra(end):
	visited = dict()
	parent = dict()
	cost = dict()
	queue = []
	result = []

	for n in myGraph.keys():
		visited[n] = False
		cost[n] = float("inf")

	#mark start node visited
	cost[sender_Name] = 0
	visited[sender_Name] = True
	# parent[sender_Name] = sender_Name

	heappush(queue,(0,sender_Name))

	# print "dijkstra ",sender_Name, " -> ",end

	while queue:
		# print "===================POP================="
		curr = heappop(queue)[1]
		# print "got ",curr

		#all nodes that can be reached from current node
		for reachable in myGraph[curr].keys():
			# print "check cost from ",curr," to ",reachable

			cost_toNode = float(cost[curr]) + float(myGraph[curr][reachable])
			#this node has not been reach from other
			if visited[reachable]:
				pass
			else:
				visited[reachable] = True

				# print "-----------"	,reachable,"visited!"
				# cost_toNode = float(cost[curr]) + float(myGraph[curr][reachable])
				# print "total cost from ",sender_Name," -> ",reachable," is ",cost_toNode

				heappush(queue, (cost_toNode,reachable))

			# for i in queue:
			# 	print i
				# print queue


			# print "new cost = ",cost_toNode," old cost = ",float(cost[reachable])
			if cost_toNode < cost[reachable]:
				# print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
				cost[reachable] = cost_toNode
				parent[reachable] = curr

			# print "\nvisited: ",visited
			# print "parent: ",parent
			# print "distance: ",cost,"\n"

	final = end
	# print "dest is ",final
	while final != sender_Name:
		# print final,"<-"
		result.insert(0,final)
		final = parent[final]
		# print final,"<-"
	result.insert(0,sender_Name)
	# print "----------------------------------------------------------------"

	# print "result: ",result," ",cost[end]
	return (result,cost[end])

def	findPath(myGraph):
	queue = []
	for nodeName in myGraph.keys():
		if nodeName != sender_Name and len(myGraph[nodeName]) != 0 :
			(nodes,cost) = dijkstra(nodeName)
			string = "".join(nodes)
			# if(len(string) == 1):
			# 	string = ""
			# else:
			heappush(queue, (nodeName,(string,cost)))
			# print "least-cost path to node %s: %s and the cost is %.1f" %(nodeName,str(string),float(cost))
		else:
			pass

	while queue:
		info = heappop(queue)
		nodeName = info[0]
		string = str(info[1][0])
		cost = float(info[1][1])
		print "least-cost path to node %s: %s and the cost is %.1f" %(nodeName,str(string),float(cost))
	# print "\nGraph is: ", myGraph
	return

def printGraphKey(myGraph):
	print "KEYS: ",
	for key in myGraph.keys():
		print key," ",
	print ""
	return




def fixGraph(myGraph, nodename):
	try:
		del myGraph[nodename]
	except KeyError:
		pass

	for keys in myGraph.keys():
		if nodename in myGraph[keys].keys():
			del myGraph[keys][nodename]
	# print "\n\n\nGraph is: ", myGraph
	return myGraph

def send_node_lost(dead_list):
	data_packege = "0"
	for node in dead_list:
		data_packege = data_packege + " "+ node

	for node_port  in port_to_name.keys():
		address = (ip_address,node_port)
		socket_.sendto(data_packege,address)
	return

def deleteNode(myGraph,send_list,recv_list,dead_list,port_to_name,nodeName):
	if nodeName not in dead_list:
		dead_list.append(nodeName)

	myGraph = fixGraph(myGraph, nodeName )
	# print "\nGraph is: ", myGraph

	try:
		del send_list[nodeName]
	except KeyError:
		pass

	try:
		del recv_list[ nodeName]
	except KeyError:
		pass

	try:
		for port in port_to_name.keys():
			if port_to_name[port] == nodeName:
				del port_to_name[port]
	except KeyError:
		pass


	return (myGraph,send_list,recv_list,dead_list,port_to_name)

def checkAlive(myGraph,send_list,recv_list,dead_list,port_to_name):
	for port in port_to_name.keys():
		if send_list[port_to_name[port]] - recv_list[port_to_name[port]] >=3:
			# print "========node ",port_to_name[port]," lost!========"
			(myGraph,send_list,recv_list,dead_list,port_to_name) = deleteNode(myGraph,send_list,recv_list,dead_list,port_to_name,port_to_name[port])


	return(myGraph,send_list,recv_list,dead_list,port_to_name)


def recv_heartbeat(data,port):
	# print "-----------------------------rcv heartbeat-----------------------------"
	# port = address[1]
	# print "heartbeat recieved from ",port_to_name[port]," is ", data

	port_name = port_to_name[port]
	recv_list[port_name] = recv_list[port_name]+1

	# print "send_list: ",send_list
	# print "recv_list: ",recv_list
	return

############################################################################

def kill_some_node(data,myGraph,send_list,recv_list,dead_list,port_to_name):
	data = data.split()[1:]
	# print data
	for nodeName in data:
		(myGraph,send_list,recv_list,dead_list,port_to_name) = deleteNode(myGraph,send_list,recv_list,dead_list,port_to_name,nodeName)
	return (myGraph,send_list,recv_list,dead_list,port_to_name)

for node_info in neighbour_info:
	myGraph.setdefault(sender_Name,dict())
	myGraph[sender_Name][node_info.split()[0]] = node_info.split()[1]
	# port_list.append(int(node_info.split()[2]))

	send_list[node_info.split()[0]] = 0
	recv_list[node_info.split()[0]] = 0

	#for debug: eg.  2003:C
	port_to_name[int(node_info.split()[2])] = node_info.split()[0]
# print "\nGraph is: ", myGraph

visited = dict()
cost = dict()
st = dict()
for nodeName in myGraph.keys():
	visited[nodeName] = False
	cost[nodeName] = float("inf")

executetime = time.time()
socket_.settimeout(0.01)
i = 0
time_ = time.time()
flag = True
print "This is for node: ", sender_Name

while True:

	(myGraph,send_list,recv_list,dead_list,port_to_name) = checkAlive(myGraph,send_list,recv_list,dead_list,port_to_name)

	#send heartbeat once pre second
	if(time.time() - time_) >= 0.5 and flag :#or i == 0:
		flag = False
		data_packege = "1"
		for node_port  in port_to_name.keys(): # or use node_list
			address = (ip_address,node_port)
			socket_.sendto(data_packege,address)
			port_name = port_to_name[node_port]
			send_list[port_name] = send_list[port_name]+1
			# print port_name

		send_node_lost(dead_list)

	# broadcasting
	if(time.time() - time_) >= 1 or i == 0:
		time_ = time.time()
		flag = True

		# data_packege = makeDataPacket()
		for node_port  in port_to_name.keys(): #recieved_List
			address = (ip_address,node_port)
			if port_to_name[node_port] == sender_Name:
				pass
			else:
				data_packege = makeDataPacket(node_port)
				socket_.sendto(data_packege,address)


		i = i +1
	try:
		data, address =  socket_.recvfrom(4096)
		from_port = address[1]

		if str(data[0]) == "0" :
			# print "===========================recieve from ",port_to_name[from_port],"==========================="
			# print "-----------------------------deleteNode-----------------------------"
			# print "recieve data: \n",data

			# (myGraph,send_list,recv_list,dead_list,port_to_name) = deleteNode(myGraph,send_list,recv_list,dead_list,port_to_name,from_port)
			(myGraph,send_list,recv_list,dead_list,port_to_name) = kill_some_node(data,myGraph,send_list,recv_list,dead_list,port_to_name)

		elif str(data[0]) == "1" :
			recv_heartbeat(data,from_port)

		else:
			# print "recieve data: \n",data,"|"
			myGraph = updateNeighbour(myGraph,data)

	except :
		pass

	if time.time() -  executetime > 30:
		i = 0
		print time.time() -  executetime
		# time_ = time.time()
		# print "=========================================================================="

		# print "\nGraph is: ", myGraph
		# print "port_to_name: ",port_to_name
		# print "send_list: ",send_list
		# print "recv_list: ",recv_list
		# print "dead_list: ",dead_list
		if len(port_to_name.keys())!=0:
			findPath(myGraph)
		print time.time() -  executetime
		executetime = time.time()


print "\nThis is for node: ", sender_Name,"\n"

import sys
import re
from socket import *
import threading
import time
import math
from collections import OrderedDict
from heapq import *

def checkKey(key,dictionary):
	if key in dictionary.keys():
		return True
	else:
		return False

def makeDataPacket():
	data = ""
	for start in myGraph.keys():
		substr = start
		for dest in myGraph[start].keys():
			substr = substr + " "+ dest + " " +myGraph[start][dest]
		data = data + substr + "\n"

	#print "data sent is ",data
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
		#myGraph[nodeName] = list(OrderedDict.fromkeys(myGraph[nodeName]))

	# print "\nGraph is: ", myGraph
	return myGraph


def getCost(start, dest):
	return myGraph[start][dest]


#
# # find the path sender_Name -> dest
# def dijkstra(dest):
#
# 	cost_toNode =0
#
# 	if dest in myGraph[sender_Name].keys():
# 		print "dijkstra ",sender_Name, " -> ",dest,
# 		cost_toNode = getCost(sender_Name,dest) #straight from this to that node
# 		print "cost is ",cost_toNode
#
# 		if dest in cost.keys():
# 			if cost[dest] > cost_toNode:
# 				print "update"
# 			else:
# 				pass
# 	return


def dijkstra(end):
	visited = dict()
	parent = dict()
	cost = dict()
	queue = []
	result = []

	# print "Graph have keys:",myGraph.keys()
	for n in myGraph.keys():
		visited[n] = False
		cost[n] = float("inf")

	#mark start node visited
	cost[sender_Name] = 0
	visited[sender_Name] = True
	# parent[sender_Name] = sender_Name

	heappush(queue,(0,sender_Name))

	print "dijkstra ",sender_Name, " -> ",end
	# print "visited: ",visited
	# print "parent: ",parent
	# print "cost: ",cost,"\n"

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
		if nodeName != sender_Name:
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

	def recv_heartbeat(data):
		print "heartbeat recieved is ", data

		return

ip_address = "127.0.0.1"
sender_Name = sys.argv[1]
sender_Port = int(sys.argv[2])
config_file = open(sys.argv[3],'r')

socket_ = socket(AF_INET, SOCK_DGRAM)
socket_.bind(('', sender_Port))

neighbour_info = config_file.read().splitlines()
neighbour_info = neighbour_info[1:]#['B 2 2001', 'Z 5 5000']#remove number here
myGraph = dict()


dead_list=[] #nodes that are dead
#cost_list=[]
port_list=[]
#node_list.append(s.split()[0])
#cost_list.append(float(s.split()[1]))
#port_list.append(int(s.split()[2]))


for node_info in neighbour_info:
	myGraph.setdefault(sender_Name,dict())
	myGraph[sender_Name][node_info.split()[0]] = node_info.split()[1]
	port_list.append(int(node_info.split()[2]))

# print "\nGraph is: ", myGraph

visited = dict()
cost = dict()
st = dict()
for nodeName in myGraph.keys():
	visited[nodeName] = False
	cost[nodeName] = float("inf")


socket_.settimeout(0.01)
i = 0
time_ = time.time()
#array = []

print "This is for node: ", sender_Name
while True:
	#data_packege = sender_Name + ' '
	#data_packege = data_packege + ' '.join(neighbour_info)


	if(time.time() - time_) >= 1 or i == 0:
		data_packege = makeDataPacket()
		#print "send data: ",data_packege
		for node_port  in port_list: # or use node_list
			#print "-----",node
			#node_port = int(myGraph[sender_Name][node])
			# print "send to ",node_port
			address = (ip_address,node_port)
			socket_.sendto(data_packege,address)

		time_ = time.time()
		i = i +1
	try:
		data, address =  socket_.recvfrom(4096)
		# print "--------------------recieve from ",data[0] ,"--------------------"

		print "recieve data: \n",data
		if str(data[0]) == "" :
			reply_heartbeat(data,address)
		else:
			myGraph = updateNeighbour(myGraph,data)
		#print "\nGraph is: ", myGraph


	except :
		pass

	if i>10:
		break


findPath(myGraph)
print "\nGraph is: ", myGraph

#!/usr/bin/python2.7
from sys import *
from socket import *
from heapq import *
from thread import *
from time import *
from collections import OrderedDict

StartNode = argv[1]
StartPort = int(argv[2])
file_input = open(argv[3],'r')
s = socket(AF_INET, SOCK_DGRAM) # UDP socket
s.bind(('127.0.0.1',StartPort))
data = file_input.read().splitlines()
length = len(data)  # get file line num
data[0] = StartNode
start = time ()
sendMe = ""
i = 0
j = 0
portList = []
recvList = []
newList = []
deadList = []
nameList = []

while i < length:
    sendMe += str(data[i])
    sendMe += " "
    i += 1

def dijkstra(Graph,start,end):
    visited = dict()
    parent = dict()
    distance = dict()
    queue = []
    path = []
    for node in Graph.keys():
        visited[node] =False
        distance[node] = float("inf")
    distance[start] =0
    heappush(queue,(0,start))
    while queue:
        current = heappop(queue)[1]
        visited[current] = True
        for connected in Graph[current].keys():
            if not visited[connected]:
                totalWeight = distance[current]+Graph[current][connected]
                heappush(queue,(totalWeight,connected))
                if totalWeight < distance[connected]:
                    distance[connected] = totalWeight
                    parent[connected] = current
    final = end
    while final != start:
        path.insert(0,final)
        if Graph[final].keys() and Graph[start].keys():
            final = parent[final]
        else:
            pass
    if start:
        path.insert(0,start)
    else:
        pass
    return (path,distance[end])

def updateGraph(recvData,graph): # data, adjList
    Start = recvData.split()[0]   # startNode
    a = recvData.split()[1:]
    new = []
    for i in range(0,len(a),3):
        new.append(a[i:i+3])
    for i in range(0,len(new)):
        nodeA = Start
        nodeB = new[i][0]
        weightAB = float(new[i][1])
        portB = int(new[i][2])
        portList.append(portB)
        nameList.append(nodeB)
        graph.setdefault(nodeA,dict())
        graph[nodeA][nodeB] = weightAB
        graph.setdefault(nodeB,dict())
        graph[nodeB][nodeA] = weightAB

def printPath(adjList):
    for dest in adjList:
        (path,shortestDist) = dijkstra(adjList,StartNode,dest)
        pathf = "".join(path)
        if(len(pathf) == 1):
            pathf = ""
        else:
            print "least-cost path to node %s: %s and the cost is %.1f" %(dest,str(pathf),float(shortestDist))


def checkAlive(graph):
    for port in newList:
        message = "heartbeat"
        host = '127.0.0.1'
        addr = (host,port)
        s.sendto(message,addr)
        s.settimeout(0.01)
        try:
            data, address = s.recvfrom(4096)
            if(data == "heartbeat"):
                recvPort = address[1]
                recvList.append(recvPort)
                if(StartPort in recvList):
                    recvList.remove(StartPort)
                else:
                    pass
            else:
                pass
        except:
            break
    return

def removeDeadNode(graph,deadList,nameList,PortList):
    ListLen = len(deadList)
    l = 0
    while(l < ListLen):
        if deadList[l] in PortList:
            DeadNodeName = nameList[PortList.index(deadList[l])]
            if DeadNodeName in graph.keys():
                del graph[DeadNodeName]
            else:
                pass
            for node in graph.keys():
                if DeadNodeName in graph[node].keys():
                    del graph[node][DeadNodeName]
                else:
                    pass
        else:
            pass
        l+=1
    return graph
# main part
adjList = dict()
portList = []
recvList = []
for line in data:
    if len(line) == 1:  # ignore the number of neighbour
        pass
    else:
        words = line.split()
        nodeA = StartNode
        nodeB = words[0]
        weightAB = float(words[1])
        portB = int(words[2])
        nameList.append(nodeB)
        portList.append(portB)
        nameList = list(OrderedDict.fromkeys(nameList))
        portList = list(OrderedDict.fromkeys(portList))
        adjList.setdefault(nodeA,dict())
        adjList[nodeA][nodeB] = weightAB
        adjList.setdefault(nodeB,dict())
        adjList[nodeB][nodeA] = weightAB

while True:  # loop forever send data
    curr = time()
    for port in portList:  #  bug here portList not update
        host = '127.0.0.1'
        addr = (host,port)
        s.sendto(sendMe,addr)
        try:
            data,address = s.recvfrom(4096)
        except:
            pass
        if(data == "heartbeat"):
            pass
        else:
            if(port == StartPort):
                pass
            else:
                s.sendto(data,addr)  # broadcasting
            checkAlive(adjList)
            updateGraph(data,adjList)
            portList = list(OrderedDict.fromkeys(portList))
            if(StartPort in portList):
                portList.remove(StartPort)
            else:
                pass
            j += 1
            portList = list(OrderedDict.fromkeys(portList))
            newList = portList
            #checkAlive(adjList)
            if curr - start >= 30 :
            #if j == 48: # 29
                start = time()
                recvList = list(OrderedDict.fromkeys(recvList))
                nameList = list(OrderedDict.fromkeys(nameList))
                deadList = list(set(portList) -set(recvList))
                if (StartNode in nameList):
                    nameList.remove(StartNode)
                else:
                    pass
                adjList = removeDeadNode(adjList,deadList,nameList,portList)
                printPath(adjList)
                print "\n"
                j=0
                recvList = []
            else:
                pass

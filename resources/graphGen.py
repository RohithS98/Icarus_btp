import random

header = '''<?xml version="1.0" encoding="UTF-8"?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlns"  
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns
     http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">
  <graph id="G" edgedefault="undirected">\n'''
  
footer = '''  </graph>
</graphml>'''

def getAdj(n):
	return [[0 for i in range(n)] for j in range(n)]

def fillGraph(p, adj, seed = None):
	if seed:
		random.seed(seed)
		
	for i in range(len(adj)):
		for j in range(i+1, len(adj)):
			if(random.random() < p):
				adj[i][j] = adj[j][i] = 1
	
	return adj
	
def DFS(temp, v, visited,adj):
	visited[v] = 1
	temp.append(v)
	for i in range(len(adj)):
		if adj[v][i] or adj[i][v]:
			if not visited[i]:
				temp = DFS(temp,i,visited,adj)
	return temp
	
def getComp(adj):
	visited = [0 for i in range(len(adj))]
	cc = []
	for i in range(len(adj)):
		if not visited[i]:
			temp = []
			cc.append(DFS(temp,i,visited,adj))
	return cc
	
def makeConnected(adj,comp):
	while len(comp) > 1:
		a = comp.pop(random.randint(0,len(comp)-1))
		b = comp.pop(random.randint(0,len(comp)-1))
		for i in range(random.randint(1,max(1,min(len(a),len(b))/2))):
			u, v = random.choice(a), random.choice(b)
			adj[u][v] = adj[v][u] = 1
		a.extend(b)
		comp.append(b)
	return adj
	
def write(adj, fileName):
	f = open(fileName, 'w')
	f.write(header)
	for i in range(len(adj)):
		f.write('<node id="'+str(i)+'"/>\n')
	
	for i in range(len(adj)):
		for j in range(i+1, len(adj)):
			if adj[i][j]:
				f.write('<edge source="'+str(i)+'" target="'+str(j)+'"/>\n')
	
	f.write(footer)
	f.close()

n = 200
p = 0.3

adj = fillGraph(p, getAdj(n))

cc = getComp(adj)
#print(cc)
#print()
adj = makeConnected(adj, cc)
write(adj, 'graph1.graphml')


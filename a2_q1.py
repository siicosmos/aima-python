''' Cmpt 310 assignment 2 question 1 
	Created by Liam Ling
	Date: Web May 29 2019'''

import random # for test p

def rand_graph(n, p):
	edges = []
	graph = {i:[] for i in range(n)} # create the defalut graph
	for i in range(n):
		for j in range(i): 
			if random.random() < p: # with probability p append edges to edges
				edges.append((i,j))

	for (i, j) in edges:
		if j not in graph[i]: # check if the edge already exist
			graph[i].append(j)
		if i not in graph[j]: # check if the edge already exist
			graph[j].append(i)
	return graph
	#print(graph)

#rand_graph(5, 0.5)

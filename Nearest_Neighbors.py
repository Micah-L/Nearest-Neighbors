#!/usr/bin/env python
from math import sqrt
import sys 
#import numpy #for generating random numbers in testing

def build_kdtree(points,depth=0):
	n = len(points)
	if n <= 0:
		return None
	axis = depth % 3
	sorted_points = sorted(points, key = lambda point: point[axis])
	return {
		'point': sorted_points[n//2], 
		'left': build_kdtree(sorted_points[:n//2], depth+1),
		'right': build_kdtree(sorted_points[n//2+1:], depth+1)
	}
	
#Can be replaced with your favorite distance function
def distance(p,q):
	d = 0
	for x,y in zip(p,q):
		d += (x-y)**2
	return sqrt(d)
	
#Returns the set of neighbors which are close enough to each node, indexed by (node_id - 1)
#Assumes points is a list of points indexed by (node_id - 1)
def tree_alg(points, radius, kdtree):
	n = len(points)
	near_neighbors = [set() for i in range(n)]
	node_lookup = {tuple(points[i]):i for i in range(len(points))}
	
	def get_neighbors_in_tree(point,radius,kdtree,depth=0):
		neighbors = set()
		axis = depth % 3
		if kdtree is None:
			return set()
		d = kdtree['point'][axis] - point[axis]
		if d >= radius:
			if d == radius:
				if distance(point,kdtree['point']) <= radius:
					neighbors.add(node_lookup[tuple(kdtree['point'])])
			#skip the right subtree
			neighbors.update(get_neighbors_in_tree(point,radius,kdtree['left'],depth+1)) 
		elif d <= -1*radius: 
			if d == radius:
				if distance(point,kdtree['point']) <= radius:
					neighbors.add(node_lookup[tuple(kdtree['point'])])
			#skip the left subtree
			neighbors.update(get_neighbors_in_tree(point,radius,kdtree['right'],depth+1)) 
		else: #cant skip either subtree since the ball will overlap with both cells
			if distance(point,kdtree['point']) <= radius:
				neighbors.add(node_lookup[tuple(kdtree['point'])])
			neighbors.update(get_neighbors_in_tree(point,radius,kdtree['left'],depth+1))
			neighbors.update(get_neighbors_in_tree(point,radius,kdtree['right'],depth+1))
		neighbors.discard(node_lookup[tuple(point)]) #remove self
		return neighbors
		
	for i in range(n):
		near_neighbors[i].update(get_neighbors_in_tree(points[i],radius,kdtree))
	
	return near_neighbors
	
	
# Used for testing/comparing
# def naive_alg(points,radius):
	# n = len(points)
	# nearest_arr = [set() for i in range(n)]
	# for i in range(n):
		# for j in range(i+1, n):
			# if distance(points[i],points[j]) <= radius:
				# nearest_arr[i].add(j)
				# nearest_arr[j].add(i)
	# return nearest_arr
	
# Used for testing
# If you uncomment this, also import numpy
# def generate_input(numpoints,filename,radius):
	# points = numpy.random.rand(numpoints,3)
	# with open(filename,"w") as fw:
		# for i in range(len(points)):
			# fw.write("{} {} {} {}\n".format(i+1,points[i][0], points[i][1], points[i][2]))
		# fw.write(str(radius))
	
	
# Assuming input file looks like this:
# node_id x y z 
#  . . . (n lines of int float float float)
# node_id x y z 
# radius (1 line. float)
# Output is formatted as such (1 line per node_id):
# [node_id] [number_of_close_nodes] [list_of_node_ids]
if __name__ == "__main__":
	if len(sys.argv) > 1:
		with open(sys.argv[1],"r") as fp:
			points = []
			for line in fp:
				if len(line.split()) > 1:
					points.append(tuple(float(x) for x in line.split()[1:]))
				else:
					radius = float(line)
	else:
		print("No input file specified.\nUsage: python {} input_file".format(sys.argv[0]))
		raise SystemExit
	kdtree = build_kdtree(points)
	nearest = tree_alg(points, radius, kdtree)
	for i in range(len(nearest)):
		n = len(nearest[i])
		print(str(i+1) + " {} ".format(n) + " ".join(map(str, map(lambda x: x+1, sorted(nearest[i]) ))))
		

		
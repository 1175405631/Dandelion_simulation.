import random 

num_nodes = 10000

file = open("peerids.txt", "w+")

for user in range(num_nodes):
	for i in range(25):
		file.write(str(random.randint(0, 1)))
		
	file.write("\n")

file.close()
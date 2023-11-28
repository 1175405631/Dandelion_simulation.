import random
import matplotlib.pyplot as plt

num_queries = 1




def count_common_prefix_bits(a, b):
    common_prefix_bits = 0
    for bit_a, bit_b in zip(a, b):
        if bit_a == bit_b:
            common_prefix_bits += 1
        else:
            break
    return common_prefix_bits



def route(target_key, peerid, routingtables):
	assert isinstance(target_key, str), f"target_key must be a string, got {type(target_key)}"
	assert isinstance(peerid, str), f"peerid must be a string, got {type(peerid)}"
	""" TO DO: Return true if target_key is found in peeridx. 
	Else return best peer to contact next as per the Kademlia 
	protocol. """
	# cloest peerid in the specific bucket
	closest_peer = None
	# smallest XOR distance in the specific bucket
	xOrSmallestDistance = None

	#if the target_key equal the peerid, directly return the true
	if(target_key == peerid):
		return True

	#calculate th xor_distance between target key and peer_id 
	xor_distance = int(target_key, 2) ^ int(peerid, 2)

	#find the correct bucket_index of src code
	k_bucket_index = 0
	while k_bucket_index < 25 - 1:
		if str(peerid)[k_bucket_index] == str(target_key)[k_bucket_index]:
			k_bucket_index += 1
		else:
			break  

	#get all the peerid in the target bucket 
	k_bucket_context = routingtables[peerid][k_bucket_index + 1]


	#find the smallest Xor distance in the bucket
	for each_value in k_bucket_context:
		each_distance = int(each_value, 2) ^ int(target_key, 2)
		if xOrSmallestDistance is None or each_distance < xOrSmallestDistance:
			closest_peer = each_value
			xOrSmallestDistance = each_distance


	return closest_peer





def recursive_search(target_key, peerid, previousId, routingtables, attackers, sourceid, peerids):


	if peerid == target_key:
		return True


	if peerid in attackers:
		#print("hei hei hei, I am the attackers : ", peerid)


		common_bits = count_common_prefix_bits(previousId, peerid)
		#print("this is common bits: ", common_bits)

		if common_bits < 4:
			#print("I think the previous node is source Node")
			if(previousId == sourceid):
				#print("Succeful attack !")
				return False
		else:
			#print("Random Guess")
			random_address = random.choice(peerids)
			if(random_address == sourceid):
				#print("Succeful attack !")
				return False

	next_peer = route(target_key, peerid, routingtables)
	previousId = peerid

	#print("right now:", peerid)
	#print("next_peer: ",next_peer)


	
	return recursive_search(target_key, next_peer, previousId,  routingtables, attackers, sourceid, peerids)


def main():

	""" Load list of peerids from file """
	peerids = []
	file = open("peerids.txt", "r")
	lines = file.readlines()
	file.close()
	for x in lines:
		x = x[:-1]
		peerids.append(x)


	# Randomly select 1000 attackers from the list of peer IDs
	attackers = random.sample(peerids, 1000)
	total_attack = 0



	""" Load routing tables from file """
	file = open("routingtables.txt", "r")
	routingtables = file.read()
	routingtables = eval(routingtables)

	file.close()	


	""" Total number of nodes, and length of key space """
	num_nodes = len(peerids)
	print("num_nodes:", num_nodes)
	key_len = len(peerids[0])	


	""" Route num_queries queries through the DHT, and measure 
	number of steps it takes to resolve each query """
	num_steps = []
	attacked_paths_count = {}
	total_search_count = {}


	for i in range(num_queries): 


		""" Target key is randomly selected from peerids """
		target_key = peerids[random.randint(0, num_nodes - 1 )]


		""" Initial peer to send query also randomly chosen """
		peerid = peerids[random.randint(0, num_nodes -1  )]
		num_steps_current = 0 
		target_key_found = False 
		

		""" Perform DHT walk until target key is found """
		each_path = [peerid]

		previousId = peerid

		#print("previousId: ", previousId)
		right_peer = route(target_key, previousId, routingtables)
		#print("TargetID: ",target_key)
		#print("RIght now Node: ", right_peer)


		
		target_key_found = recursive_search(target_key, right_peer, previousId, routingtables, attackers, peerid, peerids)

		if target_key_found == False:
			total_attack += 1



		
		#print("The target_key_found:", target_key_found)

	
		##for each_element in each_path:
			##if(each_element in attackers):
				##total_attack += 1
				# Increment the count for the corresponding search step in the attacked_paths_count dictionary
				##if num_steps_current not in attacked_paths_count:
					##attacked_paths_count[num_steps_current] = 1
				##else:
					##attacked_paths_count[num_steps_current] += 1

				##break
			

		##if num_steps_current not in total_search_count:
			##total_search_count[num_steps_current] = 1
		##else:
			##total_search_count[num_steps_current] += 1

		##num_steps.append(num_steps_current)


	print("total_attack: ", total_attack )
	print("Attacked rate: ", total_attack/ 2000)


		
	##attack_rate = {step: attacked_paths_count.get(step, 0) / total_search_count[step] for step in total_search_count}
	##total_attacker_rate = total_attack / 2000
	##""" TO DO: Plot histogram of num_steps_current """
	##print("total path which were attacked", total_attack)
	##print("total attacker rate:", total_attacker_rate)
	##print("attack rate in different search steps:", attack_rate)
	##print("attacked paths count in different search steps:", attacked_paths_count)



	##plt.bar(attack_rate.keys(), attack_rate.values(), edgecolor='red')
	##plt.title('Attack Rate in Different Search Steps')
	##plt.xlabel('Search Step')
	##plt.ylabel('Attack Rate')
	##plt.grid(True)

	##for x, y in zip(attack_rate.keys(), attack_rate.values()):
		##total_search = total_search_count[x]
		##plt.text(x, y / 2, f'({total_search})', ha='center', va='center')
		##plt.text(x, y, f'{y:.2f}', ha='center', va='bottom')

	##plt.show()



	##plt.hist(num_steps, bins=range(min(num_steps), max(num_steps) + 2, 1), edgecolor='red')
	#plt.title('Histogram of number of Steps to Resolve Queries')
	#plt.xlabel('Number of Steps In one query(Amount)')
	#plt.ylabel('Query amount(Frequency)')
	#plt.grid(True)
	#plt.show()


if __name__ == '__main__':
	main()
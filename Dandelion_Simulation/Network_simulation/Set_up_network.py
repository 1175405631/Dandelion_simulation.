import random
import matplotlib.pyplot as plt
# in your main function or wherever you load the routing tables
from dandelion_timeClock import set_dandelion_path, propagate_dandelion1
from dandelion import set_dandelion_path, propagate_dandelion, calculate_average_parents
from Kademlia_search import route, recursive_search
from generate_key import generate_keys
import Global_param




num_queries = 2000






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

	""" Set up dandelion Path """
	dandelion_path = set_dandelion_path(peerids, routingtables)
	average_parents = calculate_average_parents(dandelion_path)
	print("average_parents:", average_parents)


	""" Total number of nodes, and length of key space """
	num_nodes = len(peerids)
	print("num_nodes:", num_nodes)
	key_len = len(peerids[0])	

	generate_keys()


	""" Route num_queries queries through the DHT, and measure 
	number of steps it takes to resolve each query """
	num_steps = []
	attacked_paths_count = {}
	total_search_count = {}

	seach_success_time = 0
	avergae_latency = 0
	for i in range(num_queries): 


		
		target_key = peerids[random.randint(0, num_nodes - 1 )]
		peerid = peerids[random.randint(0, num_nodes -1  )]
		
		target_key_found = False 
		previousId = peerid

		print("Sender: ", previousId)
		right_peer = route(target_key, previousId, routingtables)

		print("TargetID: ",target_key)


		

		Global_param.global_time = 0
		search_success = propagate_dandelion(peerids, target_key, peerid, dandelion_path, routingtables, attackers)
		if not search_success:
			print("Searching Failure")
		else:
			seach_success_time += 1
			avergae_latency = avergae_latency + Global_param.global_time
			print("Global_time", Global_param.global_time)
	
		#search_success = propagate_dandelion1(global_time, peerids, target_key, peerid, dandelion_path, routingtables, attackers)
		

		

		
		#target_key_found = recursive_search(target_key, right_peer, previousId, routingtables, attackers, peerid)

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


	print("total_queries: ", num_queries)
	print("total_attack: ", num_queries - seach_success_time)
	print("Successful rate: ", seach_success_time/ 2000)
	print("Average Global_time", avergae_latency / seach_success_time)


		
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
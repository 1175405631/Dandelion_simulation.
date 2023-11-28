import random
import matplotlib.pyplot as plt
import Global_param


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





def route_3_cloest_node(target_key, peerid, routingtables):
	assert isinstance(target_key, str), f"target_key must be a string, got {type(target_key)}"
	assert isinstance(peerid, str), f"peerid must be a string, got {type(peerid)}"
    # Check if the target_key is equal to the peerid, directly return True
	if target_key == peerid:
		return True

    # Calculate the XOR distance between target_key and peer_id	
	xor_distance = int(target_key, 2) ^ int(peerid, 2)

    # Find the correct bucket_index of src code
	k_bucket_index = 0
	while k_bucket_index < 25 - 1:
		if str(peerid)[k_bucket_index] == str(target_key)[k_bucket_index]:
			k_bucket_index += 1
		else:
			break

    # Get all the peerids in the target bucket
	k_bucket_context = routingtables[peerid][k_bucket_index + 1]

    # Find the XOR distances for each peer in the bucket
	distances = []
	for each_peer in k_bucket_context:
		each_distance = int(each_peer, 2) ^ int(target_key, 2)
		distances.append((each_peer, each_distance))

    # Sort the peers by their XOR distance, then select the top 5 closest
	distances.sort(key=lambda x: x[1])
	top_5_closest_peers = [peer for peer, distance in distances[:5]]

	return top_5_closest_peers




def recursive_search(target_key, peerid, previousId, routingtables, attackers, sourceid, local_timer):
	

	if peerid == target_key:
		return local_timer

	if peerid in attackers:
		print("Encounter the attackers in Kademlia network : ", peerid)
		local_timer = local_timer + 60

		

	next_peer = route(target_key, peerid, routingtables)
	previousId = peerid
	local_timer += 1

	print("previous One:", previousId)
	print(next_peer)

	
	return recursive_search(target_key, next_peer, previousId,  routingtables, attackers, sourceid, local_timer)

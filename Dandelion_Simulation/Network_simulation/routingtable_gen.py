import random 

def index_peerids(prefix, peer_list, peer_idx_dict, key_len):

	if len(peer_list) > 1 and len(prefix) < key_len:

		list_0 = []
		list_1 = []

		prefix_len = 0
		if prefix != "":
			prefix_len = len(prefix)

		for peer in peer_list:
			if peer[prefix_len] == '0':
				list_0.append(peer)
			else:
				list_1.append(peer)

		peer_idx_dict[prefix + '0'] = list_0
		peer_idx_dict[prefix + '1'] = list_1

		index_peerids(prefix + '0', list_0, peer_idx_dict, key_len)
		index_peerids(prefix + '1', list_1, peer_idx_dict, key_len)

	return peer_idx_dict


def compute_routing_table(peerid, peerids, key_len, num_nodes, peer_idx_dict, k_bucket_size): 
	
	k_bucket = {}
	
	for i in range(1, key_len+1): 

		if i == 1:
			prefix = str((int(peerid[0]) + 1) % 2) 
		else: 
			prefix = peerid[0:i-1] + str((int(peerid[i-1]) + 1) % 2) 

		if prefix in peer_idx_dict.keys():
			eligible_peers = peer_idx_dict[prefix]

			if len(eligible_peers) > k_bucket_size:
				k_bucket[i] = random.sample(eligible_peers, k_bucket_size)
			else: 
				k_bucket[i] = eligible_peers

	return k_bucket


def main():
	peerids = []
	routing_tables = {}

	file = open("peerids.txt", "r")
	lines = file.readlines()
	file.close()
	for x in lines:
		x = x[:-1]
		peerids.append(x)	

	num_nodes = len(peerids)
	key_len = len(peerids[0])
	k_bucket_size = 3 

	peer_idx_dict = {}
	prefix = ""
	peer_idx_dict = index_peerids(prefix, peerids, peer_idx_dict, key_len)

	for i in range(num_nodes):
		k_bucket = compute_routing_table(peerids[i], peerids, key_len, num_nodes, peer_idx_dict, k_bucket_size)
		routing_tables[peerids[i]] = k_bucket

	file = open("routingtables.txt", "w+")
	file.write(str(routing_tables))
	file.close()


if __name__ == '__main__':
	main()
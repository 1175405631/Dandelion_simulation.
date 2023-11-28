import random
from Kademlia_search import route, recursive_search, route_3_cloest_node
import Global_param

child_count = {}

def set_dandelion_path(peerids, routingtables):
    dandelion_path = {}
    peerids_local = list(peerids)
    for peerid in peerids:
        if peerid in routingtables:
            valid_child_found = False

            while not valid_child_found and peerids_local:
                # Choose a random peer from peerids_local
                potential_child = random.choice(peerids_local)


                if potential_child not in child_count:
                    dandelion_path[peerid] = potential_child
                    child_count[potential_child] = 1
                    valid_child_found = True
                
                if potential_child in child_count and child_count[potential_child] < 2:
                    dandelion_path[peerid] = potential_child
                    child_count[potential_child] = child_count.get(potential_child, 0) + 1
                    valid_child_found = True

                # Remove the peer from peerids_local if it now has 2 parents
                if child_count[potential_child] >= 2:
                    peerids_local.remove(potential_child)



    return dandelion_path



import random






def propagate_dandelion1(peerids, target_key, current_node, dandelion_path, routingtables, attackers):

    sender_node = current_node
    print("Dandelion_child of Sender", dandelion_path[sender_node])
    

    def timer_expired():
            print(f"60 seconds passed without response. Node {sender_node} will choose a new Dandelion child and restart.")
            if sender_node in routingtables:
                dandelion_child = random.choice(peerids)
                dandelion_path[sender_node] = dandelion_child
    
    
    search_success = False
    

    while not search_success:
        in_stem_phase = True
        while in_stem_phase:
            # If the current node is the target key, return success
            if current_node == target_key:
                print(f"Target key {target_key} found at node {current_node}.")
                return True

            # Flip a coin
            coin_flip = random.choices(['heads', 'tails'], weights=[9, 1], k=1)[0]
            
            if coin_flip == 'heads':
                # If current_node has a Dandelion child, send the message to the child
                if current_node in dandelion_path:
                    current_node = dandelion_path[current_node]
                    print(f"Node {current_node} received the search request in the stem phase.") 
                    if current_node in attackers:
                        print(f"Node {current_node} is a attacker in dandelion, the message is dropped.")
                        timer_expired()
                        print("Choose the new dandelion children, and Start a new search !!")
                        continue
                    Global_param.global_time += 1
                else:
                    # If current_node doesn't have a Dandelion child (or its child is not available),
                    # it should enter the fluff phase
                    in_stem_phase = False
            else:
                in_stem_phase = False

        local_timer = 0
        query_time = []
        

        cloest_5_node = route_3_cloest_node(target_key, current_node, routingtables)
        print("cloest_5_node",cloest_5_node )

        # Start recursive search if target_key hasn't been found during Dandelion's path
        for i in range(3):
            search_time = recursive_search(target_key, cloest_5_node[i - 1], None, routingtables, attackers, current_node, local_timer)
            query_time.append(search_time)
            print("Each searching time", search_time )

        # Find the smallest value in query_time
        quickest_search = min(query_time)   



        print("Local_TImer", quickest_search )

        if quickest_search > 60:
            search_success = False
            print("All 3 search encounter the Back_hole attacker in Kademlia")
            timer_expired()
            continue
        else:
            Global_param.global_time += quickest_search
            
        # Check if global_time is less than 60 seconds at the end
        if Global_param.global_time < 60:
            search_success = True
        else:
            timer_expired()  # If time is more than 60s, restart the process



    return search_success









# 6.100B Problem Set 2 Spring 2023
# Graph Optimization
# Name: Vivian Hir 
# Collaborators:

# Problem Set 2
# =============
# Finding shortest paths to drive from home to work on a road network

from graph import DirectedRoad, Node, RoadMap


# PROBLEM 2: Building the Road Network
#
# PROBLEM 2.1: Designing your Graph
#
#   What do the graph's nodes represent in this problem? What
#   do the graph's edges represent? Where are the times
#   represented?
#
# Write your answer below as a comment:
# The graph's nodes are the locations 
# The graph's edges are the types of paths 
# 
#

# PROBLEM 2.2: Implementing create_graph
def create_graph(map_filename):
    """
    Parses the map file and constructs a road map (graph).

    Travel time and traffic multiplier should be each cast to a float.

    Parameters:
        map_filename : str
            Name of the map file.

    Assumes:
        Each entry in the map file consists of the following format, separated by spaces:
            source_node destination_node travel_time road_type traffic_multiplier

        Note: hill road types always are uphill in the source to destination direction and
              downhill in the destination to the source direction. Downhill travel takes
              1/4 as long as uphill travel. The travel_time represents the time to travel
              from source to destination (uphill).

        e.g.
            N0 N1 10 highway 1
        This entry would become two directed roads; one from 'N0' to 'N1' on a highway with
        a weight of 10.0, and another road from 'N1' to 'N0' on a highway using the same weight.

        e.g.
            N2 N3 7 uphill 2
        This entry would become two directed roads; one from 'N2' to 'N3' on a hill road with
        a weight of 7.0, and another road from 'N3' to 'N2' on a hill road with a weight of 1.75.
        Note that the directed roads created should have both type 'hill', not 'uphill'!

    Returns:
        RoadMap
            A directed road map representing the given map.
    """
    
    file=open(map_filename, "r")
    final_list=[]
    formatted_list=[]
    #initialize variables 
    while file: 
        line=file.readline()
        final_list.append(line)
        if line =="":
            break 
    file.close() 
    final_list=final_list[:-1]
    for path in final_list: 
        new_path=path.replace('\n', '')
        new_path=new_path.split()
        formatted_list.append(new_path)
    #open file and add path to a formatted list 
    new_map=RoadMap() 
    for obj in formatted_list: 
        source_node=Node(obj[0])
        dest_node=Node(obj[1]) #create source node and destination node 
        boolean_value_one=new_map.contains_node(source_node)
        boolean_value_two=new_map.contains_node(dest_node)
        if boolean_value_one is False: 
            new_map.insert_node(source_node)
        if boolean_value_two is False:
            new_map.insert_node(dest_node)
        #string needs to be a node 
        
       
        if obj[3]=="uphill":
            obj[3]="hill" #redefine as a hill type 
            new_road=DirectedRoad(source_node, dest_node,float(obj[2]), str(obj[3]), float(obj[4]))
            another_road=DirectedRoad(dest_node, source_node, float(obj[2])/4, str(obj[3]), float(obj[4])) #divide by 4 for time 
        else: 
            new_road=DirectedRoad(source_node, dest_node,float(obj[2]), str(obj[3]), float(obj[4]))
            another_road=DirectedRoad(dest_node, source_node, float(obj[2]), str(obj[3]), float(obj[4])) #default if not hill 
        new_map.insert_road(new_road)
        new_map.insert_road(another_road)
    return new_map

# PROBLEM 2.3: Testing create_graph
#
#   Go to the bottom of this file, look for the section under FOR PROBLEM 2.3,
#   and follow the instructions in the handout.


# PROBLEM 3: Finding the Shortest Path using Depth-First Search

# Problem 3.1: Objective function
#
#   What is the objective function for this problem? What are the constraints?
#
# Answer:
# The objective function for this problem is to find the path providing the shortest travel time  
# The constraint is that the path traveled cannot included restricted roads 
#

# PROBLEM 3.2: Implement find_shortest_path
def find_shortest_path(roadmap, start, end, restricted_roads=None, has_traffic=False):
    """
    Finds the shortest path between start and end nodes on the road map,
    without using any restricted roads, following traffic conditions.
    If restricted_roads is None, assume there are no restricted roads.
    Use the depth first search algorithm (DFS) from 6.100B lecture 3. 

    Parameters:
        roadmap: RoadMap
            The graph on which to carry out the search.
        start: Node
            Node at which to start.
        end: Node
            Node at which to end.
        restricted_roads: list of str or None
            Road Types not allowed on path. If None, all are roads allowed
        has_traffic: bool
            Flag to indicate whether to get shortest path during traffic or not.

    Returns:
        A two element tuple of the form (best_path, best_time).
            The first item is a list of Nodes, the shortest path from start to end.
            The second item is a float, the length (time traveled) of the best path.
        If there exists no path that satisfies constraints, then return None.
    """
        
    start_boolean=roadmap.contains_node(start)
    end_boolean=roadmap.contains_node(end)
    if not start_boolean: 
        return None 
    if not end_boolean: 
        return None 
    if start==end: 
        return ([start], 0)
    stack=[([start],0)] 
    best_time=float("inf") #initialize to infinity 
    best_path=[]
    while stack: 
        current_path= stack.pop()
        #check if last node in the path is the end node 
        end_node=current_path[0][-1]
        travel_time=current_path[1]
        if end_node==end:
            if travel_time<best_time: 
                best_time=travel_time
                best_path=current_path[0]
            #if distance for this path is shorter than the current distance 
            #update the distance 
        if restricted_roads is not None: 
            roads=roadmap.get_reachable_roads_from_node(current_path[0][-1], restricted_roads) #last node of the path 
        else: 
            roads=roadmap.get_reachable_roads_from_node(current_path[0][-1], []) #search for an empty list
        for road in roads:
            neighbor=road.get_destination_node()
            travel_time=road.get_travel_time(has_traffic)
            if neighbor not in current_path[0]:
                stack.append((current_path[0]+[neighbor],current_path[1]+travel_time))
    if best_path==[]:
        return None 
    return (best_path, best_time)
    #sets work by hashing stuff (give it 5, puts it at a given address determine by some function h )
    #can only put it at a given address if it is immutable. If you give it a list, change the list now it's a different list 
    #then you can't go to the list so it has to be unchangeable 
    #want to check if current_path end node is the end 
    #keep track of the best path and the best distance 

    #add the last node's neighbors update the path then add it back to the stack 
    #increase the distance by the length of the edge and time. 
    #keep the distance with the path. 
    #path as a list, distance is float (path, distance) 


# PROBLEM 4.1: Implement find_shortest_path_no_traffic
def find_shortest_path_no_traffic(filename, start, end):
    """
    Finds the shortest path from start to end during conditions of no traffic.
    Assume there are no restricted roads.

    You must use find_shortest_path.

    Parameters:
        filename: str
            Name of the map file that contains the graph
        start: Node
            Node object at which to start.
        end: Node
            Node object at which to end.

    Returns:
        A two element tuple of the form (best_path, best_time).
            The first item is a list of Nodes, the shortest path from start to end with no traffic.
            The second item is a float, the length (time traveled) of the best path.
        If there exists no path that satisfies constraints, then return None.
    """
    roadmap=create_graph(filename)
    shortest_path=find_shortest_path(roadmap, start, end)
    return shortest_path

# PROBLEM 4.2: Implement find_shortest_path_restricted
def find_shortest_path_restricted(filename, start, end):
    """
    Finds the shortest path from start to end when local roads and hill roads cannot be used.
    Assume no traffic.

    You must use find_shortest_path.

    Parameters:
        filename: str
            Name of the map file that contains the graph
        start: Node
            Node object at which to start.
        end: Node
            Node object at which to end.

    Returns:
        A two element tuple of the form (best_path, best_time).
            The first item is a list of Nodes, the shortest path from start to end given the aforementioned conditions.
            The second item is a float, the length (time traveled) of the best path.
        If there exists no path that satisfies constraints, then return None.
    """
    roadmap=create_graph(filename)
    restricted_roads=["local", "hill"]
    #should delete the roads containing this type from roadmap
    shortest_path=find_shortest_path(roadmap, start, end, restricted_roads)
    return shortest_path
    


# PROBLEM 4.3: Implement find_shortest_path_in_traffic
def find_shortest_path_in_traffic(filename, start, end):
    """
    Finds the shortest path from start to end in traffic,
    i.e. when all roads' travel times are multiplied by their traffic multipliers.

    You must use find_shortest_path.

    Parameters:
        filename: str
            Name of the map file that contains the graph
        start: Node
            Node object at which to start.
        end: Node
            Node object at which to end.

    Returns:
        A two element tuple of the form (best_path, best_time).
            The first item is a list of Nodes, the shortest path from start to end given the aforementioned conditions.
            The second item is a float, the length (time traveled) of the best path.
        If there exists no path that satisfies constraints, then return None.
    """
    roadmap=create_graph(filename)
    #if has traffic is true then you should multiply each by traffic multiplier when constructing the roadmap cause it affects time 
    shortest_path=find_shortest_path(roadmap, start, end, has_traffic=True)
    return shortest_path 


if __name__ == '__main__':

    # UNCOMMENT THE LINES BELOW TO DEBUG OR TO EXECUTE PROBLEM 2.3
    pass

   
    small_map= create_graph('./maps/road_map.txt')
    # # # ------------------------------------------------------------------------
    # # # FOR PROBLEM 2.3
    road_map = create_graph("maps/test_create_graph.txt")
    # print(second_map)
    # # ------------------------------------------------------------------------
    print(road_map)
    # start = Node('N0')
    # end = Node('N4')
    # restricted_roads = []
    # print(find_shortest_path_no_traffic('./maps/small_map.txt', start, end))
    #wrote expected and comparing it with result 

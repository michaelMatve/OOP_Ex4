# OOP_Ex4

## how to operate the project
at first you should make sure you have pygame install in your IDE. once you installed pygame, you should open the cmd. in the cmd you should go into the folder that has Ex4_Server_v0.0.jar and write in the cmd the following command : java -jar Ex4_Server_v0.0.jar X where X is the number of the case you want to check. 
## The Main Classes
The classes we chose to create are: </br>
1. Node
2. DiGraph
3. GraphAlgo
4. agent
5. pokemon
6. pokemon_game
</br>
you also have the main program which is student_code
</br>

### student_code
in this program we start to run the game. at the beginning we make a connection to the server. after that we pull information from the server about the game : the graph, the agents, and the pokemons. we set the agents to the most stratigic place and then we start the game and run in a loop until the time is up or if someone will press the stop button. in the loop we update our information about the game and every time we remove the old pokemons from the graph and set the new ones. after that, we use pygame to draw the game. the pokemon color will be red or green, depends on the type of pokemon (up or down), the nodes and edges will be in blue, and the agents will be grey. in addition, we draw the ttl, the number of moves and the grade and the right bottom of the screen. after that, we check the next node that the agent should go to, by using dijkstra algorithm for calculating the best way to capture pokemons (where to go next). we set clock to 10 ticks in a second for not getting more than 10 moves in a second.
</br>

### Agent
Agent is the class representing an agent, the field of this class are id, value, src, dest, speed, pos, time. this class has only two functions the first is init- creating a new agent. and the second one is update, which update the agents.
</br>

###Pokemons
Pokemon is the class representing a pokemon. the fields of this class are id, value, type, pos. this class has only a constructor function.
</br>

### Pokemon_game 
this class contain the game graph. in addition, it contains a dictionary of agents and a dictionary of all the information about the game. the function that this class have are : 
1. add_pokemons
2. remove_pokemons
3. add_agent
4. update_agent
</br>




### Node
Node is a class representing a vertex. we used the Node class we created in OOP_Ex3 project, but we added 2 fields to this function. the first is value, and the second is type.  the fields of this graph are id, pos, in_edges, out_edges, tag, weight and info. this class has a constructor that gets an id and position and creates new Node that has no edges (in or out) and sets the tag to -1, the weight to 0.0 and the info to "w" - white.
</br>

### DiGraph
DiGraph is a class representing a graph, that implements GraphInterface. once again we used the same DiGraph we used in OOP_Ex3 project, and we added a few functions : minx which returns the min x in the graph, miny which reutrns the min y in the graph, maxx and maxy are the same. in addition, we added the function add_pokemon that take a pokemon, find the right edge and add it to the graph by removing the edge and connnect the pokemon with 2 new edges one to src and the other to dest (we can know which node is pokemon by checking if the id is a round number or not. the other fucntion removes all the pokemons from the graph and add a new edge instead of the pokemon (in the right way). it fields are a dictionary of nodes that the key is the node id, and the value is Node. it also has a num_nodes that is the number of nodes in the graph, num_edges which is the number of edges int the graph, and also mc that is the number of changes made in the graph. this class has a constructor that creates an empty dict of nodes, sets num_node and num_edges to 0, and sets mc to 0. this class implements the following functions: </br>
1. v_size </br> this function returns num_nodes
2. e_size </br> this function returns num_edges
3. get_all_v </br> this function returns a dictionary of all the nodes in the graph
4. all_in_edges_of_node </br> this function gets a node id and returns the number of in_edges this node has
5. all_out_edges_of_node </br> this function gets a node id and returns the number of out_edges this node has
6. get_mc </br> this function returns the number of changes made in the graph
7. add_edge </br> this function gets and edge info (node src, node dest, weight), checks if the nodes exist, if there is an edge between them already, and if not creates a new edge
8. add_node </br> this function gets a node id and a node pos, checks if this node is already exist in the graph, and if not creates a node with this info
9. remove_edge </br> this function gets a node src and node dest, checks if the nodes exist in the graph, if so checks if there is an edge between this nodes, if so it deletes this edge from the graph by updating each node's in and out edges dict
10. remove_node </br> this function gets a node id, checks if this node exists in the graph, if so, goes through the dict of nodes and deletes every edge that has this node as a src or dest 
</br>

### GraphAlgo
GraphAlgo is a class that implements different algorithms on a graph, this class implements GraphAlgoInterface. we used the same GrapAlgo from OOP_Ex3 project and added a function that finds the next node to go to for the agent by using dijkstra algorithm and calculating the most valuable to go to. this class has only one field which is a directed graph - DiGraph. this class has a constructor that gets a DiGraph and sets the graph to it, if its empty it creates a new DiGraph.
this class has the following function:
1. get_graph </br> this function returns the graph which we perform the algorithms on
2. load_from_json </br> this function gets a string in a json format and creates a new graph from it. we create a new dictionary from the json file, and then we go through the dictionary and creates a DiGraph from it.
3. save_to_json </br> this function gets a json file name and creates a json file that has all the info of the DiGraph we are working on. we use to_json_file function that helps us convert our graph to the right objects that fits the json file format we got.
4. shortest_path </br> this function gets source and destination and computes the shortest path distance from src to dest and also the path itself. in this function we used the dijkstra algorithm. we created a helper function that called dijkstra_algo, the function uses set_tags_weight that sets the info of every node to "w" (it means that this node wasnt visited), the starting shortest path dist is float("inf") (no path), and the tag is set to -1 and will show us the key of the previous node in the path. the algorithm starts to run from the source node and tags him as visited, and update the distance to the neighbour nodes. after that, we take other node that wasnt visited and have the shortest path and checks the distance to the neighbour, and if the distance + this node shortest path smaller than the neighbour, we update the neighbour path, and the tag. we will run on all the nodes that we could go to them from the source. this function sets the graph such that every node in the graph holds the shortest path from the source node. and every node contain the previous node on the path. after the dijkstra_algo function finishes we create a new list that will hold all the nodes in the path, if the destination node is equal to -1, we return the tuple (float("inf"), []). if not we will run in a loop until we reach the src node, and in every iteration we will add a node to the list. then we return a tuple that contains the shortest path dist and the path itself.
5. TSP </br> this function gets a list and return  a tuple contains a list of the path, and the distance. we use the greedy algorithm of the traveling salesman problem. we start from the first node in the list given and by using dijkstra_algo we use the graph that helps us find the node that has the shortest path from this node. we create a list with a path from the node to it closet node , and we add it to the answer list, and we remove from the given list the nodes we visited. then we do the same with the node that was the closet one to the previous node, until we will visit all the nodes in the given list. 
6. centerPoint </br> this function checks if the graph is connected, if not returns a tuple - (-1 , float("inf")), else, we run through all the nodes and for every node we use max_dist function that returns the largest path from other node, by using dijkstra_algo. if the longest path we will get is shorter than all the previous minimum longest path we update the minimum and save the node. in the end we take the node with shortest longest path and return a tuple contains the center and the minimum largest distance.
7. plot_graph </br> this function draws the graph. at first, this function checks if there are node that dont have pos, if so it uses the random_pos function that creates random pos. after that we go through all the nodes in the graph, and draw it. and for every node we draw its out_edges.
8. is_connected </br> this function check if the graph is strongly connected components.at first,  we set all the tags of the nodes in this graph to -1, then we do dfs on the first node of the graph, and then we go through all the nodes in the graph. if there is a node that its tag is -1 it means that the graph is not connected. if not, we create a transpose graph using the get_transpose function, sets all the nodes' tag to -1, and do dfs on the first node. then, we go through all the nodes in the transpose graph, if there is a node with tag -1, it means the graph is not connected. if not, it means the graph is SCC.
9. dfs </br> this function is an iterative dfs. we get a node and adds him to a stack, then run while the stack is not empty, we check if we didnt touch the first node in the stack, if we didnt touch him we change his tag, and then run through all his out_edges and add the nodes that we didnt touch to the stack.
10. get_transpose </br> this function changes the graph to a transpose graph. we switch between in_edges to out_edges.
</br>

in addition we have 4 unittests that checks the correctness of the algorithms and the classes.










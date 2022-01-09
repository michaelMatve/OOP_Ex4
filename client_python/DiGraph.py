import math

from GraphInterface import GraphInterface
from node import Node

"""
this class DiGraph implements the GraphAlgoInterface.
this class contains dict of all the graph nodes named nodes , int num_nodes-number of nodes in graph ,
int num_edges- number of edges and int mc-number of changes

"""
class DiGraph(GraphInterface):
    def __init__(self):
        self.nodes = {}
        self.num_nodes = 0
        self.num_edges = 0
        self.mc = 0

    """
    return the node number
    """
    def v_size(self) -> int:
        return self.num_nodes

    """
     return the edge number
    """
    def e_size(self) -> int:
        return self.num_edges

    def get_all_v(self) -> dict:
        return self.nodes

    """
     return all the incoming edges
    """
    def all_in_edges_of_node(self, id1: int) -> dict:
        if self.nodes.get(id1) != None:
            return self.nodes[id1].in_edges
        return None

    """
     return all the out edges
    """
    def all_out_edges_of_node(self, id1: int) -> dict:
        if self.nodes.get(id1) != None:
            return self.nodes[id1].out_edges
        return None
    """
    return the number of changes
    """
    def get_mc(self) -> int:
        return self.mc
    """
     if the graph has the node source and the dest node 
     and there is no edge in this direction the function will add new edge
     to the graph
     """
    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if self.nodes.get(id1) == None:
            return False
        if self.nodes.get(id2) == None:
            return False
        if self.nodes.get(id1).out_edges.get(id2) != None:
            return False
        self.nodes.get(id1).out_edges[id2] = weight
        self.nodes.get(id2).in_edges[id1] = weight
        self.num_edges += 1
        self.mc += 1
        return True
    """
    checks if the node is exsit and if not we make new nude and add it to the graph
    """
    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if self.nodes.get(node_id) != None:
            return False
        self.nodes[node_id]= Node(node_id, pos)
        self.num_nodes += 1
        self.mc += 1
        return True
    """
    we run on all the nodes and use remove edge function on every node(with the node we want to remove
    if there is edge we will remove it else we do nothing.
    and in the end we remove the node from the dict by useing pop
    """
    def remove_node(self, node_id: int) -> bool:
        if self.nodes.get(node_id) == None:
            return False
        for node in self.nodes.values() :
            if node.id != node_id:
                if self.remove_edge(node_id, node.id)==True:
                    self.mc +=1
                if self.remove_edge(node.id, node_id)==True:
                    self.mc +=1
        self.nodes.pop(node_id)
        self.num_nodes -= 1
        self.mc += 1
        return True
    """
    we check if the node id1 and id2 is in our graph and if they are we remove the edge
    """
    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if self.nodes.get(node_id1) == None:
            return False
        if self.nodes.get(node_id2) == None:
            return False
        if self.nodes.get(node_id1).out_edges.get(node_id2) == None:
            return False
        self.nodes.get(node_id1).out_edges.pop(node_id2)
        self.nodes.get(node_id2).in_edges.pop(node_id1)
        self.num_edges -= 1
        self.mc += 1
        return True

    def getminx(self):
        minx = float("inf")
        for n in self.nodes.values():
            if n.pos[0]<minx:
                minx = n.pos[0]
        return minx

    def getminy(self):
        miny = float("inf")
        for n in self.nodes.values():
            if n.pos[1]<miny:
                miny = n.pos[1]
        return miny

    def getmaxx(self):
        maxx = 0.0
        for n in self.nodes.values():
            if n.pos[0]>maxx:
                maxx = n.pos[0]
        return maxx

    def getmaxy(self):
        maxy = 0.0
        for n in self.nodes.values():
            if n.pos[1]>maxy:
                maxy = n.pos[1]
        return maxy
    def checkpokesrcanddst(self, pokemon):
        for srcn in self.nodes.values():
            for e in srcn.out_edges:
                dstn = self.nodes.get(e)
                if pokemon.type == 1 :
                    if dstn.id > srcn.id :
                        if self.checkonedge(srcn.pos,dstn.pos,pokemon.pos):
                            return (srcn,dstn)
                else:
                    if dstn.id < srcn.id :
                        if self.checkonedge(srcn.pos,dstn.pos,pokemon.pos):
                            return (srcn,dstn)

    def checkonedge (self, srcp , dstp , pokemonp):
        destnodes = self.edgelong(srcp,dstp)
        destpokedest = self.edgelong(pokemonp,dstp)
        destpokesrc =  self.edgelong(pokemonp,srcp)
        dest = abs(destnodes-destpokesrc-destpokedest)
        if dest<0.00001:
            return True
        return False

    def edgelong(self, point1 , point2):
        destx = abs(point1[0]-point2[0])
        destx =destx*destx
        desty = abs(point1[1] - point2[1])
        desty = desty * desty
        dest  = desty+destx
        return math.sqrt(dest)

    def add_pokemon(self, pokemon):
        self.add_node(pokemon.id, pokemon.pos)
        src, dest = self.checkpokesrcanddst(pokemon)
        pnode = self.nodes.get(pokemon.id)
        pnode.value = pokemon.value
        pnode.type == pokemon.type
        pnode.in_edges[src.id]= self.nodes.get(src.id).out_edges[dest.id]
        src.out_edges[pnode.id] = self.nodes.get(src.id).out_edges[dest.id]
        pnode.out_edges[dest.id] = 0
        dest.in_edges[pnode.id] = 0
        self.remove_edge(src,dest)

    def gremove_pokemons(self):
        removelst =[]
        for n in self.nodes.values():
            if n.id!=int(n.id):
                removelst.insert(0,n.id)
                for s in n.in_edges :
                    for d in n.out_edges :
                        self.add_edge(s,d,n.out_edges[d])
        while len(removelst)!=0:
            self.remove_node(removelst.pop())

    def __str__(self):
        return "Graph: |V|={}, |E|={}".format(self.num_nodes, self.num_edges)



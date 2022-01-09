"""
this is class represent an node that contain pos and id.
in addition every node has 2 dicts one for all the incoming edges and one for all the out edges
"""

class Node:
    def __init__(self,id: int, pos: tuple = None):
        self.pos = pos
        self.id = id
        self.in_edges = {}
        self.out_edges = {}
        self.tag = -1
        self.weight = float('inf')
        self.info = 'w'

    def __repr__(self):
        return "{}: |edges_out| {} |edges in| {}".format(self.id, len(self.out_edges), len(self.in_edges))




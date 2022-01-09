from GraphAlgo import GraphAlgo

class Pokemon_game:
    def __init__(self, gamedata: dict):
        self.gamedata = gamedata
        self.grathalgo = GraphAlgo()
        self.agents = {}
    """
    add new pokemons from the list to the grath
    """
    def add_pokemons(self, pokemons):
        grath = self.grathalgo.graph
        while(len(pokemons)!=0):
            grath.add_pokemon(pokemons.pop())
    """
    remove all the pokemons from the grath
    """
    def remove_pokemons(self):
        self.grathalgo.graph.gremove_pokemons()

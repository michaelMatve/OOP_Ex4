from GraphAlgo import GraphAlgo

class Pokemon_game:
    def __init__(self, gamedata: dict):
        self.gamedata = gamedata
        self.grathalgo = GraphAlgo()
        self.agents = {}

    def add_pokemons(self, pokemons :list):
        grath = self.grathalgo.graph
        while(len(pokemons)!=0):
            grath.add_pokemon(pokemons.pop())

    def remove_pokemons(self):
        self.grathalgo.graph.gremove_pokemons()

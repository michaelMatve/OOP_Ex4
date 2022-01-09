import json

class Pokemon:
    def __init__(self, pokemondata :dict, uid: float):
        self.id = uid
        self.value = pokemondata['value']
        self.type = pokemondata['type']
        self.pos = tuple(float(s) for s in pokemondata['pos'].strip("()").split(","))


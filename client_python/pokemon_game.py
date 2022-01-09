from GraphAlgo import GraphAlgo

class Pokemon_game:
    def __init__(self, gamedata: dict):
        self.gamedata = gamedata
        self.grathalgo = GraphAlgo()
        self.agents = {}

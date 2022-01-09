from types import SimpleNamespace
from client import Client
from pokemon_game import Pokemon_game
from DiGraph import DiGraph
from agent import Agent
from pokemon import Pokemon
import json
from pygame import gfxdraw
import pygame
from pygame import *

# init pygame
WIDTH, HEIGHT = 1080, 720

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'

client = Client()
client.start_connection(HOST, PORT)


"""
from here you can change
"""

"""
make mygame object
get info of game to object
"""
gamedata = json.loads(client.get_info())
gamedata = gamedata['GameServer']
myGame = Pokemon_game(gamedata)

"""
get the graph 

graph_json = client.get_graph()
graph = json.loads(graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict)) # make graph
for n in graph.Nodes:
    x, y, _ = n.pos.split(',')
    n.pos = SimpleNamespace(x=float(x), y=float(y))
"""
myGame.grathalgo.load_from_json(client.get_graph())

"""
get all the pokemons:

pokemons = client.get_pokemons()
pokemons_obj = json.loads(pokemons, object_hook=lambda d: SimpleNamespace(**d)) # make pokemon list?
print(pokemons)
"""

pokemons = json.loads(client.get_pokemons())
lstpokemon = pokemons['Pokemons']
newlstpokemon = []
for p in lstpokemon:
    newlstpokemon.insert(0,Pokemon(p['Pokemon']))
print(myGame.gamedata['agents'])
for i in range (myGame.gamedata['agents']):
    client.add_agent("{\"id\":"+str(i)+"}")
agents = json.loads(client.get_agents())
lstagents = agents['Agents']
newlstagents = []
for i,p in enumerate (lstagents):
    myGame.agents[i]=Agent(p['Agent'])
    print(i)
    print(myGame.agents.get(i).id)


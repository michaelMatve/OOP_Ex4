from pokemon import Pokemon
from agent import Agent
from pokemon_game import Pokemon_game
from client import Client
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
pygame.init()

screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()
pygame.font.init()

client = Client()
client.start_connection(HOST, PORT)

FONT = pygame.font.SysFont('Arial', 20, bold=True)

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

myGame.grathalgo.load_from_json(client.get_graph())

pokemons = json.loads(client.get_pokemons())
lstpokemon = pokemons['Pokemons']
newlstpokemon = []
nuid = 0.5
for p in lstpokemon:
    newlstpokemon.insert(0,Pokemon(p['Pokemon'], nuid))
    nuid = nuid+1

min_x = myGame.grathalgo.graph.getminx()
min_y = myGame.grathalgo.graph.getminy()
max_x = myGame.grathalgo.graph.getmaxx()
max_y = myGame.grathalgo.graph.getmaxy()


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data-min_data)) * (max_screen - min_screen) + min_screen

def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height()-50, min_y, max_y)


radius = 15

for i in range (myGame.gamedata['agents']):
    client.add_agent("{\"id\":"+str(i)+"}")
agents = json.loads(client.get_agents())
lstagents = agents['Agents']
newlstagents = []
for i,p in enumerate (lstagents):
    myGame.agents[i]=Agent(p['Agent'])

# this commnad starts the server - the game is running now
client.start()

while client.is_running() == 'true':
    """
    pokemons = json.loads(client.get_pokemons(),object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    pokemons = [p.Pokemon for p in pokemons]
    """
    pokemons = json.loads(client.get_pokemons())
    lstpokemon = pokemons['Pokemons']
    newlstpokemon = []
    nuid = 0.5
    for p in lstpokemon:
        newlstpokemon.insert(0, Pokemon(p['Pokemon'], nuid))
        nuid = nuid + 1

    for p in newlstpokemon:
        x, y, _ = p.pos
        p.pos = (my_scale(float(x), x=True), my_scale(float(y), y=True), 0)
    """
    agents = json.loads(client.get_agents(),object_hook=lambda d: SimpleNamespace(**d)).Agents
    agents = [agent.Agent for agent in agents]
    """

    agents = json.loads(client.get_agents())
    lstagents = agents['Agents']
    newlstagents = []
    for i, p in enumerate(lstagents):
        myGame.agents[i] = Agent(p['Agent'])

    for a in myGame.agents.values():
        x, y, _ = a.pos
        a.pos = (my_scale(float(x), x=True), my_scale(float(y), y=True), 0)
    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    # refresh surface
    screen.fill(Color(0, 0, 0))

    # draw nodes
    for n in myGame.grathalgo.graph.nodes.values():
        x = my_scale(n.pos[0], x=True)
        y = my_scale(n.pos[1], y=True)

        # its just to get a nice antialiased circle
        gfxdraw.filled_circle(screen, int(x), int(y), radius, Color(64, 80, 174))
        gfxdraw.aacircle(screen, int(x), int(y), radius, Color(255, 255, 255))

        # draw the node id
        id_srf = FONT.render(str(n.id), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)
        for e in n.out_edges:
            # find the edge nodes
            src = n
            dest = myGame.grathalgo.graph.nodes[e]

            # scaled positions
            src_x = my_scale(src.pos[0], x=True)
            src_y = my_scale(src.pos[1], y=True)
            dest_x = my_scale(dest.pos[0], x=True)
            dest_y = my_scale(dest.pos[1], y=True)

            # draw the line
            pygame.draw.line(screen, Color(61, 72, 126), (src_x, src_y), (dest_x, dest_y))


    # draw agents
    for agent in myGame.agents.values():
        pygame.draw.circle(screen, Color(122, 61, 23), (int(agent.pos[0]), int(agent.pos[1])), 10)
    # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
    for p in newlstpokemon: pygame.draw.circle(screen, Color(0, 255, 255), (int(p.pos[0]), int(p.pos[1])), 10)

    # update screen changes
    display.update()

    # refresh rate
    clock.tick(60)

    # choose next edge
    for agent in myGame.agents.values():
        if agent.dest == -1:
            next_node = (agent.src - 1) % (myGame.grathalgo.graph.num_nodes)
            client.choose_next_edge('{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
            ttl = client.time_to_end()
            print(ttl, client.get_info())

    client.move()
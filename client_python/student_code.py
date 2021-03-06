import time
from pokemon import Pokemon
from agent import Agent
from pokemon_game import Pokemon_game
from client import Client
import json
import time
from pygame import gfxdraw
import pygame
from pygame import *
from timeit import default_timer as timer

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
client = Client()
client.start_connection(HOST, PORT)

"""
make mygame object
and
get info of game to object
"""
gamedata = json.loads(client.get_info())
gamedata = gamedata['GameServer']
myGame = Pokemon_game(gamedata)
"""
insert the grath data to the game
"""
myGame.grathalgo.load_from_json(client.get_graph())
"""
insert first pokeomn list
we do to list one to use for add to the grath and the other one is used to put the agents
"""
pokemons = json.loads(client.get_pokemons())
lstpokemon = pokemons['Pokemons']
newlstpokemon = []
newlstpokemon2 = []
nuid = 0.5
for p in lstpokemon:
    newlstpokemon2.insert(0, Pokemon(p['Pokemon'], nuid))
    newlstpokemon.insert(0,Pokemon(p['Pokemon'], nuid))
    nuid = nuid+1

"""
Add all the agents to the server
first we will add them close to the pokemon
and if we have no more pokemon we will put the in defult index
"""
for i in range (myGame.gamedata['agents']):
    if len(newlstpokemon2) != 0:
        src, dst = myGame.grathalgo.graph.check_poke_srcanddst(newlstpokemon2.pop())
        client.add_agent("{\"id\":" + str(src.id) + "}")
    else:
        client.add_agent("{\"id\":" + str(i) + "}")
"""
Add all the agents to the mygame 
"""
myGame.add_agents(json.loads(client.get_agents()))

# init pygame and set difult width and high
WIDTH, HEIGHT = 1080, 720
pygame.init()

screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()
pygame.font.init()
FONT = pygame.font.SysFont('Arial', 20, bold=True)

"""
get min and max of node for scale
"""
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

# this commnad starts the server - the game is running now
client.start()
"""
we use try becouse if the time will finished we could not go to the server and we will close the game
"""
first_time = int(client.time_to_end())
try:
    while client.is_running() == 'true':
        """
        Get all new pokemons
        """
        gamedata = json.loads(client.get_info())
        myGame.updateinfo(gamedata['GameServer'])
        pokemons = json.loads(client.get_pokemons())
        lstpokemon = pokemons['Pokemons']
        newlstpokemon = []
        nuid = 0.5
        for p in lstpokemon:
            newlstpokemon.insert(0, Pokemon(p['Pokemon'], nuid))
            nuid = nuid + 1
        num_pokemon = len(lstpokemon)
        """
            update the agents.
        """
        myGame.update_agents(json.loads(client.get_agents()))

        for a in myGame.agents.values():
            x, y, _ = a.pos
            a.pos = (my_scale(float(x), x=True), my_scale(float(y), y=True), 0)
        # check events
        """
        check if we finish the game
        """
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pos()[0] >= (int(my_scale(max_x, x=True)))-50 and pygame.mouse.get_pos()[1] >= (my_scale(max_y, y=True))-30:
                        client.stop()
                        pygame.quit()
                        exit(0)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

        # refresh surface
        screen.fill(Color(0, 0, 0))
        """
        remove old pokemons
        """
        myGame.remove_pokemons()
        """
        add new pokemons
        """
        myGame.add_pokemons(newlstpokemon)
        """
        drow the grath
        first we run other all the nodes(pokemons and realnodes)
        """
        for n in myGame.grathalgo.graph.nodes.values():
            x = my_scale(n.pos[0], x=True)
            y = my_scale(n.pos[1], y=True)
            if n.id == int(n.id):# check if the node is pokemon ar not we know pokemon id is float and node id is round int
                gfxdraw.filled_circle(screen, int(x), int(y), radius, Color(64, 80, 174)) # node print in one color
                gfxdraw.aacircle(screen, int(x), int(y), radius, Color(255, 255, 255))
                id_srf = FONT.render(str(n.id), True, Color(255, 255, 255))
            else:
                if n.type != -1:# we check if the pokemon go up ar down
                    gfxdraw.filled_circle(screen, int(x), int(y), radius, Color(255, 0, 0)) #drow in other color and write pu
                    gfxdraw.aacircle(screen, int(x), int(y), radius, Color(255, 255, 255))
                    id_srf = FONT.render('pu', True, Color(255, 255, 255))
                else:
                    gfxdraw.filled_circle(screen, int(x), int(y), radius, Color(0, 255, 0))#drow in other color and write pd
                    gfxdraw.aacircle(screen, int(x), int(y), radius, Color(255, 255, 255))
                    id_srf = FONT.render('pd', True, Color(255, 255, 255))

            rect = id_srf.get_rect(center=(x, y))
            screen.blit(id_srf, rect)
            # go other and drow all nude out edges
            for e in n.out_edges:
                src = n
                dest = myGame.grathalgo.graph.nodes[e]

                # set the x,y src and x,y dst
                src_x = my_scale(src.pos[0], x=True)
                src_y = my_scale(src.pos[1], y=True)
                dest_x = my_scale(dest.pos[0], x=True)
                dest_y = my_scale(dest.pos[1], y=True)

                # draw the line
                pygame.draw.line(screen, Color(61, 72, 126), (src_x, src_y), (dest_x, dest_y))

        # draw agents
        for agent in myGame.agents.values():
            gfxdraw.filled_circle(screen, (int(agent.pos[0])),int(agent.pos[1]), radius, Color(70, 80, 80))
            gfxdraw.aacircle(screen, int(x), int(y), radius, Color(255, 255, 255))
            id_srf = FONT.render(str(agent.id), True, Color(255, 255, 255))
            rect = id_srf.get_rect(center=((int(agent.pos[0])),int(agent.pos[1])))
            screen.blit(id_srf, rect)

        """
        drow moves 
        """
        id_srf = FONT.render('moves:', True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(((int(my_scale(max_x, x=True))) - 50), int((my_scale(max_y, y=True))) - 120))
        screen.blit(id_srf, rect)

        id_srf = FONT.render(str(str(myGame.gamedata['moves'])), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(((int(my_scale(max_x, x=True)))), int((my_scale(max_y, y=True))) - 120))
        screen.blit(id_srf, rect)

        """
        drow ttl 
        """
        id_srf = FONT.render('ttl:', True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(((int(my_scale(max_x, x=True)))-50), int((my_scale(max_y, y=True))) - 40))
        screen.blit(id_srf, rect)

        id_srf = FONT.render(str(client.time_to_end()), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(((int(my_scale(max_x, x=True)))), int((my_scale(max_y, y=True))) - 40))
        screen.blit(id_srf, rect)
        """
        drow grade
        """
        id_srf = FONT.render('grade:', True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(((int(my_scale(max_x, x=True))) - 50), int((my_scale(max_y, y=True))) - 80))
        screen.blit(id_srf, rect)

        id_srf = FONT.render(str(myGame.gamedata['grade']), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(((int(my_scale(max_x, x=True)))), int((my_scale(max_y, y=True))) - 80))
        screen.blit(id_srf, rect)

        """
        drow buttomcd 
        """
        FONT1 = pygame.font.SysFont('Arial', 30, bold=True)
        id_srf = FONT1.render(str('stop'), True, Color(255, 255, 255))
        stopButtom = id_srf.get_rect(center=(((int(my_scale(max_x, x=True)))), int((my_scale(max_y, y=True)))))
        screen.blit(id_srf, stopButtom)

        # and we update the scream
        display.update()

        # refresh rate  10 times in secend becouse we dont want to cal the server more then 10 times in sec
        clock.tick(10)

        """
        now we check for every egent what should be his next move by makeing dikstra on the agent src we find the most valued
        place to go (most value == value/time).
        if the nude is still moving we just take down the pokemon from the grafe (becouse we want that two agent will not go to same 
        pokemon)
        if the node isnt moveing we take the pokemon from the grafe and tell him to go to the next node in the way.
        """
        for agent in myGame.agents.values():
            if agent.dest == -1:
                next_node = myGame.grathalgo.getwhereto(agent.src, 0)
                temptime = myGame.grathalgo.graph.nodes.get(agent.src).out_edges[next_node]
                agent.time = temptime/agent.speed*200
                if agent.src != next_node:
                    client.choose_next_edge('{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
            else:
                next_node = myGame.grathalgo.getwhereto(agent.dest, agent.time)
                if agent.src != next_node:
                    client.choose_next_edge('{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
        client.move()


except IOError as e:
    pygame.quit()
    exit(0)
# game over:
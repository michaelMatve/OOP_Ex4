from unittest import TestCase
from pokemon_game import Pokemon_game
from client import Client
from pokemon import Pokemon
import json
from agent import Agent

PORT = 6666
HOST = '127.0.0.1'

class TestPokemon_game(TestCase):
    def test_add_pokemons(self):
        client = Client()
        client.start_connection(HOST, PORT)
        gamedata = json.loads(client.get_info())
        gamedata = gamedata['GameServer']
        myGame = Pokemon_game(gamedata)
        myGame.grathalgo.load_from_json(client.get_graph())
        pokemons = json.loads(client.get_pokemons())
        lstpokemon = pokemons['Pokemons']
        newlstpokemon = []
        nuid = 0.5
        for p in lstpokemon:
            newlstpokemon.insert(0, Pokemon(p['Pokemon'], nuid))
            nuid = nuid + 1

        pos = newlstpokemon[0].pos
        self.assertEqual(newlstpokemon[0].id,0.5)
        self.assertEqual(myGame.grathalgo.graph.nodes.get(0.5), None)
        myGame.add_pokemons(newlstpokemon)
        self.assertEqual(myGame.grathalgo.graph.nodes[0.5].pos, pos)


    def test_remove_pokemons(self):
        client = Client()
        client.start_connection(HOST, PORT)
        gamedata = json.loads(client.get_info())
        gamedata = gamedata['GameServer']
        myGame = Pokemon_game(gamedata)
        myGame.grathalgo.load_from_json(client.get_graph())
        pokemons = json.loads(client.get_pokemons())
        lstpokemon = pokemons['Pokemons']
        newlstpokemon = []
        nuid = 0.5
        for p in lstpokemon:
            newlstpokemon.insert(0, Pokemon(p['Pokemon'], nuid))
            nuid = nuid + 1

        pos = newlstpokemon[0].pos
        myGame.add_pokemons(newlstpokemon)
        self.assertEqual(myGame.grathalgo.graph.nodes[0.5].pos, pos)
        myGame.remove_pokemons()
        self.assertEqual(myGame.grathalgo.graph.nodes.get(0.5), None)



    def test_add_agents(self):
        client = Client()
        client.start_connection(HOST, PORT)
        gamedata = json.loads(client.get_info())
        gamedata = gamedata['GameServer']
        myGame = Pokemon_game(gamedata)
        myGame.grathalgo.load_from_json(client.get_graph())
        pokemons = json.loads(client.get_pokemons())
        lstpokemon = pokemons['Pokemons']
        newlstpokemon = []
        newlstpokemon2 = []
        nuid = 0.5
        for p in lstpokemon:
            newlstpokemon2.insert(0, Pokemon(p['Pokemon'], nuid))
            newlstpokemon.insert(0, Pokemon(p['Pokemon'], nuid))
            nuid = nuid + 1

        myGame.add_pokemons(newlstpokemon)
        for i in range(myGame.gamedata['agents']):
            if len(newlstpokemon2) != 0:
                src, dst = myGame.grathalgo.graph.check_poke_srcanddst(newlstpokemon2.pop())
                client.add_agent("{\"id\":" + str(src.id) + "}")
            else:
                client.add_agent("{\"id\":" + str(i) + "}")

        agents = json.loads(client.get_agents())
        self.assertEqual(len(myGame.agents), 0)
        myGame.add_agents(agents)
        self.assertNotEqual(len(myGame.agents), 0)



    def test_update_agents(self):
        client = Client()
        client.start_connection(HOST, PORT)
        gamedata = json.loads(client.get_info())
        gamedata = gamedata['GameServer']
        myGame = Pokemon_game(gamedata)
        myGame.grathalgo.load_from_json(client.get_graph())
        pokemons = json.loads(client.get_pokemons())
        lstpokemon = pokemons['Pokemons']
        newlstpokemon = []
        newlstpokemon2 = []
        nuid = 0.5
        for p in lstpokemon:
            newlstpokemon2.insert(0, Pokemon(p['Pokemon'], nuid))
            newlstpokemon.insert(0, Pokemon(p['Pokemon'], nuid))
            nuid = nuid + 1

        myGame.add_pokemons(newlstpokemon)
        for i in range(myGame.gamedata['agents']):
            if len(newlstpokemon2) != 0:
                src, dst = myGame.grathalgo.graph.check_poke_srcanddst(newlstpokemon2.pop())
                client.add_agent("{\"id\":" + str(src.id) + "}")
            else:
                client.add_agent("{\"id\":" + str(i) + "}")

        agents = json.loads(client.get_agents())
        self.assertEqual(len(myGame.agents), 0)
        myGame.add_agents(agents)
        self.assertNotEqual(len(myGame.agents), 0)
        agents = json.loads(client.get_agents())
        myGame.agents[0].id = 2
        self.assertEqual(myGame.agents[0].id, 2)
        myGame.update_agents(agents)
        self.assertNotEqual(myGame.agents[0].id, 2)


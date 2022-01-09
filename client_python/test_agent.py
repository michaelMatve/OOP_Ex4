from unittest import TestCase
from agent import Agent


class TestAgent(TestCase):
    def test_update(self):

        agentdict = {'id':1,'value':5.0, 'src':0, 'dest':1, 'speed':1.5, "pos":"35.18753053591606,32.10378225882353,0.0"}
        agent = Agent(agentdict)
        self.assertEqual(1, agent.id)
        self.assertEqual(5.0, agent.value)
        agentdict2 = {'id': 4, 'value': 2.0, 'src': 6, 'dest': 5, 'speed': 1.5,
                     "pos": "35.18753053591606,32.10378225882353,0.0"}
        agent.update(agentdict2)
        self.assertEqual(4,agent.id)
        self.assertEqual(2.0, agent.value)



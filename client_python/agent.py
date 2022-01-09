
class Agent:
    def __init__(self, agentdata: dict):
        self.id = agentdata['id']
        self.value = agentdata['value']
        self.src = agentdata['src']
        self.dest = agentdata['dest']
        self.speed = agentdata['speed']
        self.pos = tuple(float(s) for s in agentdata['pos'].strip("()").split(","))
        self.time = 0

    def update(self, agentdata: dict):
        self.id = agentdata['id']
        self.value = agentdata['value']
        self.src = agentdata['src']
        self.dest = agentdata['dest']
        self.speed = agentdata['speed']
        self.pos = tuple(float(s) for s in agentdata['pos'].strip("()").split(","))
        self.time = 0
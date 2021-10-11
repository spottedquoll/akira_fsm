from transitions import Machine

class Matter(object):

    def __init__(self): self.set_environment()

    def set_environment(self, temp=0, pressure=101.325):
        self.temp = temp
        self.pressure = pressure

    def heat(self, add_heat):
        self.temp = self.temp  + add_heat

lump = Matter()

# The states
states = ['solid', 'liquid', 'gas', 'plasma']

# And some transitions between states. We're lazy, so we'll leave out
# the inverse phase transitions (freezing, condensation, etc.).
transitions = [
    {'trigger': 'melt', 'source': 'solid', 'dest': 'liquid'},
    {'trigger': 'evaporate', 'source': 'liquid', 'dest': 'gas'},
    {'trigger': 'sublimate', 'source': 'solid', 'dest': 'gas'},
    {'trigger': 'ionize', 'source': 'gas', 'dest': 'plasma'},
    {'trigger': 'to_liquid', 'source': '*', 'dest': 'liquid'}
]

# Initialize
machine = Machine(lump, states=states, transitions=transitions, initial='solid')

lump.melt()
print(lump.state)

lump.evaporate()
print(lump.state)

lump.trigger('ionize')
print(lump.state)

print('Current temperature is ' + str(lump.temp) + ' degrees celsius')
lump.heat(5)
print('Current temperature is ' + str(lump.temp) + ' degrees celsius')
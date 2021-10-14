from transitions import Machine
import random
import pickle
from utils import random_walk_next_step
from strategies import strategy_ltma
from merchant_methods import m_states, m_transitions

# A fake ticker stream is created by modeling the stock price as a random walk
# Two machine instances. What are trading rounds called? Sessions? phase/loop
# Comptroller makes decisions about overall portfolio

# Initialise the random walk
ceiling = 1000
floor = 1
step_size = 5
initial_pos = random.randint(floor, ceiling)

# Initialise the ticker
buffer = 10
ticker = [initial_pos]

# Initialise the bank
available_funds = 1000


# Initialise the Merchant class
class Merchant(object):

    def __init__(self):
        self.stock_holding = 0

        # Initialize the state machine
        self.machine = Machine(model=self, states=m_states(), transitions=m_transitions(), initial='idle')


#  machine (each Merchant instance holds a single trading session?)
session = Merchant()
machine = Machine(session, states=m_states(), )

# Run simulation
for t in range(500):

    # Next step
    next_step = random_walk_next_step(ticker[-1], floor, ceiling, step_size)
    ticker.append(next_step)

    if t > buffer:

        decision = strategy_ltma(ticker, machine)

        print(str(next_step))


#
#
# # Can freeze/pickle trading instance
# # store the machine
# dump = pickle.dumps(m)
#
# # load the Machine instance again
# m2 = pickle.loads(dump)

print('Finished simulation')
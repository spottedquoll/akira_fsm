import random
import pickle
from utils import random_walk_next_step
from strategies import strategy_ltma
from merchant_methods import Merchant, log_state

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
available_funds = 10000

# Machine (each Merchant instance holds a single trading session?)
machine = Merchant()
machine.scan()  # Transition machine to discover state

# Run simulation
print('Starting simulation')

for t in range(1000):

    # Generate next step in stock price random walk
    current_price = random_walk_next_step(ticker[-1], floor, ceiling, step_size)
    ticker.append(current_price)

    if t > buffer:

        decision = strategy_ltma(ticker, machine)

        if decision is not None:
            available_funds = machine.execute_trade(decision, available_funds, current_price)

# Force sell at end of trading
if machine.state == 'hold':
    available_funds = machine.execute_trade('sell', available_funds, ticker[-1])

machine.pause()

print('Available funds: ' + str(available_funds))

#
#
# # Can freeze/pickle trading instance
# # store the machine
# dump = pickle.dumps(m)
#
# # load the Machine instance again
# m2 = pickle.loads(dump)

print('Finished simulation')
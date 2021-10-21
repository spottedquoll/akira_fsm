import random
import os
from utils import random_walk_next_step, write_pickle, read_pickle
from strategies import strategy_ltma
from merchant_methods import Merchant

# A fake ticker stream is created by modeling the stock price as a random walk
# Two machine instances. What are trading rounds called? Sessions? phase/loop
# Comptroller makes decisions about overall portfolio

# Path
current_path = os.path.dirname(os.path.realpath(__file__))
fsm_dir = current_path + '/fsm_objects/'
if not os.path.exists(fsm_dir):
    os.makedirs(fsm_dir)

# Initialise the random walk
ceiling = 1000
floor = 1
step_size = 5
initial_pos = random.randint(floor, ceiling)

# Initialise the ticker
buffer = 10
ticker = [initial_pos]

# Initialise the bank
initial_funds = 10000
available_funds = None

# Initialise simulation
n_steps = 10000  # timeseries (simulation) steps
n_seshos = 3  # concurrent trading blocks
n_eons = 3  # serial trading instances (serial in time)
eon_ids = []

# Create the FSM objects
for s in range(n_seshos):

    # Machine (each Merchant instance holds a single trading session?)
    machine = Merchant()
    machine.scan()  # Transition machine to discover state

    # Save machine object
    m_id = machine.id
    fname = fsm_dir + '/' + 'fsm_' + m_id + '.pickle'
    write_pickle(fname, machine)
    eon_ids.append(m_id)

# Running simulation
for e in range(n_eons):

    print('Starting Eon ' + str(e))

    for m_id in eon_ids:

        # Run simulation
        print('Simulating machine ' + m_id + ' with ' + str(n_steps) + ' steps')

        # Read fsm
        fname = fsm_dir + '/' + 'fsm_' + m_id + '.pickle'
        machine = read_pickle(fname)

        for t in range(n_steps):

            # Set bank balance
            if t == 0:
                available_funds = initial_funds

            # Generate next step in stock price random walk
            current_price = random_walk_next_step(ticker[-1], floor, ceiling, step_size)
            ticker.append(current_price)

            if t > buffer:

                decision = strategy_ltma(ticker, machine)

                if decision is not None:
                    available_funds = machine.execute_trade(decision, available_funds, current_price)

        # Log state
        if e < n_eons-1:
            machine.log_state()
        else:  # Force sell at end of trading

            if machine.state == 'hold':
                available_funds = machine.execute_trade('sell', available_funds, ticker[-1])

            machine.pause()
            print('Finished simulation')

            # Log result
            percent_return = (available_funds - initial_funds)/initial_funds * 100
            if available_funds > initial_funds:
                print('You made cash money! Baller! Available funds: ' + str(available_funds) + ', return: '
                      + '{:.2f}'.format(percent_return) + '%')
            elif available_funds < initial_funds:
                print('You lost money! Give up! Available funds: ' + str(available_funds) + ', return: '
                      + '{:.2f}'.format(percent_return) + '%')
            else:
                print('Available funds: ' + str(available_funds))

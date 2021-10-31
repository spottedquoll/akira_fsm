import random
import os
from utils import random_walk_next_step, write_pickle, read_pickle
from strategies import strategy_ltma
from merchant_methods import Merchant, calculate_return, log_state

# A fake ticker stream is created by modeling the stock price as a random walk
# Two machine instances. What are trading rounds called? Sessions? phase/loop
# Comptroller makes decisions about overall portfolio
# When stock is sold, all stock in sesho is sold

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
initial_funds = 20000
available_funds = 20000  # Set bank balance

# Initialise simulation
n_steps = 10000  # timeseries (simulation) steps
n_seshos = 3  # concurrent trading blocks
n_eons = 3  # serial trading instances (serial in time)
eon_ids = []

print('Starting account balance: $' + str(initial_funds) + ', simulation steps per Eon: ' + str(n_steps))

# Create the FSM objects
for s in range(n_seshos):

    # Machine (each Merchant instance holds a single trading session?)
    machine = Merchant()
    machine.scan()  # Transition machine to discover state

    # Initialise price increase floor setting
    machine.sell_rel_increase = random.randrange(10, 15) / 10.0

    # Initialise neighborhood size for long term average
    machine.lta_neighborhood = random.randint(3, buffer-1)  # cannot be larger than the buffer

    # Save machine object
    m_id = machine.id
    fname = fsm_dir + '/' + 'fsm_' + m_id + '.pickle'
    write_pickle(fname, machine)
    eon_ids.append(m_id)

# Running simulation
for e in range(n_eons):

    print('Starting Eon ' + str(e))

    # Create timeseries (each step in stock price random walk)
    ticker_segment = [ticker[-1]]  # initialise with last item in previous ticker
    for t in range(n_steps):
        current_price = random_walk_next_step(ticker_segment[-1], floor, ceiling, step_size)
        ticker_segment.append(current_price)

    for m_id in eon_ids:

        print('Simulating machine ' + m_id)

        # Read fsm
        fname = fsm_dir + '/' + 'fsm_' + m_id + '.pickle'
        machine = read_pickle(fname)

        # Replay timeseries
        for t in range(n_steps):
            if t > buffer:
                decision = strategy_ltma(ticker_segment[:t], machine, neighborhood=machine.lta_neighborhood
                                         , sell_rel_increase=machine.sell_rel_increase)
                if decision is not None:
                    current_price = ticker_segment[t-1]
                    available_funds = machine.execute_trade(decision, available_funds, current_price)

        log_state(machine)  # Log machine state
        print('Balance: ' + str( available_funds))
        write_pickle(fname, machine) # Save updated machine

    ticker.extend(ticker_segment)
    print('.')

print('Finished simulation')

for m_id in eon_ids:

    print('Calculating return for machine ' + m_id)

    # Read fsm
    fname = fsm_dir + '/' + 'fsm_' + m_id + '.pickle'
    machine = read_pickle(fname)

    # Force sell for all seshos at last eon
    final_price = ticker[-1]
    if machine.state == 'hold':

        available_funds = machine.execute_trade('sell', available_funds, final_price)

    # Log result
    #print(str(machine.stock_holding_past) + ',' + str(machine.buy_price) + ',' + str(machine.sell_price))
    absolute_return, relative_return = calculate_return(machine.stock_holding_past,
                                                        machine.buy_price, machine.sell_price)
    percent_return = relative_return * 100

    print('Absolute return: $' + str(absolute_return) + ', relative return: '
          + '{:.2f}'.format(percent_return) + '%')

# Log final balance
print('Final account balance: $' + str(available_funds))
if available_funds > initial_funds:
    print('You made $' + str(available_funds - initial_funds) + '! Baller!')
elif available_funds < initial_funds:
    print('You lost $' + str(available_funds - initial_funds) + '! Give up!')
else:
    stop=1


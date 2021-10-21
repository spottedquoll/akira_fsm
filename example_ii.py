from transitions import Machine
import random


# Define states
states = ['idle', 'discover', 'buy', 'hold', 'sell']

# Define transitions
transitions = [
                {'trigger': 'scan', 'source': 'idle', 'dest': 'discover'},  # start discovery
                {'trigger': 'buy', 'source': 'discover', 'dest': 'hold'},  # after buying go to hold
                {'trigger': 'sell', 'source': 'hold', 'dest': 'discover'},
                {'trigger': 'buy', 'source': 'hold', 'dest': 'hold'},  # buy more from hold
                {'trigger': 'pause', 'source': '*', 'dest': 'idle'},
                ]


# Each Merchant instance holds a single trade instance?
class Merchant(object):

    def __init__(self):
        self.available_funds = 10
        self.stock_holding = 0

    # Attempt to execute trade, small chance this will fail
    def execute_trade(self, action):
        if random.random() > 0.1:
            if action == 'buy':
                self.available_funds -= 1
                self.stock_holding += 1
            elif action == 'sell':
                self.available_funds += 1
                self.stock_holding -= 1
            else:
                raise ValueError('Unknown action')
            return 'success'
        else:
            return 'fail'

    def log_state(self):
        print('state: ' + self.state + ', funds: ' + str(self.available_funds) + ', stock: '
              + str(self.stock_holding))


# Strategy logic
def strategy_buy(available_funds):
    if available_funds > 0 and random.random() > 0.5:
        return True
    else:
        return False


# Strategy logic
def strategy_sell(stock_holding):
    if stock_holding > 0 and random.random() > 0.5:
        return True
    else:
        return False


# Initialize
session = Merchant()
machine = Machine(session, states=states, transitions=transitions, initial='idle')

# Start
session.scan()  # scan for opportunities
print(session.state)

for x in range(20):

    if strategy_buy(session.available_funds) and session.execute_trade('buy') == 'success':
        session.buy()

    if session.state == 'hold' and strategy_sell(session.stock_holding) and session.execute_trade('sell') == 'success':
        session.sell()

    session.log_state()

print('Finished simulation')
session.log_state()
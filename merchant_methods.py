from math import floor
from transitions import Machine
from uuid import uuid4


def log_state(machine):
    print('state: ' + machine.state + ', stock: ' + str(machine.stock_holding))


# Define states
def m_states():
    return ['idle', 'discover', 'buy', 'hold', 'sell']


# Define transitions
def m_transitions():

    return [{'trigger': 'scan', 'source': 'idle', 'dest': 'discover'},  # start discovery
            {'trigger': 'buy', 'source': 'discover', 'dest': 'hold'},  # after buying go to hold
            {'trigger': 'sell', 'source': 'hold', 'dest': 'discover'},
            {'trigger': 'buy', 'source': 'hold', 'dest': 'hold'},  # buy more from hold
            {'trigger': 'pause', 'source': '*', 'dest': 'idle'},
            ]


# Each Merchant instance holds a single trade instance? Not sure which methods should be attached to this class object
class Merchant(object):

    def __init__(self):
        self.stock_holding = 0
        self.id = str(uuid4())
        self.buy_price = None
        self.sell_price = None

        # Initialize the state machine
        self.machine = Machine(model=self, states=m_states(), transitions=m_transitions(), initial='idle')

    # Execute the trade
    def execute_trade(self, action, available_funds, current_price):

        if action == 'buy':
            units_to_buy = comptroller(current_price, available_funds)
            if units_to_buy > 0:
                available_funds = available_funds - units_to_buy * current_price
                self.stock_holding += units_to_buy
                self.buy()
                self.buy_price = current_price
        elif action == 'sell':
            available_funds = available_funds + self.stock_holding * current_price
            self.stock_holding = 0
            self.sell()
        else:
            raise ValueError('Unknown action')

        return available_funds


def comptroller(current_price, available_funds, max_individual_holding=0.3):
    """
    This method determines how much of each stock to buy
    Can be expanded to include more risk parameters
    """

    max_affordable_units = floor(max_individual_holding*available_funds/current_price)

    return max_affordable_units


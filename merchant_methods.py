from math import floor

import numpy as np
from transitions import Machine
from uuid import uuid4


def log_state(machine):
    print('state: ' + machine.state + ', stock: ' + str(machine.stock_holding) + ' units')


# Define states
def m_states():
    return ['idle', 'discover', 'buy', 'hold', 'sell']


# Define transitions
def m_transitions():

    return [{'trigger': 'scan', 'source': 'idle', 'dest': 'discover'},  # start discovery
            {'trigger': 'buy', 'source': 'discover', 'dest': 'hold'},  # after buying go to hold
            {'trigger': 'sell', 'source': 'hold', 'dest': 'idle'}  # trading is finished after a sell
            ]


# Each Merchant instance holds a single trade instance? Not sure which methods should be attached to this class object
class Merchant(object):

    def __init__(self):

        self.stock_holding = 0  # Current stock holding (count of units)
        self.stock_holding_past = 0  # Previous stock holding, before any sales (count of units)
        self.id = str(uuid4())  #
        self.buy_price = None
        self.sell_price = None

        # Initialize the state machine
        self.machine = Machine(model=self, states=m_states(), transitions=m_transitions(), initial='idle')

    # Execute the trade
    def execute_trade(self, action, available_funds, current_price):
        """
            This method should receive some confirmation from the platform that trade was successful
        """

        if action == 'buy':
            units_to_buy = comptroller(current_price, available_funds)
            if units_to_buy > 0:
                available_funds = available_funds - units_to_buy * current_price
                self.stock_holding += units_to_buy
                self.buy_price = current_price
                self.buy()
        elif action == 'sell':
            if self.stock_holding > 0:
                available_funds = available_funds + self.stock_holding * current_price
                self.stock_holding_past = self.stock_holding
                self.stock_holding = 0
                self.sell_price = current_price
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


def calculate_return(units, buy_price, sell_price):

    assert units > 0

    value_at_purchase = units*buy_price
    value_at_sale = units*sell_price

    absolute_return = value_at_sale - value_at_purchase
    relative_return = absolute_return/value_at_purchase

    assert np.isfinite(absolute_return) and np.isfinite(relative_return)

    return absolute_return, relative_return

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

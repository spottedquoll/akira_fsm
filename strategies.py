import numpy as np


def strategy_ltma(ticker, machine, neighborhood=5):
    """
        Strategy long term moving average
    """

    lt_mean = np.mean(ticker)
    nbr_mean = np.mean(ticker[-1*neighborhood])

    if machine.state() == 'discover' and nbr_mean < lt_mean:
        return 'buy'
    elif machine.state() == 'hold' and nbr_mean > lt_mean:
        return 'sell'
    else:
        return 'None'


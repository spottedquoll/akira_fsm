import numpy as np


def strategy_ltma(ticker, machine, neighborhood=None, sell_rel_increase=None):
    """
        Strategy long term moving average
        neighborhood: local neighborhood of prices to consider
        sell_rel_increase: sell when current price is >= buy_price*price_increase
    """

    # Initialise settings
    if neighborhood is None:
        neighborhood = 5
    if sell_rel_increase is None:
        sell_rel_increase = 1.2

    if machine.state == 'discover':

        lt_mean = np.mean(ticker)
        nbr_mean = np.mean(ticker[-1 * neighborhood])

        if nbr_mean < lt_mean:
            return 'buy'
        else:
            return None

    elif machine.state == 'hold' and ticker[-1] >= machine.buy_price*sell_rel_increase:
        return 'sell'
    else:
        return None


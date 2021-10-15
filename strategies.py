import numpy as np


def strategy_ltma(ticker, machine, neighborhood=5, price_increase=1.2):
    """
        Strategy long term moving average
        neighborhood: local neighborhood of prices to consider
        price_increase: sell when current price is >= buy_price*price_increase
    """

    if machine.state == 'discover':

        lt_mean = np.mean(ticker)
        nbr_mean = np.mean(ticker[-1 * neighborhood])

        if nbr_mean < lt_mean:
            return 'buy'
        else:
            return None

    elif machine.state == 'hold' and ticker[-1] >= machine.buy_price*price_increase:
        return 'sell'
    else:
        return None


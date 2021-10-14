import random


def random_walk_next_step(previous, floor, ceiling, step_size):

    r = random.randint(-1*step_size, step_size)
    next_position = previous + r

    next_position = min(next_position, ceiling)
    next_position = max(floor, next_position)

    return next_position

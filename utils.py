import random
import pickle


def random_walk_next_step(previous, floor, ceiling, step_size):

    r = random.randint(-1*step_size, step_size)
    next_position = previous + r

    next_position = min(next_position, ceiling)
    next_position = max(floor, next_position)

    return next_position


def write_pickle(fname, obj_to_write):

    with open(fname, 'wb') as f:
        pickle.dump(obj_to_write, f)



def read_pickle(fname):

    with open(fname, 'rb') as pickle_file:
        result = pickle.load(pickle_file)

    return result

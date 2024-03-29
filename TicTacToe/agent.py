import numpy as np
from environment import Environment


class Agent():
    def __init__(self, eps=0.1, alpha=0.5):
        self.eps = eps  # probability of choosing random action instead of greedy
        self.alpha = alpha  # learning rate
        self.verbose = False  # talks to console
        self.state_history = []

    def setV(self, V):
        self.V = V

    def set_symbol(self, sym):
        self.sym = sym

    def set_verbose(self, verbose):
        self.verbose = verbose

    def reset_state_history(self):
        self.state_history = []

    def update_state_history(self, s):
        self.state_history.append(s)

    def take_action(self, env):
        p = np.random.rand()
        pos2value = {}  # debugging
        if p < self.eps:
            if self.verbose:
                print("Taking a random action")

            # Get all empty spots
            possible_actions = []

            for y in range(len(env.tiles)):
                for x in range(len(env.tiles[0])):
                    if env.is_empty(x, y):
                        possible_actions.append((x, y))

            idx = np.random.choice(len(possible_actions))
            next_move = possible_actions[idx]

        else:
            next_move = None
            best_value = -1

            # loop through all tiles on the board
            for y in range(env.size):
                for x in range(env.size):
                    # if the tile is empty,
                    if env.is_empty(x, y):
                        # if so check this action's value
                        env.tiles[y, x] = self.sym
                        state = env.get_state()
                        # don't forget to set back to empty
                        env.tiles[y, x] = 0
                        pos2value[(x, y)] = self.V[state]
                        # set the max value if this value is greater than the previous max
                        if self.V[state] > best_value:
                            best_value = self.V[state]
                            next_move = (x, y)

        if self.verbose and p >= self.eps:
            print("Taking a greedy action")
            for y in range(env.size):
                temp = ""

                for x in range(env.size):
                    if env.is_empty(x, y):
                        temp += str(round(pos2value[(x, y)], 2)) + " "
                    else:
                        if env.tiles[y, x] == env.x:
                            temp += "X   "
                        elif env.tiles[y, x] == env.o:
                            temp += "O   "
                        else:
                            temp += "    "

                print(temp)

        env.tiles[next_move[1], next_move[0]] = self.sym

    def update(self, env):
        # Will be done at the end of the episode
        # Modify the steps taken to have a lower / higher value depending on the reward
        # (weather or not this agent won the game, lost, or tied).
        # this function re-evaluates the values for each game configuration hash
        # based on the reward value.
        reward = env.reward(self.sym)
        target = reward
        for prev in reversed(self.state_history):
            value = self.V[prev] + self.alpha*(target - self.V[prev])
            self.V[prev] = value
            target = value
        self.reset_state_history()

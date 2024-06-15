# qlearning.py

import numpy as np
import random

class QLearningAgent:
    def __init__(self, actions, state_space, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.actions = actions
        self.state_space = state_space
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.q_table = np.zeros(state_space + (len(actions),))

    def choose_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.actions)
        else:
            return self.actions[np.argmax(self.q_table[state])]

    def update_q_value(self, state, action, reward, next_state):
        current_q_value = self.q_table[state + (self.actions.index(action),)]
        max_future_q_value = np.max(self.q_table[next_state])
        new_q_value = current_q_value + self.alpha * (reward + self.gamma * max_future_q_value - current_q_value)
        self.q_table[state + (self.actions.index(action),)] = new_q_value

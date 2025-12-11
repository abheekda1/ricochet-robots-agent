from agent.agent import Agent
import math
import random

import time

UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3

class MCTSAgent(Agent):
    def __init__(self, model, time=1, rollout_depth=15):
        super().__init__(model)
        self.time = time
        self.rollout_depth = rollout_depth

    def choose_action(self, state):
        root = Node(state, self.model, self.rollout_depth)
        end_time = time.time() + self.time
        while time.time() < end_time:
            leaf = root.traverse()
            node = leaf.expand() or leaf
            reward = node.simulate()
            node.update(reward)
        if not root.children:
            return None
        return max(root.children.items(), key=lambda kv: kv[1].r / kv[1].n)[0]

class Node:
    def __init__(self, state, model, rollout_depth, parent=None):
        self.parent = parent
        self.children = {}
        self.s = state
        self.model = model
        self.rollout_depth = rollout_depth
        self.r = 0.0
        self.n = 0

    def add_child(self, action, child_state):
        child = Node(child_state, self.model, self.rollout_depth, parent=self)
        self.children[action] = child
        return child

    def _ucb(self):
        if self.n == 0 or self.parent is None:
            return float('inf')
        exploit = self.r / self.n
        explore = math.sqrt(2 * math.log(self.parent.n) / self.n)
        return exploit + explore

    def traverse(self):
        node = self
        while node.children:
            unvisited = [c for c in node.children.values() if c.n == 0]
            if unvisited:
                return random.choice(unvisited)
            node = max(node.children.values(), key=lambda c: c._ucb())
        return node

    def expand(self):
        if self.model.is_terminal(self.s) or self.n == 0 or self.children:
            return None
        for next_state, action in self.model.successors(self.s):
            self.add_child(action, next_state)
        return random.choice(tuple(self.children.values()))

    def simulate(self):
        state = self.s
        depth = 0
        while not self.model.is_terminal(state) and depth < self.rollout_depth:
            successors = list(self.model.successors(state))
            if not successors:
                break
            state, action = random.choice(successors)
            depth += 1

        if self.model.is_terminal(state):
            return 1.0
        else:
            return 0.0

    def update(self, reward):
        node = self
        while node:
            node.n += 1
            node.r += reward
            node = node.parent

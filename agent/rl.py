from agent.agent import Agent
from collections import defaultdict

class ValueIterationAgent(Agent):
    def __init__(self, model, num_robots, discount=0.9, num_iterations=100):
        super().__init__(model)
        self.num_robots = num_robots
        self.discount = discount
        self.num_iterations = num_iterations
        self.values = defaultdict(float)
        self.planned = False

    def run_value_iteration(self):
        for i in range(self.num_iterations):
            # print(i)
            next_iter = defaultdict(float)
            all_states = self.model.get_states(self.num_robots)

            for state in all_states:
                best_val = -float('inf')
                for next_state, action in self.model.successors(state):
                    q_val = self.model.is_terminal(state) + self.discount * self.values[next_state]
                    best_val = max(best_val, q_val)

                next_iter[state] = 0.0 if best_val == -float('inf') else best_val

            for state in all_states:
                self.values[state] = next_iter[state]

        self.planned = True

    def choose_action(self, state):
        if self.model.is_terminal(state):
            return None

        if not self.planned:
            self.run_value_iteration()

        best_action = None
        best_val = -float('inf')
        for next_state, action in self.model.successors(state):
            if self.values[next_state] > best_val:
                best_val = self.values[next_state]
                best_action = action

        return best_action

from agent.agent import Agent
import util

class ValueIterationAgent(Agent):
    
    def __init__(self, model, discount = 0.9, num_iterations = 1000):
        super().__init__(model)
        self.discount = discount
        self.num_iterations = num_iterations
        self.values = util.Counter()
        self.run_value_iteration()

    def run_value_iteration(self):
        for i in range(self.num_iterations):
            next_iter = {}
            all_states =  self.model.get_states()
            for state in all_states:
                all_states_and_actions = [(next_state, action) for next_state, action in self.model.successors(state)]
                best_val = -float('inf')
                for next_state, action in all_states_and_actions:
                    q_val = self.model.is_terminal(state) + self.discount * self.values[next_state]
                    best_val = max(best_val, q_val)
                if best_val == -float('inf'):
                    next_iter[state] = 0.0
                else:
                    next_iter[state] = best_val
            for state in all_states:
                self.values[state] = next_iter[state]
                
    def choose_action(self, state):
        if self.model.is_terminal(state):
            return None
        best_action = None
        best_val = -float('inf')
        for next_state, action in self.model.successors(state):
            if self.values[next_state] > best_val:
                best_val = self.values[next_state]
                best_action = action
        return best_action
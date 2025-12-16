from agent.agent import Agent
from collections import deque

class BFSAgent(Agent):
    def __init__(self, model, max_nodes=100_000):
        super().__init__(model)
        self.max_nodes = max_nodes
        self.plan = None
        self.plan_index = 0
        self.last_start_state = None

    def choose_action(self, state):
        # If no plan exists or state changed unexpectedly, replan
        if self.plan is None or state != self.last_start_state:
            self.plan = self._bfs_plan(state)
            self.plan_index = 0
            self.last_start_state = state

        if self.plan is None or self.plan_index >= len(self.plan):
            return None

        action = self.plan[self.plan_index]
        self.plan_index += 1
        return action

    def _bfs_plan(self, start_state):
        queue = deque()
        queue.append((start_state, []))
        visited = {start_state}
        nodes_expanded = 0

        while queue:
            state, path = queue.popleft()
            nodes_expanded += 1

            if nodes_expanded > self.max_nodes:
                return None

            if self.model.is_terminal(state):
                return path

            for next_state, action in self.model.successors(state):
                if next_state not in visited:
                    visited.add(next_state)
                    queue.append((next_state, path + [action]))

        return None

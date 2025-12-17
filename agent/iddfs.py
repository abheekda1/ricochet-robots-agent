from agent.agent import Agent

class IDDFSAgent(Agent):
    
    def __init__(self, model, max_depth=30, max_nodes=100_000):
        super().__init__(model)
        self.max_depth = max_depth
        self.max_nodes = max_nodes
        self.plan = None
        self.plan_index = 0
        self.last_start_state = None
    
    def choose_action(self, state):
        if self.plan is None or state != self.last_start_state:
            self.plan = self._iddfs_plan(state)
            self.plan_index = 0
            self.last_start_state = state
        
        if self.plan is None or self.plan_index >= len(self.plan):
            return None
        
        action = self.plan[self.plan_index]
        self.plan_index += 1
        return action
    
    def _iddfs_plan(self, start_state):
        for depth_limit in range(1, self.max_depth + 1):
            result = self._depth_limited_search(start_state, depth_limit)
            if result is not None:
                return result
        return None
    
    def _depth_limited_search(self, start_state, depth_limit):
        stack = [(start_state, [], 0)]
        visited = set()
        nodes_expanded = 0
        
        while stack:
            current_state, path, depth = stack.pop()
            nodes_expanded += 1
            
            if nodes_expanded > self.max_nodes:
                return None
            
            if self.model.is_terminal(current_state):
                return path
            
            if depth >= depth_limit:
                continue
            
            state_depth_key = (current_state, depth)
            if state_depth_key in visited:
                continue
            visited.add(state_depth_key)
            
            for next_state, action in self.model.successors(current_state):
                new_path = path + [action]
                stack.append((next_state, new_path, depth + 1))
        
        return None

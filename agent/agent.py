class Agent:
    def __init__(self, model):
        """
        model: instance of RRModel
        All agents receive the same model interface:
            - model.successors(state)
            - model.transition(state, action)
            - model.is_terminal(state)
        """
        self.model = model

    # --------------------------------------------------------
    # Required: each agent must implement choose_action()
    # --------------------------------------------------------
    def choose_action(self, state):
        """
        Given a state, return an action that should be taken next.

        Agents MUST override this.
        Valid actions are typically: UP, RIGHT, DOWN, LEFT,
        or (robot_index, direction) if multiple robots.

        Returns:
            action  (int or tuple)
        """
        raise NotImplementedError("choose_action() must be implemented by subclasses.")

    # --------------------------------------------------------
    # Optional: compute an entire plan
    # --------------------------------------------------------
    def plan(self, start_state, max_steps=200):
        """
        Optionally compute a full sequence of actions from start_state
        until terminal or max_steps is reached.

        Default implementation:
        repeatedly call choose_action().
        Agents may override for efficiency (e.g., A*).

        Returns:
            actions: list of actions
        """
        actions = []
        state = start_state

        for _ in range(max_steps):
            if self.model.is_terminal(state):
                break

            action = self.choose_action(state)
            actions.append(action)
            state = self.model.transition(state, action)

        return actions
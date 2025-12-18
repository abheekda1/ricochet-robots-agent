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

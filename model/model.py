UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3
DIRS = {
    UP:    (-1, 0),
    RIGHT: (0, 1),
    DOWN:  (1, 0),
    LEFT:  (0, -1)
}

W_UP, W_RIGHT, W_DOWN, W_LEFT = 1, 2, 4, 8


class RRModel:
    def __init__(self, rows, cols, walls, goal_pos):
        """
        rows, cols : board dimensions
        walls      : 2D array [rows][cols] of wall bitmasks
        goal_pos   : (goal_r, goal_c)
        """
        self.rows = rows
        self.cols = cols
        self.walls = walls
        self.goal = goal_pos

    def is_terminal(self, state):
        """Return True if robot has reached the goal."""
        return state[0] == self.goal

    def slide(self, r, c, direction, other_robots=None):
        """
        Slide from (r,c) in the given direction until blocked by:
        - walls
        - board edges
        - another robot (if provided)
        Returns (new_r, new_c)
        """
        dr, dc = DIRS[direction]

        while True:
            nr, nc = r + dr, c + dc

            if nr < 0 or nr >= self.rows or nc < 0 or nc >= self.cols:
                break

            if direction == UP    and (self.walls[r][c] & W_UP): break
            if direction == RIGHT and (self.walls[r][c] & W_RIGHT): break
            if direction == DOWN  and (self.walls[r][c] & W_DOWN): break
            if direction == LEFT  and (self.walls[r][c] & W_LEFT): break

            if direction == DOWN  and (self.walls[nr][nc] & W_UP): break
            if direction == UP    and (self.walls[nr][nc] & W_DOWN): break
            if direction == RIGHT and (self.walls[nr][nc] & W_LEFT): break
            if direction == LEFT  and (self.walls[nr][nc] & W_RIGHT): break

            if other_robots and (nr, nc) in other_robots:
                break

            r, c = nr, nc

        return (r, c)

    def transition(self, state, action):
        """
        Apply action (slide in a direction) to state.
        state = (r,c) for single robot
        """
        # r, c = state
        # return self.slide(r, c, direction, other_robots)
        robot_idx, direction = action

        robots = list(state)
        r, c = robots[robot_idx]

        # other robots block movement
        other_robots = set(robots)
        other_robots.remove((r, c))

        new_pos = self.slide(r, c, direction, other_robots)

        # update only the chosen robot
        robots[robot_idx] = new_pos
        return tuple(robots)

    def successors(self, state):
        """
        Yield (next_state, action) for moves that actually change the state.
        """
        # r, c = state

        # for direction in (UP, RIGHT, DOWN, LEFT):
        #     next_state = self.transition((r, c), direction)

        #     if next_state != (r, c):
        #         yield next_state, direction
        num_robots = len(state)

        for i in range(num_robots):
            r, c = state[i]

            other_robots = set(state)
            other_robots.remove((r, c))

            for direction in (UP, RIGHT, DOWN, LEFT):
                new_pos = self.slide(r, c, direction, other_robots)

                if new_pos != (r, c):
                    new_state = list(state)
                    new_state[i] = new_pos
                    yield tuple(new_state), (i, direction)

    def render(self, state):
        """
        Return a Unicode string representation of the board.
        """
        # Map robot positions to indices
        robot_at = {pos: i for i, pos in enumerate(state)}

        out = []

        for r in range(self.rows):
            # ---- Top wall line ----
            top = ""
            for c in range(self.cols):
                top += "┼"
                top += "━━━" if (self.walls[r][c] & W_UP) else "   "
            top += "┼"
            out.append(top)

            # ---- Cell contents + vertical walls ----
            mid = ""
            for c in range(self.cols):
                mid += "┃" if (self.walls[r][c] & W_LEFT) else " "

                pos = (r, c)
                if pos in robot_at:
                    if robot_at[pos] == 0:
                        mid += " R "   # target robot
                    else:
                        mid += " B "   # blocker robot
                elif pos == self.goal:
                    mid += " G "
                else:
                    mid += " · "

            mid += "┃" if (self.walls[r][self.cols - 1] & W_RIGHT) else " "
            out.append(mid)

        # ---- Bottom wall line ----
        bottom = ""
        for c in range(self.cols):
            bottom += "┼"
            bottom += "━━━" if (self.walls[self.rows - 1][c] & W_DOWN) else "   "
        bottom += "┼"
        out.append(bottom)

        return "\n".join(out)


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
        return state == self.goal

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

    def transition(self, state, direction, other_robots=None):
        """
        Apply action (slide in a direction) to state.
        state = (r,c) for single robot
        """
        r, c = state
        return self.slide(r, c, direction, other_robots)

    def successors(self, state):
        """
        Yield (next_state, action) for moves that actually change the state.
        """
        r, c = state

        for direction in (UP, RIGHT, DOWN, LEFT):
            next_state = self.transition((r, c), direction)

            if next_state != (r, c):
                yield next_state, direction

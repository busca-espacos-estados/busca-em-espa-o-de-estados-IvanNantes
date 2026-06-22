import heapq
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        distance = 0

        for i, tile in enumerate(state.tiles):
            if tile == 0:
                continue

            current_row, current_col = i // 3, i % 3
            goal_row, goal_col = (tile - 1) // 3, (tile - 1) % 3

            distance += abs(current_row - goal_row) + abs(current_col - goal_col)

        return distance

    def search(self, initial: State) -> SearchResult:
        if initial.is_goal:
            return SearchResult(
                solution=initial,
                nodes_expanded=0,
                nodes_generated=1,
                max_frontier_size=1,
                depth=0
            )

        counter = 0

        frontier = []
        heapq.heappush(
            frontier,
            (self.heuristic(initial), 0, counter, initial)
        )

        g_score = {initial.tiles: 0}
        explored = set()

        nodes_generated = 1
        nodes_expanded = 0
        max_frontier_size = 1

        while frontier:
            max_frontier_size = max(max_frontier_size, len(frontier))

            f, g, _, current = heapq.heappop(frontier)

            if current.tiles in explored:
                continue

            explored.add(current.tiles)
            nodes_expanded += 1

            if current.is_goal:
                return SearchResult(
                    solution=current,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=len(current.path()) - 1
                )

            for neighbor in current.neighbors():
                g_new = g + 1

                if (
                    neighbor.tiles not in g_score
                    or g_new < g_score[neighbor.tiles]
                ):
                    g_score[neighbor.tiles] = g_new

                    h = self.heuristic(neighbor)
                    f_new = g_new + h

                    counter += 1

                    heapq.heappush(
                        frontier,
                        (f_new, g_new, counter, neighbor)
                    )

                    nodes_generated += 1

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
            depth=-1
        )
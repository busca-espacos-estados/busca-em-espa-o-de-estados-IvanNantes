import heapq
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        """Distância Manhattan - soma das distâncias de cada peça até sua posição objetivo."""
        distance = 0
        for i, tile in enumerate(state.tiles):
            if tile == 0:  # não contamos o espaço vazio
                continue
            # Posição atual
            current_row, current_col = i // 3, i % 3
            # Posição objetivo (tile-1 porque os valores são 1-8)
            goal_row, goal_col = (tile - 1) // 3, (tile - 1) % 3
            distance += abs(current_row - goal_row) + abs(current_col - goal_col)
        return distance

    def search(self, initial: State) -> SearchResult:
        if initial.is_goal:
            return SearchResult(solution=initial, nodes_expanded=0, nodes_generated=0, depth=0)

        # Priority queue: (f = g + h, g, estado)
        f_initial = self.heuristic(initial)
        frontier = [(f_initial, 0, initial)]
        explored = set()

        nodes_generated = 1
        nodes_expanded = 0
        max_frontier_size = 1

        while frontier:
            max_frontier_size = max(max_frontier_size, len(frontier))
            f, g, current = heapq.heappop(frontier)

            if current.tiles in explored:
                continue
            explored.add(current.tiles)

            nodes_expanded += 1

            if current.is_goal:
                depth = len(current.path())
                return SearchResult(
                    solution=current,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=depth
                )

            for neighbor in current.neighbors():
                if neighbor.tiles not in explored:
                    g_new = g + 1
                    h = self.heuristic(neighbor)
                    f_new = g_new + h
                    heapq.heappush(frontier, (f_new, g_new, neighbor))
                    nodes_generated += 1

        return SearchResult(solution=None, nodes_expanded=nodes_expanded, nodes_generated=nodes_generated)

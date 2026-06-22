from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class BFS(BaseSearch):

    def search(self, initial: State) -> SearchResult:
        if initial.is_goal:
            return SearchResult(solution=initial, nodes_expanded=0, nodes_generated=0, depth=0)

        frontier = deque([initial])
        explored = set()

        nodes_generated = 1
        nodes_expanded = 0
        max_frontier_size = 1

        while frontier:
            max_frontier_size = max(max_frontier_size, len(frontier))
            current = frontier.popleft()

            if current.tiles in explored:
                continue
            explored.add(current.tiles)

            nodes_expanded += 1

            for neighbor in current.neighbors():
                if neighbor.tiles not in explored:
                    if neighbor.is_goal:
                        depth = len(neighbor.path())
                        return SearchResult(
                            solution=neighbor,
                            nodes_expanded=nodes_expanded,
                            nodes_generated=nodes_generated + len(current.neighbors()),
                            max_frontier_size=max_frontier_size,
                            depth=depth
                        )
                    frontier.append(neighbor)
                    nodes_generated += 1

        return SearchResult(solution=None, nodes_expanded=nodes_expanded, nodes_generated=nodes_generated)

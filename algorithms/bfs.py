from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class BFS(BaseSearch):

    def search(self, initial: State) -> SearchResult:
        if initial.is_goal:
            return SearchResult(
                solution=initial,
                nodes_expanded=0,
                nodes_generated=1,
                max_frontier_size=1,
                depth=0
            )

        frontier = deque([initial])
        frontier_set = {initial.tiles}
        explored = set()

        nodes_generated = 1
        nodes_expanded = 0
        max_frontier_size = 1

        while frontier:
            max_frontier_size = max(max_frontier_size, len(frontier))

            current = frontier.popleft()
            frontier_set.remove(current.tiles)

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
                if (
                    neighbor.tiles not in explored
                    and neighbor.tiles not in frontier_set
                ):
                    frontier.append(neighbor)
                    frontier_set.add(neighbor.tiles)
                    nodes_generated += 1

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
            depth=-1
        )
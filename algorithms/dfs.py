from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        if initial.is_goal:
            return SearchResult(
                solution=initial,
                nodes_expanded=0,
                nodes_generated=1,
                max_frontier_size=1,
                depth=0
            )

        stack = [initial]
        stack_set = {initial.tiles}
        explored = set()

        nodes_generated = 1
        nodes_expanded = 0
        max_frontier_size = 1

        while stack:
            max_frontier_size = max(max_frontier_size, len(stack))

            current = stack.pop()
            stack_set.remove(current.tiles)

            explored.add(current.tiles)
            nodes_expanded += 1

            current_depth = len(current.path()) - 1

            if current.is_goal:
                return SearchResult(
                    solution=current,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=current_depth
                )

            if current_depth >= self.depth_limit:
                continue

            neighbors = current.neighbors()[::-1]

            for neighbor in neighbors:
                if (
                    neighbor.tiles not in explored
                    and neighbor.tiles not in stack_set
                ):
                    stack.append(neighbor)
                    stack_set.add(neighbor.tiles)
                    nodes_generated += 1

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
            depth=-1
        )
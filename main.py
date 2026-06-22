from puzzle.state import State
from algorithms.bfs import BFS
from algorithms.dfs import DFS
from algorithms.a_star import AStar


def print_result(name: str, result):
    print(f"\n{'='*40}")
    print(f"Algoritmo : {name}")
    if result.found:
        actions_str = ' -> '.join(result.actions)
        print(f"Solucao   : {actions_str}")
        print(f"Custo     : {result.path_cost}")
        print(f"Profund.  : {result.depth}")
        print("\nEstado final:")
        print(result.solution)
    else:
        print("Solucao   : NAO ENCONTRADA (estado impossível)")
    print(f"Expandidos: {result.nodes_expanded}")
    print(f"Gerados   : {result.nodes_generated}")
    print(f"Fronteira : {result.max_frontier_size} (max)")


if __name__ == "__main__":
    initial = State((2, 8, 3, 1, 6, 4, 7, 0, 5))
    print("Estado inicial:")
    print(initial)

    print_result("BFS",  BFS().search(initial))
    print_result("DFS",  DFS().search(initial))
    print_result("A*",   AStar().search(initial))

from __future__ import annotations
from typing import List, Optional, Tuple


GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)


class State:
    """Representa um estado do 8-puzzle como tupla imutável de 9 inteiros (0 = espaço vazio)."""

    def __init__(self, tiles: Tuple[int, ...], parent: Optional["State"] = None, action: Optional[str] = None, cost: int = 0):
        if len(tiles) != 9 or set(tiles) != set(range(9)):
            raise ValueError("Estado inválido: deve conter exatamente os valores 0-8.")
        self.tiles = tiles
        self.parent = parent
        self.action = action
        self.cost = cost

    @property
    def is_goal(self) -> bool:
        return self.tiles == GOAL_STATE

    @property
    def blank_index(self) -> int:
        return self.tiles.index(0)

    def neighbors(self) -> List["State"]:
        """Retorna os estados filhos válidos a partir deste estado."""
        blank = self.blank_index
        neighbors = []

        row, col = blank // 3, blank % 3

        # Cima (não pode se estar na linha 0)
        if row > 0:
            new_idx = blank - 3
            moved_number = self.tiles[new_idx]
            new_tiles = list(self.tiles)
            new_tiles[blank], new_tiles[new_idx] = new_tiles[new_idx], new_tiles[blank]
            action = f"{moved_number}: CIMA"
            neighbors.append(State(tuple(new_tiles), self, action, self.cost + 1))

        # Baixo (não pode se estar na linha 2)
        if row < 2:
            new_idx = blank + 3
            moved_number = self.tiles[new_idx]
            new_tiles = list(self.tiles)
            new_tiles[blank], new_tiles[new_idx] = new_tiles[new_idx], new_tiles[blank]
            action = f"{moved_number}: BAIXO"
            neighbors.append(State(tuple(new_tiles), self, action, self.cost + 1))

        # Esquerda (não pode se estar na coluna 0)
        if col > 0:
            new_idx = blank - 1
            moved_number = self.tiles[new_idx]
            new_tiles = list(self.tiles)
            new_tiles[blank], new_tiles[new_idx] = new_tiles[new_idx], new_tiles[blank]
            action = f"{moved_number}: ESQUERDA"
            neighbors.append(State(tuple(new_tiles), self, action, self.cost + 1))

        # Direita (não pode se estar na coluna 2)
        if col < 2:
            new_idx = blank + 1
            moved_number = self.tiles[new_idx]
            new_tiles = list(self.tiles)
            new_tiles[blank], new_tiles[new_idx] = new_tiles[new_idx], new_tiles[blank]
            action = f"{moved_number}: DIREITA"
            neighbors.append(State(tuple(new_tiles), self, action, self.cost + 1))

        return neighbors

    def path(self) -> List["State"]:
        """Retorna a sequência de estados do estado inicial até este."""
        path = []
        current = self
        while current is not None:
            path.append(current)
            current = current.parent
        return path[::-1]  # inverte para começar do inicial

    def actions(self) -> List[str]:
        """Retorna a sequência de ações do estado inicial até este."""
        path = self.path()
        # O primeiro estado não tem ação, então pulamos ele
        return [state.action for state in path[1:] if state.action is not None]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, State) and self.tiles == other.tiles

    def __hash__(self) -> int:
        return hash(self.tiles)

    def __lt__(self, other: "State") -> bool:
        return self.cost < other.cost

    def __repr__(self) -> str:
        t = self.tiles
        return (
            f"+-------+\n"
            f"| {t[0]} {t[1]} {t[2]} |\n"
            f"| {t[3]} {t[4]} {t[5]} |\n"
            f"| {t[6]} {t[7]} {t[8]} |\n"
            f"+-------+"
        ).replace("0", " ")

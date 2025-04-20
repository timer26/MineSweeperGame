import random
from abc import ABC, abstractmethod
from GlobalData.GlobalContext import Context




    


class Tile(ABC):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @abstractmethod
    def scan_context(self, tile_grid):
        pass

    @abstractmethod
    def on_click(self, tile_grid):
        pass


class EmptyTile(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.adjacent_mines = 0
        self.revealed = False

    def scan_context(self, tile_grid):
        neighbors = tile_grid.get_neighbors(self.x, self.y)
        self.adjacent_mines = sum(isinstance(tile, MineTile) for tile in neighbors)

    def on_click(self, tile_grid):
        if self.revealed:
            return

        print(f"Clicked empty tile at ({self.x}, {self.y}) with {self.adjacent_mines} adjacent mines")
        self.revealed = True

        to_reveal = {(self.x, self.y)}
        visited = set()

        def cast_ray(x, y, dx, dy):
            while 0 <= x < tile_grid.width and 0 <= y < tile_grid.height:
                if (x, y) in visited:
                    break
                visited.add((x, y))

                tile = tile_grid.grid[y][x]
                if not isinstance(tile, EmptyTile):
                    break  # Stop on non-empty

                to_reveal.add((x, y))

                if tile.adjacent_mines > 0:
                    break  # Wall — reveal but stop ray
                x += dx
                y += dy

        # Cast rays in all 8 directions
        for dx, dy in tile_grid.DIRECTIONS:
            cast_ray(self.x + dx, self.y + dy, dx, dy)

        # Reveal all tiles in ray paths
        for x, y in to_reveal:
            tile = tile_grid.grid[y][x]
            if not tile.revealed:
                tile.revealed = True
                print(f"Revealed tile at ({x}, {y}) with {tile.adjacent_mines} adjacent mines")

            # Also reveal their neighbors (wall border effect)
            for neighbor in tile_grid.get_neighbors(x, y):
                if isinstance(neighbor, EmptyTile) and not neighbor.revealed:
                    neighbor.revealed = True


class MineTile(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.revealed = False

    def scan_context(self, tile_grid):
        pass

    def on_click(self, tile_grid):
        self.revealed = True
        print(f"💥 BOOM! Mine at ({self.x}, {self.y})")


class TileGrid:
    DIRECTIONS = [
            (-1,-1), (0,-1), (1,-1),
            (-1, 0),         (1, 0),
            (-1, 1), (0, 1), (1, 1)
                  ]

    def __init__(self, num_mines, width=None, height=None):
        self.width = width if width is not None else Context.grid_width
        self.height = height if height is not None else Context.grid_height
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.revealed_symbol="R"
        self.hidden_symbol="0"
        self.mine_symbol="M"
        self._place_mines(num_mines)
        self._fill_empty_tiles()
        self._scan_all_tiles()

    def _place_mines(self, num_mines):
        positions = [(x, y) for y in range(self.height) for x in range(self.width)]
        random.shuffle(positions)
        for i in range(num_mines):
            x, y = positions[i]
            self.grid[y][x] = MineTile(x, y)

    def _fill_empty_tiles(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] is None:
                    self.grid[y][x] = EmptyTile(x, y)

    def _scan_all_tiles(self):
        for row in self.grid:
            for tile in row:
                tile.scan_context(self)

    def get_neighbors(self, x, y):
        neighbors = []
        for dx, dy in self.DIRECTIONS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbors.append(self.grid[ny][nx])
        return neighbors

    def render_grid(self) -> list[list[str]]:
        visual_grid = []

        for row in self.grid:
            visual_row = []
            for tile in row:
                if isinstance(tile, EmptyTile):
                    if not tile.revealed:
                        visual_row.append(self.hidden_symbol)
                    elif tile.adjacent_mines == 0:
                        visual_row.append(self.revealed_symbol)
                    else:
                        visual_row.append(str(tile.adjacent_mines))
                elif isinstance(tile, MineTile):
                    if tile.revealed:
                        visual_row.append(self.mine_symbol)
                    else:
                        visual_row.append(self.hidden_symbol)
                else:
                    visual_row.append("?")
            visual_grid.append(visual_row)

        return visual_grid

    def render_cheat_grid(self) -> list[list[str]]:

        visual_grid = []

        for row in self.grid:
            visual_row = []
            for tile in row:
                if isinstance(tile, EmptyTile):
                    if not tile.revealed:
                        visual_row.append("0")
                    elif tile.adjacent_mines == 0:
                        visual_row.append(".")
                    else:
                        visual_row.append(str(tile.adjacent_mines))
                elif isinstance(tile, MineTile):
                    if tile.revealed:
                        visual_row.append("M")
                    else:
                        visual_row.append("0")
                else:
                    visual_row.append("?")
            visual_grid.append(visual_row)

        return visual_grid
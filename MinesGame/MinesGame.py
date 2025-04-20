from GlobalData.GlobalContext import Context


class TileGrid:
    def __init__(self, width, height, num_mines):
        self.width = Context
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        self._place_mines(num_mines)
        self._fill_tiles()

    def _place_mines(self, num_mines):
        # randomly place mines
        pass

    def _fill_tiles(self):
        # set EmptyTile or MineTile instances
        pass

    def get_neighbors(self, x, y):
        # returns a list of neighbor tiles
        pass
class Tile:
    
    def scan_context(self):                 
        ...
    def on_click(self):
        ...
    
    
    
    
class EmptyTile(Tile):

    def scan_context(self):     
        ...
    def on_click(self):        
        ...
    
    
    
class MineTile(Tile):

    def scan_context(self):
        ...
    def on_click(self):         #udela bum
        ...
    
#napsat pomocí dědičnosti 
#použí abstract dekorátor
#každá mina bude přidávat +1 do okolních tile --> mechanika hledíní
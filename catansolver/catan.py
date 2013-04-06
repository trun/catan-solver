GRAIN = 'grain'
SHEEP = 'sheep'
BRICK = 'brick'
WOOD = 'wood'
ORE = 'ore'
DESERT = 'desert'

STARTING_RESOURCES = (
    [ GRAIN ] * 4 +
    [ SHEEP ] * 4 +
    [ BRICK ] * 3 +
    [ WOOD ] * 4 +
    [ ORE ] * 3 +
    [ DESERT ]
)

class Tile(object):
    RESOURCES = {
        GRAIN: 'yellow',
        SHEEP: 'lightgreen',
        BRICK: 'red',
        WOOD: 'green',
        ORE: 'gray',
        DESERT: 'white',
    }

    def __init__(self):
        self.resource = None
        self.number = None

    def color(self):
        return self.RESOURCES[self.resource]

    def dots(self):
        n = self.number
        if n == 6 or n == 8:
            return 5
        if n == 5 or n == 9:
            return 4
        if n == 4 or n == 10:
            return 3
        if n == 3 or n == 11:
            return 2
        if n == 2 or n == 12:
            return 1
        return 0

    def to_dict(self):
        return {
            'resource': self.resource,
            'number': self.number,
            'color': self.color(),
            'dots': self.dots(),
        }


class Board(object):
    ORDER = [
        (4,0), (4,1), (4,2), (3,3),
        (2,4), (1,3), (0,2), (0,1),
        (0,0), (1,0), (2,0), (3,0),
        (3,1), (3,2), (2,3), (1,2),
        (1,1), (2,1), (2,2),
    ]

    NUMBERS = [ 5, 2, 6, 3, 8, 10, 9, 12, 11, 4, 8, 10, 9, 4, 5, 6, 3, 11 ]

    def __init__(self, resources):
        self.tiles = [
            [ Tile(), Tile(), Tile() ],
            [ Tile(), Tile(), Tile(), Tile() ],
            [ Tile(), Tile(), Tile(), Tile(), Tile() ],
            [ Tile(), Tile(), Tile(), Tile() ],
            [ Tile(), Tile(), Tile() ],
        ]

        resources = resources[:]
        for row in self.tiles:
            for tile in row:
                tile.resource = resources.pop(0)

        numbers = self.NUMBERS[:]
        for row, col in self.ORDER:
            tile = self.tiles[row][col]
            if tile.resource != DESERT:
                tile.number = numbers.pop(0)

    def to_dict(self):
        return [ [ tile.to_dict() for tile in row ] for row in self.tiles ]

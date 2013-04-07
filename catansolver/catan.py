GRAIN = 'G'
SHEEP = 'S'
BRICK = 'B'
WOOD = 'W'
ORE = 'O'
DESERT = '-'

STARTING_RESOURCES = (
    [ GRAIN ] * 4 +
    [ SHEEP ] * 4 +
    [ BRICK ] * 3 +
    [ WOOD ] * 4 +
    [ ORE ] * 3 +
    [ DESERT ]
)

class Direction(object):
    @staticmethod
    def opposite(ordinal):
        return (ordinal + 3) % 6

    @staticmethod
    def opposite_vertex(ordinal):
        return (ordinal + 4) % 6


class Tile(object):
    RESOURCE_COLORS = {
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
        self.vertices = [ None ] * 6
        self.edges = [ None ] * 6

    def color(self):
        return self.RESOURCE_COLORS[self.resource]

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


class Vertex(object):
    def __init__(self):
        self.tiles = set()
        self.edges = set()
        self.settlement = None

    def occupied(self):
        return self.settlement is not None

    def can_settle(self):
        if self.occupied():
            return False
        for vertex in self.neighbors():
            if vertex.occupied():
                return False
        return True

    def neighbors(self):
        return [ edge.opposite(self) for edge in self.edges ]


class Edge(object):
    def __init__(self):
        self.tiles = set()
        self.vertices = set()
        self.road = None

    def opposite(self, vertex):
        for other in self.vertices:
            if other is vertex:
                continue
            return other
        return None


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
        self.board = [
            [ Tile(), Tile(), Tile() ],
            [ Tile(), Tile(), Tile(), Tile() ],
            [ Tile(), Tile(), Tile(), Tile(), Tile() ],
            [ Tile(), Tile(), Tile(), Tile() ],
            [ Tile(), Tile(), Tile() ],
        ]

        self.tiles = [ tile for row in self.board for tile in row ]

        self._connect_tiles(0, None, 1, 4, 3, None, None)
        self._connect_tiles(1, None, 2, 5, 4, 0, None)
        self._connect_tiles(2, None, None, 6, 5, 1, None)
        self._connect_tiles(3, 0, 4, 8, 7, None, None)
        self._connect_tiles(4, 1, 5, 9, 8, 3, 0)
        self._connect_tiles(5, 2, 6, 10, 9, 4, 1)
        self._connect_tiles(6, None, None, 11, 10, 5, 2)
        self._connect_tiles(7, 3, 8, 12, None, None, None)
        self._connect_tiles(8, 4, 9, 13, 12, 7, 3)
        self._connect_tiles(9, 5, 10, 14, 13, 8, 4)
        self._connect_tiles(10, 6, 11, 15, 14, 9, 5)
        self._connect_tiles(11, None, None, None, 15, 10, 6)
        self._connect_tiles(12, 8, 13, 16, None, None, 7)
        self._connect_tiles(13, 9, 14, 17, 16, 12, 8)
        self._connect_tiles(14, 10, 15, 18, 17, 13, 9)
        self._connect_tiles(15, 11, None, None, 18, 14, 10)
        self._connect_tiles(16, 13, 17, None, None, None, 12)
        self._connect_tiles(17, 14, 18, None, None, 16, 13)
        self._connect_tiles(18, 15, None, None, None, 17, 14)

        for tile in self.tiles:
            for i, edge in enumerate(tile.edges):
                vertexA = tile.vertices[i]
                vertexB = tile.vertices[(i + 1) % 6]
                edge.tiles.add(tile)
                edge.vertices.add(vertexA)
                edge.vertices.add(vertexB)
                vertexA.tiles.add(tile)
                vertexB.tiles.add(tile)
                vertexA.edges.add(edge)
                vertexB.edges.add(edge)

        resources = resources[:]
        for row in self.board:
            for tile in row:
                tile.resource = resources.pop(0)

        numbers = self.NUMBERS[:]
        for row, col in self.ORDER:
            tile = self.board[row][col]
            if tile.resource != DESERT:
                tile.number = numbers.pop(0)

    def _connect_tiles(self, tile_num, *args):
        tileA = self.tiles[tile_num]
        for i, n in enumerate(args):
            if n is None:
                tileA.edges[i] = Edge()
                tileA.vertices[i] = tileA.vertices[i] or Vertex()
            else:
                e_op = Direction.opposite(i)
                v_op = Direction.opposite_vertex(i)
                tileB = self.tiles[n]

                # edge
                edge = tileA.edges[i] or tileB.edges[e_op] or Edge()
                tileA.edges[i] = edge
                tileB.edges[e_op] = edge

                # vertex
                vertex = tileA.vertices[i] or tileB.vertices[v_op] or Vertex()
                tileA.vertices[i] = vertex
                tileB.vertices[v_op] = vertex


    def to_dict(self):
        return [ [ tile.to_dict() for tile in row ] for row in self.board ]


from map_checker import *
from map_reader import *
from map_writer import *
from position import Position


class Map:
    def __init__(self, map=None):
        if map is None:
            map = [[]]
        if not isinstance(map, type([[]])):
            raise Exception('map is not a two-dimension array')
        self.map = map
        self.x_size = len(map)
        self.y_size = len(map[0])

    def __getitem__(self, i):
        return self.map[i]

    def get(self, position: Position):
        return self.map[position.x][position.y]

    def is_out_of_map(self, position: Position):
        return position.x < 0 or position.x >= self.x_size or position.y < 0 or position.y >= self.y_size

    def has_route_from(self, start: Position):
        return map_has_route_from(start, self)

    def read_from(self, path: str):
        self.__init__(read_map(path))

    def write_to(self, path=''):
        write_map(self, path)

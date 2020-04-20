
from game_field.game_field_checker import check_field
from models.cell import RubberRoom
from models.direction import Direction
from models.position import Position


class GameField:
    def __init__(self, field):
        self.field = field
        self.x_size = self.field.x_size
        self.y_size = self.field.y_size
        self.players_at_position = [[set() for _ in range(self.y_size)] for _ in range(self.x_size)]
        self.position_by_player = {}

    def __getitem__(self, position: Position):
        return self.field[position]

    def reset(self):
        self.__init__(self.field)

    def players_at(self, position: Position):
        return self.players_at_position[position.x][position.y]

    def player_position(self, player):
        return self.position_by_player[player]

    def player_cell(self, player):
        return self[self.position_by_player[player]]

    def add_player_at(self, player, position: Position):
        self.players_at_position[position.x][position.y].add(player)
        self.position_by_player[player] = position

    def remove_player(self, player):
        player_position = self.position_by_player[player]
        self.players_at_position[player_position.x][player_position.y].remove(player)
        del self.position_by_player[player]

    def player_go_to(self, player, destination):
        assert isinstance(destination, Direction) or isinstance(destination, Position)
        if isinstance(destination, Direction):
            destination = self.position_by_player[player].copy_shift_to(destination)
        player_position = self.position_by_player[player]
        self.players_at_position[player_position.x][player_position.y].remove(player)
        self.position_by_player[player] = destination
        self.players_at_position[destination.x][destination.y].add(player)

    def player_can_go_from_to(self, position, direction):
        if self.field[position].has_border_at(direction) or\
                self.field.is_out_of_field(position.copy_shift_to(direction)) or\
                (isinstance(self.field[position], RubberRoom) and self.field[position].direction != direction):
            return False
        return True

    def player_can_go_to(self, player, direction):
        player_position = self.position_by_player[player]
        return self.player_can_go_from_to(player_position, direction)

    def player_try_go_to(self, player, direction):
        if self.player_can_go_to(player, direction):
            self.player_go_to(player, direction)
            return True
        else:
            return False

    def check_field(self):
        position = check_field(self)
        if position is not None:
            raise LookupError(position)
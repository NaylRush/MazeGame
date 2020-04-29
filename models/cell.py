
from models.direction import Direction
from models.inventory import Inventory
from models.position import Position


class Cell:
    def __init__(self):
        self.name = type(self).__name__
        self.position = None
        self.borders = {direction: False for direction in Direction}
        self.teleport_dest_from = []
        self.inventory = None

    def locate_at(self, position):
        self.position = position

    def add_border_at(self, direction: Direction):
        self.borders[direction] = True

    def has_border_at(self, direction: Direction):
        return self.borders[direction]

    def to_symbol(self):
        return self.name[0]

    def take_inventory(self, game):
        if self.inventory is not None:
            print('You have got someone\'s inventory!')
            if self.inventory.has_key:
                print('You have got a key!')
            game.current_player.inventory.append(self.inventory)
            self.inventory = None
            print(game.current_player.inventory)

    def can_go_this_direction(self, game, game_impl, direction):
        return True

    def arrive(self, game, game_impl):
        pass


class Empty(Cell):
    def __init__(self):
        super().__init__()

    def to_symbol(self):
        return '.'


class Key(Cell):
    def __init__(self):
        super().__init__()
        self.inventory = Inventory(has_key=True)


class Stun(Cell):
    def __init__(self, duration: int):
        assert duration >= 0
        super().__init__()
        self.duration = duration

    def arrive(self, game, game_impl):
        game.current_player.stun = self.duration
        print('You are stunned by {} steps'. format(game.current_player.stun))


class RubberRoom(Cell):
    def __init__(self, direction: Direction):
        super().__init__()
        self.direction = direction

    def to_symbol(self):
        return self.direction.to_char()

    def can_go_this_direction(self, game, game_impl, direction):
        if direction == self.direction:
            print('You leaved a rubber room')
            return True
        game_impl.successful()
        return None


class Teleport(Cell):
    def __init__(self, dest: tuple):
        assert isinstance(dest, tuple)
        super().__init__()
        self.destination = Position(dest[0], dest[1])

    def arrive(self, game, game_impl):
        current_field = game.game_fields[game.current_player.field_id[-1]]
        current_field.player_go_to(game.current_player, self.destination)
        print('You have been teleported')
        current_field.player_cell(game.current_player).take_inventory(game)


class Armory(Cell):
    def __init__(self):
        super().__init__()

    def arrive(self, game, game_impl):
        game.current_player.inventory.update_bullets()
        print('You have got bullets!')
        print(game.current_player.inventory)


class Sleep(Cell):
    def __init__(self, duration: int, coords: tuple):
        assert duration >= 0
        assert isinstance(coords, tuple) and len(coords) == 3
        super().__init__()
        self.duration = duration
        self.destination_map_id = coords[0]
        self.destination_position = Position(coords[1], coords[2])

    def arrive(self, game, game_impl):
        game.game_fields[self.destination_map_id].add_player_at(game.current_player, self.destination_position)
        game.current_player.field_id.append(self.destination_map_id)
        game.current_player.sleep_for(self.duration)


class Exit(Cell):
    def __init__(self, direction: Direction):
        super().__init__()
        self.direction = direction

    def can_go_this_direction(self, game, game_impl, direction):
        if direction != self.direction:
            return True
        if game.key_required and not game.current_player.inventory.has_key:
            print('You need a key to get out!')
        else:
            if game.current_player.is_sleeping():
                print('You won the game! But it was a dream and you waked up...')
                game_impl.wake_up_player()
                return None
            game.game_is_over = True
            print('Game is over! Player {} wins!'.format(game.current_player.id))
        return None

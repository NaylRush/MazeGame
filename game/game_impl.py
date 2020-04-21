
from copy import deepcopy
from game_field.game_field import random_position_on_field
from models.cell import Stun, RubberRoom, Teleport, Armory, Exit
from models.direction import Direction
from models.player import Player


class GameImpl:
    def __init__(self):
        self.current_player_index = 0

    def successful(self, game):
        print('You passed')

    def unsuccessful(self, game):
        print('You bumped into a wall')

    def whats_in_inventory(self, game):
        print(game.current_player.inventory)

    def update_bullets(self, game):
        game.current_player.inventory.update_bullets()
        print('You have got bullets!')
        self.whats_in_inventory(game)

    def kill_player(self, game, killed_player):
        killed_player.stun = 1
        game.game_field.player_position(killed_player).inventory = deepcopy(killed_player.inventory)
        killed_player.inventory.reset()
        game.game_field.player_go_to(killed_player, killed_player.start_position)
        print('Player {} kills Player {}!'.format(game.current_player.id, killed_player.id))
        print('Player {} has been teleported to his start position'.format(killed_player.id))

    def stun_for(self, game, duration):
        game.current_player.stun = duration
        print('You are stunned by {} steps'. format(game.current_player.stun))

    def can_player_go(self, game):
        if game.current_player.stun == 0:
            return True
        stun = game.current_player.stun
        print('Player {} is still stunned by {}'.format(game.current_player.id,
              '1 step' if stun == 1 else (str(stun) + ' steps')))
        game.current_player.stun -= 1
        return False

    def player_leaved_rubber_room(self, game):
        print('You leaved a rubber room')

    def teleport_to(self, game, destination):
        print('You have been teleported')
        game.game_field.player_go_to(game.current_player, destination)

    def key_required(self, game):
        print('You need a key to get out!')

    def try_to_exit(self, game):
        if game.key_required and not game.current_player.inventory.has_key:
            self.key_required(game)
            return
        game.game_is_over = True
        print('Game is over! Player {} wins!'.format(game.current_player.id))

    def shoot(self, game, direction: Direction):
        if game.current_player.inventory.bullets == 0:
            print('You are out of bullets')
            return False
        game.current_player.inventory.bullets -= 1
        current_position = deepcopy(game.game_field.player_position(game.current_player))
        while not game.game_field.field.is_out_of_field(current_position):
            players = game.game_field.players_at(current_position)
            if len(players) != 0 and not (len(players) == 1 and game.current_player in players):
                if len(players) == 1 and game.current_player in players:
                    current_position.shift_to(direction)
                    break
                killed_player = players.pop()
                if killed_player == game.current_player:
                    killed_player = players.pop()
                    players.add(game.current_player)
                players.add(killed_player)
                self.kill_player(game, killed_player)
                return True
            current_position.shift_to(direction)
        print('Your shot did not hit anyone')
        return True

    def take_inventory(self, game, cell):
        print('You have got someone\'s inventory!')
        if cell.inventory.has_key:
            print('You have got a key!')
        game.current_player.inventory.append(cell.inventory)
        cell.inventory = None
        self.whats_in_inventory(game)

    def help(self, game):
        print('''Walk keys:
    W — Up
    A — Left
    S — Down
    D — Right

Actions:
    X <W, A, S, D> - Shoot

Other:
    E - Inventory
    ? - Help

After any action except 'Other' you make a step.

For more information read this —— https://github.com/NaylRush/MazeGame
@NaylRush''')

    def calc_next_player(self, game):
        self.current_player_index = (self.current_player_index + 1) % len(game.players)
        return game.players[self.current_player_index]

    def place_players(self, game, players_count, players_positions):
        players = []
        for i in range(players_count):
            players.append(Player())
            if players_positions is not None and i < len(players_positions):
                players[-1].start_position = players_positions[i]
                game.game_field.add_player_at(players[-1], players_positions[i])
            else:
                random_position = random_position_on_field(game.fields[0])
                players[-1].start_position = random_position
                game.game_field.add_player_at(players[-1], random_position)
        return players

    def check_position(self, game):
        current_cell = game.game_field.player_cell(game.current_player)
        if current_cell.inventory is not None:
            self.take_inventory(game, current_cell)
        if isinstance(current_cell, Armory):
            self.update_bullets(game)
            return
        elif isinstance(current_cell, Stun):
            self.stun_for(game, current_cell.duration)
            return
        elif isinstance(current_cell, Teleport):
            if isinstance(game.game_field.player_cell(game.current_player), Teleport):
                self.teleport_to(game, current_cell.destination)
            return

    def go_to(self, game, direction: Direction):
        current_cell = game.game_field.player_cell(game.current_player)
        # before step
        if isinstance(current_cell, RubberRoom):
            if direction != current_cell.direction:
                self.successful(game)
                return
            else:
                self.player_leaved_rubber_room(game)
        elif isinstance(current_cell, Exit) and direction == current_cell.direction:
            self.try_to_exit(game)
            return
        # step
        if not game.game_field.player_try_go_to(game.current_player, direction):
            self.unsuccessful(game)
        else:
            self.successful(game)
            self.check_position(game)

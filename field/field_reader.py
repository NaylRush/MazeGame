
from copy import deepcopy
from field.field import Field
from models.cell import Empty, Key, Stun, RubberRoom, Teleport, Armory, Sleep, Exit
from models.direction import UP, LEFT, DOWN, RIGHT


def read_fields(paths):
    fields = []
    for path in paths:
        with open(path, 'r') as fields_txt:
            lines = fields_txt.readlines()

        if len(lines[0].split()) == 2:
            symbol_by_cell = find_and_read_field_symbols(lines, 1)
            fields += [read_field(lines, symbol_by_cell)]
            continue

        field_amount = int(lines[0])
        lines.pop(0)
        symbol_by_cell = find_and_read_field_symbols(lines, field_amount)
        current_line = 0
        for _ in range(field_amount):
            x_size = int(lines[current_line].split()[0])
            field_lines = lines[current_line:current_line + x_size * 2 + 1]
            fields.append(read_field(field_lines, symbol_by_cell))
            current_line += x_size * 2 + (1 if fields[-1].has_key else 0)

    return fields


def find_and_read_field_symbols(lines, field_amount):
    current_line = 0

    # jump to cell symbols
    for _ in range(field_amount):
        x_size = int(lines[current_line].split()[0])
        current_line += x_size * 2

    # read cell symbols
    symbol_by_cell = {Empty().to_symbol(): Empty()}
    for line in lines[current_line:]:
        cell_type, command = line.split(maxsplit=1)
        symbol_by_cell[cell_type] = eval(command)

    return symbol_by_cell


def read_field(lines, symbol_by_cell):
    # read size
    x_size, y_size = map(int, lines[0].split())

    # read field
    field = [[None] * y_size for _ in range(x_size)]

    read_cells(field, lines, symbol_by_cell, x_size, y_size)

    walls = read_walls(lines, x_size, y_size)

    return Field(field, walls, has_key=symbol_by_cell.get(Key().to_symbol(), None) is not None)


def read_cells(field, lines, symbol_by_cell, x_size, y_size):
    for x, cell_symbols in enumerate(lines[1:x_size * 2:2]):
        for y, sym in enumerate(cell_symbols[:y_size * 2:2]):
            cell = deepcopy(symbol_by_cell[sym])
            field[x][y] = cell


def read_walls(lines, x_size, y_size):
    vertical_walls = [[False for _ in range(y_size)] for _ in range(x_size)]
    horizontal_walls = [[False for _ in range(y_size)] for _ in range(x_size)]

    # read vertical walls
    for line in range(x_size):
        for column, sym in enumerate(lines[1 + line * 2][1:y_size * 2:2]):
            if sym == '|':
                vertical_walls[line][column] = True

    # read horizontal walls
    for line in range(x_size):
        for column, sym in enumerate(lines[2 + line * 2][:y_size * 2:2]):
            if sym == '_' or sym == '-':
                horizontal_walls[line][column] = True

    return vertical_walls, horizontal_walls

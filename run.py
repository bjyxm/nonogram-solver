import nonogram_board
import itertools

input_column = '3 4 5 4 5 6 3,2,1 2,2,5 4,2,6 8,2,3 8,2,1,1 2,6,2,1 4,6 2,4 1'
input_row = '3 5 4,3 7 5 3 5 1,8 3,3,3 7,3,2 5,4,2 8,2 10 2,3 6'
# input_column = '2,1 2,1 1 2,1 2,1'
# input_row = '2,2 2,2 0 1,1 3'

CELL_SIZE = 20
VIDEO_FPS = 3
PADDING = 2


def render(board):
    # board.render_simple()
    # board.render_grid()
    board.render_frame(cell_size=CELL_SIZE, video_fps=VIDEO_FPS, padding=PADDING)


def item_parser(item):
    return [int(x) for x in item.split(',')]


# Solver 1 of 2 -
def mark(shape, numbers):
    base_blanks = [0] + [1] * (len(numbers) - 1) + [0]
    remainder = len(shape) - sum(numbers) - sum(base_blanks)

    every_blanks = list()
    for prod in itertools.product(range(remainder + 1), repeat=len(base_blanks)):
        if sum(prod) == remainder:
            added_blanks = list()
            for i in range(len(base_blanks)):
                added_blanks.append(base_blanks[i] + prod[i])
            every_blanks.append(added_blanks)

    every_compositions = list()
    for blank in every_blanks:
        composition = list()
        for i in range(len(blank)):
            composition += [0] * blank[i]
            if i in range(len(numbers)):
                composition += [1] * numbers[i]
        every_compositions.append(composition)

    # filter
    filtered_compositions = list()
    for comp in every_compositions:
        good = True
        for i in range(len(shape)):
            if shape[i] == '×' and comp[i] == 1:
                good = False
                break
            elif shape[i] == '■' and comp[i] == 0:
                good = False
                break
        if good:
            filtered_compositions.append(comp)

    calc_mul = [1] * len(shape)
    calc_sum = [0] * len(shape)
    for comp in filtered_compositions:
        for i in range(len(shape)):
            calc_mul[i] *= comp[i]
            calc_sum[i] += comp[i]

    result = ['□'] * len(shape)
    for i in range(len(shape)):
        if calc_mul[i] == 1:
            result[i] = '■'
        elif calc_sum[i] == 0:
            result[i] = '×'

    return result


# Solver 2 of 2 -
def solve(board):
    render(board)

    if board.is_complete():
        return True
    elif not board.is_valid():
        return False

    idx_first_empty = board.locate_first_empty()
    for symbol in '■×':
        board.set_cell(idx_first_empty, symbol)
        if solve(board):
            return board
        else:
            board.set_cell(idx_first_empty, '□')


def main():
    columns = list(map(item_parser, input_column.split(' ')))
    rows = list(map(item_parser, input_row.split(' ')))
    board = nonogram_board.Board(rows, columns)

    render(board)

    any_change = True
    while any_change:
        any_change = False
        for r in range(len(rows)):
            row = board.get_row(r)
            marked = mark(row, rows[r])
            change = board.set_row(r, marked)
            if change:
                render(board)
                any_change = True
        for c in range(len(columns)):
            column = board.get_column(c)
            marked = mark(column, columns[c])
            change = board.set_column(c, marked)
            if change:
                render(board)
                any_change = True

    if not board.is_complete():
        solve(board)


if __name__ == '__main__':
    main()

import numpy as np
from xcover import covers_bool


# def add_incidence_(piece_id,position):


# returs a panda array len width + number of pieces column
def create_incidence_matrix(pieces):

    incidence_matrix = np.empty((0, width_incidence_row))

    for piece_id, piece in pieces.items():
        positions = find_all_positions(board, piece)

        for position in positions:
            row_incidence = np.zeros(width_incidence_row)

            for piece_row_i, piece_col_i in position:
                index = (piece_row_i*width)+piece_col_i
                row_incidence[index] = 1

            row_incidence[piece_id] = 1
            incidence_matrix = np.append(
                incidence_matrix, [row_incidence], axis=0)
    np.set_printoptions(threshold=np.inf)

    # print(incidence_matrix)

    return incidence_matrix

    # for row_i in range(height):
    #     for column_j in range(width):

    #         print(row_incidence)


def rotate_piece(piece):
    rotations = []
    current = piece
    for _ in range(4):
        rotated = [(y, -x) for x, y in current]

        min_x = min(x for x, y in rotated)
        min_y = min(y for x, y in rotated)
        normalized = [(x - min_x, y - min_y) for x, y in rotated]

        if normalized not in rotations:
            rotations.append(normalized)

        current = normalized
    return rotations


# returns array of tuples with position of each possible position of a piece


def find_all_positions(board, piece):
    positions = []
    rotations = rotate_piece(piece)

    for rotated_piece in rotations:

        for row_i in range(height):
            for column_j in range(width):
                if is_valid_position(board, rotated_piece, row_i, column_j):
                    positions.append([(row_i+piece_row_i, column_j+piece_col_j)
                                      for piece_row_i, piece_col_j in rotated_piece])

                # max_i_piece = max(piece_i for piece_i, piece_j in piece)

    # len_pos = len(positions)
    # print("total positions for a piece:", len_pos)

    return positions


def is_valid_position(board, piece, row_i, column_j):

    # we chose heighst left poinst of a piece as anchor point and create offsets from that point
    # for each square of a piece is within width and height of the board which means:
    # 1- not: (square_height_offset +  row_i) >=height or < 0
    # 2- not: square_width_offset + col_j)>=width or < 0
    for square_height_offset, square_width_offset in piece:

        square_height = square_height_offset + row_i
        square_width = square_width_offset + column_j

        if square_height >= height or square_height < 0:
            return False
        if square_width >= width or square_width < 0:
            return False
        # remove this one
        if board[square_height][square_width] != 0:
            return False
    return True

    # valied_position_a = []

    # np_board= np.array(board)

    # 5_row 11_column

if __name__ == "__main__":
    # board
    width = 11
    height = 5
    count_squares = width*height
    number_of_pieces = 12

    width_incidence_row = count_squares + number_of_pieces

    board = [[0 for col in range(width)] for row in range(height)]

    # pieces
    # we chose heighst poinst of a piece as anchor point and create offsets from that point

    piece_a = [(0, 0), (1, 0), (0, 1), (0, 2), (1, 2)]
    piece_b = [(0, 0), (0, 1), (1, 0), (1, -1), (1, -2)]
    piece_c = [(0, 0), (1, 0), (1, -1), (2, 0), (2, 1)]
    piece_d = [(0, 0), (1, 0), (1, 1), (1, -1)]
    piece_e = [(0, 0), (1, 0), (1, 1), (1, -1), (1, 2)]
    piece_f = [(0, 0), (0, 1), (1, 0), (1, 1), (1, -1)]
    piece_g = [(0, 0), (0, 1), (1, 0), (1, -1)]
    piece_h = [(0, 0), (0, 1), (1, 0), (2, 0)]
    piece_i = [(0, 0), (0, 1), (0, 2), (2, 1), (2, 2)]
    piece_j = [(0, 0), (0, 1), (1, 1), (1, 2), (1, 3)]
    piece_k = [(0, 0), (1, 0), (1, 1)]
    piece_l = [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2)]


    # index_last_cell
    # pieces = {count_squares: piece_a,
    #        count_squares+1: piece_b,
    #         count_squares+2: piece_c}

    pieces = {
        count_squares: piece_a,
        count_squares+1: piece_b,
        count_squares+2: piece_c,
        count_squares+3: piece_d,
        count_squares+4: piece_e,
        count_squares+5: piece_f,
        count_squares+6: piece_g,
        count_squares+7: piece_h,
        count_squares+8: piece_i,
        count_squares+9: piece_j,
        count_squares+10: piece_k,
        count_squares+11: piece_l,
    }

    # print(pieces)

    # for square_height_offset, square_width_offset in piece_a:
    #     print(square_height_offset)
    # row_incidence = [0 for i in range(10)]
    # print(row_incidence)


    # positions = find_all_positions(board, piece_a)
    # msg = f'row: {row_i} column: {column_j} '
    # positions.append((row_i, column_j))

    incidence = create_incidence_matrix(pieces)

    print("total number of posisitions: ", len(incidence))

    #print("incidence matrix:")
    # print(incidence)


    sol = covers_bool(incidence)
    total_solusions = len(list(sol))

    print("total number of solusion: ", total_solusions)

    # print("all solusions:", ec.get_exact_cover(incidence))


    # print(positions[0:2])
    # create_incidence_matrix(positions[0:10])

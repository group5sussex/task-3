from django.http import HttpResponse
from django.http import JsonResponse
from django.http import StreamingHttpResponse

import numpy as np
from xcover import covers_bool
import matplotlib.pyplot as plt
import time
import json

# return sample json file

# sample response


def index(request):

    data = [[65, 65, 62, 62, 62, 59, 59, 59, 59, 57, 56], [65, 60, 62, 66, 66, 61, 59, 57, 57, 57, 56], [60, 60, 66, 66, 58, 61,
                                                                                                         61, 63, 57, 56, 56], [60, 60, 66, 64, 58, 58, 61, 63, 55, 56, 55], [64, 64, 64, 64, 58, 63, 63, 63, 55, 55, 55]]

    response = HttpResponse(json.dumps(data), content_type="application/json")
    return response


# input json
# {
#   "initial_state": [
#     { "65": [[0, 0], [1, 0], [0, 1]] },
#     { "64": [[4, 0], [4, 1], [4, 2], [4, 3], [3, 3]] }
#   ]
# }

# required state like this
# initial_state = [
#     {65: [(0, 0), (1, 0), (0, 1)]},
#     {64: [(4, 0), (4, 1), (4, 2), (4, 3), (3, 3)]},]


def submit(request):
    data = json.loads(request.body.decode('utf-8'))
    initial_state = data.get('initial_state', [])

    for state in data['initial_state']:
        for key, value in state.items():
            state[key] = [tuple(item) for item in value]

    incidence_matrix = create_incidence_matrix(
        pieces, initial_state=initial_state)

    def stream_content():

        for solution in covers_bool(incidence_matrix):
            result = get_solution_board(solution, incidence_matrix)
            yield f"data: {json.dumps(result.tolist())}\n\n"

    # Create the StreamingHttpResponse
    response = StreamingHttpResponse(
        stream_content(), content_type="text/event-stream")
    response['Content-Disposition'] = 'inline; filename="stream.txt"'
    return response


def create_incidence_matrix(pieces, initial_state):
    incidence_matrix = np.empty((0, width_incidence_row))

    for initial_pieces in initial_state:
        for key, positions in initial_pieces.items():
            piece_id = int(key)
            row_incidence = np.zeros(width_incidence_row)
            row_incidence[piece_id] = 1

            for position in positions:
                piece_row_i, piece_col_j = position
                index = (piece_row_i*width)+piece_col_j
                row_incidence[index] = 1

            incidence_matrix = np.append(
                incidence_matrix, [row_incidence], axis=0)

            del pieces[piece_id]

    for piece_id, piece in pieces.items():
        positions = find_all_positions(board, piece)

        for position in positions:
            row_incidence = np.zeros(width_incidence_row)

            for piece_row_i, piece_col_j in position:
                index = (piece_row_i*width)+piece_col_j
                row_incidence[index] = 1

            row_incidence[piece_id] = 1
            incidence_matrix = np.append(
                incidence_matrix, [row_incidence], axis=0)
    np.set_printoptions(threshold=np.inf)

    return incidence_matrix


def generate_mirrors(piece):
    mirrors = []

    mirrors.append(piece)

    horizontal_mirror = [(-x, y) for x, y in piece]
    mirrors.append(horizontal_mirror)

    vertical_mirror = [(x, -y) for x, y in piece]
    mirrors.append(vertical_mirror)

    both_mirrors = [(-x, -y) for x, y in piece]
    mirrors.append(both_mirrors)

    return mirrors


def rotate_piece(piece):
    transformations = []

    mirrors = generate_mirrors(piece)

    for mirror in mirrors:
        current = mirror
        for _ in range(4):
            rotated = [(y, -x) for x, y in current]

            min_x = min(x for x, y in rotated)
            min_y = min(y for x, y in rotated)
            normalized = [(x - min_x, y - min_y) for x, y in rotated]

            if normalized not in transformations:
                transformations.append(normalized)

            current = normalized

    return transformations


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


# board
width = 11
height = 5
count_squares = width*height
number_of_pieces = 12
width_incidence_row = count_squares + number_of_pieces

i = count_squares
j = count_squares+number_of_pieces


board = [[0 for col in range(width)] for row in range(height)]
solution_board = [[0 for col in range(width)] for row in range(height)]

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
piece_i = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)]
piece_j = [(0, 0), (1, 0), (1, 1), (1, 2), (1, 3)]
piece_k = [(0, 0), (1, 0), (1, 1)]
piece_l = [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2)]


pieces = {count_squares: piece_a,
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


# solution=[2804, 906, 389, 2090, 1284, 1785, 979, 543, 65, 2572, 2173, 1535]
def get_solution_board(solution, incidence_matrix):

    for item in solution:
        piece_id = np.where(incidence_matrix[item][i: j] == 1)[0]
        piece_id = piece_id[0]+count_squares

        for idx, cell in enumerate(incidence_matrix[item][:count_squares]):
            # print(f"idx,cell : {idx}, {+cell}")
            if (cell == 1):
                row_i = idx//width
                column_j = idx % width
                # print(f"col,row : {column_j}, {+row_i}")
                solution_board[row_i][column_j] = piece_id

    solution = np.matrix(solution_board)
    print(solution)
    return np.matrix(solution)


'''


incidence_matrix = create_incidence_matrix(
    pieces)

for solution in covers_bool(incidence_matrix):
    print(get_solution_board(solution))

    plt.imshow(get_solution_board(solution), cmap='Spectral',
               interpolation='nearest')
    plt.colorbar()
    plt.show()
'''

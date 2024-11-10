from django.http import HttpResponse
from django.http import JsonResponse

import numpy as np
from xcover import covers_bool
import xcover
import matplotlib.pyplot as plt


def index(request):
    return HttpResponse("hello")


def submit(request):

    if request.method == 'POST':
        # Extract data from the POST request
        # 'data_key' is the name attribute in your HTML form
        data = request.POST.get('data_key', '')

        # Process the data as needed
        response_data = {
            'message': 'Data received successfully',
            'data': data,
        }

        # Return a JSON response
        return JsonResponse(request.body)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def create_incidence_from_initial_state(pieces, initial_state=[]):
    pass

    # for item in initial_state:
    #     key = list(item.keys())[0]
    #     key = int(key)
    #     del pieces[key]

    # print(pieces)

    return create_incidence_matrix(pieces)


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

    # Generate mirrors of the piece
    mirrors = generate_mirrors(piece)

    for mirror in mirrors:
        current = mirror
        for _ in range(3):  # Rotate four times (0, 90, 180, 270 degrees)
            # Rotate 90 degrees clockwise: (x, y) -> (y, -x)
            rotated = [(y, -x) for x, y in current]

            # Normalize so that the top-left corner is (0, 0)
            min_x = min(x for x, y in rotated)
            min_y = min(y for x, y in rotated)
            normalized = [(x - min_x, y - min_y) for x, y in rotated]

            # Add if this transformation is unique
            if normalized not in transformations:
                transformations.append(normalized)

            # Update current to the new rotation for the next 90-degree turn
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


'''

print(pieces)

for square_height_offset, square_width_offset in piece_a:
    print(square_height_offset)
row_incidence = [0 for i in range(10)]
print(row_incidence)


positions = find_all_positions(board, piece_a)
msg = f'row: {row_i} column: {column_j} '
positions.append((row_i, column_j))

incidence = create_incidence_matrix(pieces)

print("total number of posisitions: ", len(incidence))

print("incidence matrix:")
print(incidence)


sol = covers_bool(incidence)
total_solusions = len(list(sol))

print("total number of solusion: ", total_solusions)

print("all solusions:", ec.get_exact_cover(incidence))


print(positions[0:2])
create_incidence_matrix(positions[0:10])
incidence = create_incidence_matrix(pieces)

print("total number of posisitions: ", len(incidence))

print("incidence matrix:")
print(incidence)
sol = covers_bool(incidence)
total_solusions = len(list(sol))
print("total number of solusion: ", total_solusions)
###


'''


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


initial_state = []

incidence_matrix = create_incidence_matrix(
    pieces=pieces, initial_state=initial_state)

# print(incidence_matrix[-1])
# covers_bool(incidence_matrix)
i = count_squares
j = count_squares+number_of_pieces
solusion_board = [[0 for col in range(width)] for row in range(height)]

# solusion=[2804, 906, 389, 2090, 1284, 1785, 979, 543, 65, 2572, 2173, 1535]


def get_solusion_board(solusion):

    for item in solusion:
        piece_id = np.where(incidence_matrix[item][i: j] == 1)[0]
        piece_id = piece_id[0]+count_squares

        for idx, cell in enumerate(incidence_matrix[item][:count_squares]):
            # print(f"idx,cell : {idx}, {+cell}")
            if (cell == 1):
                row_i = idx//width
                column_j = idx % width
                # print(f"col,row : {column_j}, {+row_i}")
                solusion_board[row_i][column_j] = piece_id

    print(np.matrix(solusion_board))

    return solusion_board


#for solution in covers_bool(incidence_matrix):
 #   print(get_solusion_board(solution))

    # plt.imshow(get_solusion_board(solution), cmap='Spectral',
    #            interpolation='nearest')
    # plt.colorbar()
    # plt.show()

# sample input:
# { "0": [ [ 2, 3 ], [ 2, 4 ], [ 2, 5 ], [ 3, 3 ], [ 3, 5 ] ], "11": [ [ 1, 5 ], [ 1, 6 ], [ 2, 6 ], [ 2, 7 ], [ 3, 7 ] ] }
# key is the piece id (55 + index of piece) and value is the list of coordinates of the piece on the board


import numpy as np
from copy import deepcopy

pieces = {
    0: np.array([[1, 1, 1], [1, 0, 1]]),
    1: np.array([[0, 0, 2, 2], [2, 2, 2, 0]]),
    2: np.array([[0, 3, 0], [3, 3, 0], [0, 3, 3]]),
    3: np.array([[0, 4, 0], [4, 4, 4]]),
    4: np.array([[0, 5, 0, 0], [5, 5, 5, 5]]),
    5: np.array([[0, 6, 6], [6, 6, 6]]),
    6: np.array([[0, 7, 7], [7, 7, 0]]),
    7: np.array([[8, 8], [8, 0], [8, 0]]),
    8: np.array([[9, 9, 9], [0, 0, 9], [0, 0, 9]]),
    9: np.array([[10, 0, 0, 0], [10, 10, 10, 10]]),
    10: np.array([[0, 11], [11, 11]]),
    11: np.array([[12, 12, 0], [0, 12, 12], [0, 0, 12]])
}

def transform_to_board(data):
    board = [[0 for _ in range(11)] for _ in range(5)]
    for key, coordinates in data.items():
        piece_id = int(key) + 1
        for coord in coordinates:
            board[coord[0]][coord[1]] = piece_id
    return board

def find_free_pieces(board):
    used_pieces = set()
    for row in board:
        for cell in row:
            if cell != 0:
                used_pieces.add(cell)

    free_pieces = {key: piece for key, piece in pieces.items() if key + 1 not in used_pieces}
    return free_pieces

def check_neighbours(bool_board, i, j):
    neighbours = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
    neighbours = [(x, y) for x, y in neighbours if 0 <= x < 5 and 0 <= y < 11]
    for x, y in neighbours:
        if bool_board[x][y] == 0:
            return True
    return False

def check_win(bool_board):
    for row in bool_board:
        if 0 in row:
            return False
    return True

def place_piece(board, piece, x, y):
    new_board = deepcopy(board)
    piece_height, piece_width = piece.shape
    for i in range(piece_height):
        for j in range(piece_width):
            if piece[i][j] != 0:
                new_board[x + i][y + j] = piece[i][j]
    return new_board

def mirror_piece(piece):
    mirrors = [piece, np.fliplr(piece), np.flipud(piece)]
    return mirrors

def rotate_and_mirror_piece(piece):
    transformations = set()
    for mirrored in mirror_piece(piece):
        for _ in range(4):
            transformations.add(tuple(map(tuple, mirrored)))  # Convert to tuple for hashable type in set
            mirrored = np.rot90(mirrored)
    return [np.array(transformation) for transformation in transformations]

def fit_piece(board, piece, x, y):
    piece_height, piece_width = piece.shape
    for i in range(piece_height):
        for j in range(piece_width):
            if piece[i][j] != 0:
                if x + i >= len(board) or y + j >= len(board[0]) or board[x + i][y + j] != 0:
                    return False
    return True


def check_board(board):
    is_0 = False

    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == 0:
                if check_neighbours(board, i, j):
                    is_0 = True
                else:
                    return False

    return is_0

def backtrack(board, free_pieces):
    if check_win(board):
        print("Win")
        yield deepcopy(board)
        return

    if check_board(board):
        return

    for piece_id, piece in free_pieces.items():
        for transformation in rotate_and_mirror_piece(piece):
            for i in range(len(board)):
                for j in range(len(board[0])):
                    if fit_piece(board, transformation, i, j):
                        new_board = place_piece(board, transformation, i, j)
                        new_free_pieces = {k: v for k, v in free_pieces.items() if k != piece_id}
                        yield from backtrack(new_board, new_free_pieces)

def solvePuzzle(input_data):
    board = transform_to_board(input_data)
    free_pieces = find_free_pieces(board)
    yield from backtrack(board, free_pieces)

def turn_board_to_front(board):
    result = {}
    for i in range(5):
        for j in range(11):
            if board[i][j] == 0:
                continue
            if result.get(str(board[i][j] - 1)) is None:
                result[str(board[i][j] - 1)] = []
            result[str(board[i][j] - 1)].append([i, j])
    return result

if __name__ == "__main__":
    input_data = { "0": [ [ 2, 3 ], [ 2, 4 ], [ 2, 5 ], [ 3, 3 ], [ 3, 5 ] ], "11": [ [ 1, 5 ], [ 1, 6 ], [ 2, 6 ], [ 2, 7 ], [ 3, 7 ] ] }
    for solution in solvePuzzle(input_data):
        print("Solution found:")
        for row in solution:
            print(row)
        print("\n")
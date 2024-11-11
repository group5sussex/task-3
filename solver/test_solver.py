import unittest

import views
from xcover import covers_bool
import numpy as np
import random
import itertools
# Create your tests here.


class SolverTest(unittest.TestCase):

    def test_solution_board_have_all_pieces(self):

        incidence_matrix = views.create_incidence_matrix(views.pieces, [])

        random_int = random.randint(0, 20)
        random_solution = next(itertools.islice(
            covers_bool(incidence_matrix), random_int, None))

        solusion_board = views.get_solution_board(
            random_solution, incidence_matrix)
        pieces_exist_in_solution = True

        for piece in views.pieces:
            if np.any(solusion_board[:, :] == piece) is False:
                pieces_exist_in_solution = False

        self.assertEqual(True, pieces_exist_in_solution)

    def test_solution_board_only_have_unique_pieces(self):

        # incidence_matrix = views.create_incidence_matrix(views.pieces, [])

        # random_int = random.randint(0, 20)

        # random_solution = next(itertools.islice(
        #     covers_bool(incidence_matrix), random_int, None))

        # print(random_solution)

        # list_pieces = np.where(random_solution[:] == 1)

        # print('lennn: ',len(list_pieces))

        pass

    def test_initial_positions_should_exists_in_solution(self):

        initial_state = [
            {"65": [[0, 0], [1, 0], [0, 1]]},
            {"64": [[4, 0], [4, 1], [4, 2], [4, 3], [3, 3]]}
]
        pass

        # def test_exact_cover_finds_all_the_positions(self):
        #     pass

        # def test_if_every_positions_is_added_to_the_incidence_matrix(self):
        #     pass

        # def test_api(self):
        #     pass

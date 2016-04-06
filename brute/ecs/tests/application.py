import os
from unittest import TestCase

from ecs.application import ElectionComputingSystem
from ecs.vote import Vote


class ApplicationTest(TestCase):
    def test_load_data_from_file_suit_1(self):
        # basic test for data loading
        filename = 'test_data1.txt'
        filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), filename)
        app = ElectionComputingSystem(1, 1)
        app.load_data_from_file(filename)
        self.assertEqual(app.candidates_number, 5)
        self.assertListEqual(
            app.candidates,
            ['Monika', 'Weronika', 'Beata', 'Zuzanna', 'Alicja']
        )
        self.assertEqual(app.voters_number, 10)
        self.assertEqual(app.unique_votes, 4)
        votes = [
            Vote(1, [1, 2, 3, 4, 5]),
            Vote(1, [3, 2, 1, 4, 5]),
            Vote(1, [2, 1, 3, 4, 5]),
            Vote(7, [5, 4, 3, 2, 1]),
        ]
        self.assertListEqual(
            [str(x) for x in app.votes],
            [str(x) for x in votes]
        )

    def test_get_election_results(self):
        filename = 'test_data1.txt'
        filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), filename)
        app = ElectionComputingSystem(1, 3)
        app.load_data_from_file(filename)
        self.assertEqual(
            app.algorithm.run(),
            (3, 4, 5)
        )
        del app

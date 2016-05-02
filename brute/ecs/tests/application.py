import os
from unittest import TestCase

from ecs.application import ElectionComputingSystem
from ecs.voter import Voter


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
            [c.name for c in app.candidates],
            ['Monika', 'Weronika', 'Beata', 'Zuzanna', 'Alicja']
        )
        self.assertEqual(app.voters_number, 10)
        self.assertEqual(app.unique_votes, 4)
        voters = [
            Voter(1, Voter.get_candidates_by_ids(app.candidates, [1, 2, 3, 4, 5])),
            Voter(1, Voter.get_candidates_by_ids(app.candidates, [3, 2, 1, 4, 5])),
            Voter(1, Voter.get_candidates_by_ids(app.candidates, [2, 1, 3, 4, 5])),
            Voter(7, Voter.get_candidates_by_ids(app.candidates, [5, 4, 3, 2, 1])),
        ]
        self.assertListEqual(
            [str(x) for x in app.voters],
            [str(x) for x in voters]
        )

    def test_get_election_results(self):
        filename = 'test_data1.txt'
        filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), filename)
        app = ElectionComputingSystem(1, 3)
        app.load_data_from_file(filename)
        self.assertEqual(
            app.algorithm.run(),
            Voter.get_candidates_by_ids(app.candidates, (3, 4, 5))
        )
        del app

import os
from unittest import TestCase

from ecs.application import ElectionComputingSystem
from ecs.voter import Voter
from ecs.exceptions import *


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

    def test_incorrect_type_of_candidates_number_exception(self):
        filename = 'test_exceptions1.soc'
        filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), filename)
        app = ElectionComputingSystem(1, 1)
        self.assertRaises(IncorrectTypeOfCandidatesNumberException, app.load_data_from_file, filename)

    def test_candidates_name_incorrect_format_exception(self):
        filename = 'test_exceptions2.soc'
        filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), filename)
        app = ElectionComputingSystem(1, 1)
        self.assertRaises(CandidatesNameIncorrectFormatException, app.load_data_from_file, filename)

    def test_summing_line_format_exception(self):
        filename = 'test_exceptions3.soc'
        filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), filename)
        app = ElectionComputingSystem(1, 1)
        self.assertRaises(SummingLineFormatException, app.load_data_from_file, filename)

    def test_summing_line_type_exception(self):
        filename = 'test_exceptions4.soc'
        filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), filename)
        app = ElectionComputingSystem(1, 1)
        self.assertRaises(SummingLineTypeException, app.load_data_from_file, filename)

    def test_bad_data_format_exception(self):
        filename = 'test_exceptions5.soc'
        filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), filename)
        app = ElectionComputingSystem(1, 1)
        self.assertRaises(BadDataFormatException, app.load_data_from_file, filename)

    def test_preference_order_type_exception(self):
        filename = 'test_exceptions6.soc'
        filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), filename)
        app = ElectionComputingSystem(1, 1)
        self.assertRaises(PreferenceOrderTypeException, app.load_data_from_file, filename)

    def test_preference_order_logic_exception(self):
        filename = 'test_exceptions7.soc'
        filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), filename)
        app = ElectionComputingSystem(1, 1)
        self.assertRaises(PreferenceOrderLogicException, app.load_data_from_file, filename)

    def test_non_positive_number_of_votes_exception(self):
        filename = 'test_exceptions8.soc'
        filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), filename)
        app = ElectionComputingSystem(1, 1)
        self.assertRaises(NonPositiveNumberOfVotesException, app.load_data_from_file, filename)

    def test_incorrect_votes_number_unique_votes_relation_exception(self):
        filename = 'test_exceptions9.soc'
        filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), filename)
        app = ElectionComputingSystem(1, 1)
        self.assertRaises(IncorrectVotesNumberUniqueVotesRelationException, app.load_data_from_file, filename)

    def test_preference_order_length_exception(self):
        filename = 'test_exceptions10.soc'
        filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), filename)
        app = ElectionComputingSystem(1, 1)
        self.assertRaises(PreferenceOrderLengthException, app.load_data_from_file, filename)

    def test_preference_order_beyond_scope_exception(self):
        filename = 'test_exceptions11.soc'
        filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), filename)
        app = ElectionComputingSystem(1, 1)
        self.assertRaises(PreferenceOrderBeyondScopeException, app.load_data_from_file, filename)

    def test_incorrect_preference_order_exception(self):
        filename = 'test_exceptions12.soc'
        filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), filename)
        app = ElectionComputingSystem(1, 1)
        self.assertRaises(IncorrectPreferenceOrderException, app.load_data_from_file, filename)

    def test_number_of_votes_inconsistency_exception(self):
        filename = 'test_exceptions13.soc'
        filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), filename)
        app = ElectionComputingSystem(1, 1)
        self.assertRaises(NumberOfVotesInconsistencyException, app.load_data_from_file, filename)

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

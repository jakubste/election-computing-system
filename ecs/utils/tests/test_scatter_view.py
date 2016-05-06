from ecs.utils.scatter_view import ScatterChartMixin
from ecs.utils.unittestcases import TestCase


class ScatterViewTestCase(TestCase):
    def setUp(self):
        self.view = ScatterChartMixin()

    def test_get_data_raises_not_implemented(self):
        self.assertRaises(NotImplementedError, self.view.get_data)

    def test_get_labels_raises_not_implemented(self):
        self.assertRaises(NotImplementedError, self.view.get_labels)

    def test_get_colors_raises_not_implemented(self):
        self.assertRaises(NotImplementedError, self.view.get_colors)

    def test_get_labels_returns_labels_from_field(self):
        labels = ['labelA', 'labelB']
        self.view.labels = labels
        self.assertEqual(self.view.get_labels(), labels)

    def test_get_colors_returns_colors_from_field(self):
        colors = ['colorA', 'colorB']
        self.view.colors = colors
        self.assertEqual(self.view.get_colors(), colors)

    def test_get_points_stroke_colors_defaults(self):
        self.view.datasets_number = 2
        self.assertEqual(self.view.get_points_stroke_colors(), ['black', 'black'])

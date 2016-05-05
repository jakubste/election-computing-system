from django.http import JsonResponse
from django.views.generic import View


class ScatterChartMixin(View):
    datasets_number = 0
    labels = None
    colors = None

    def get_data(self):
        raise NotImplementedError

    def get_labels(self):
        if not self.labels:
            raise NotImplementedError
        else:
            return self.labels

    def get_colors(self):
        if not self.colors:
            raise NotImplementedError
        else:
            return self.colors

    def get_points_stroke_colors(self):
        return ['black' for i in xrange(self.datasets_number)]

    def get_datasets(self, *args, **kwargs):
        """
        Format data to Scatter dataset format
        """
        labels = self.get_labels()
        colors = self.get_colors()
        point_stroke_colors = self.get_points_stroke_colors()
        data = self.get_data()

        return [
            {
                'label': labels[i],
                'pointColor': colors[i],
                'pointStrokeColor': point_stroke_colors[i],
                'data': [{'x': x, 'y': y} for (x, y) in data[i]]
            }
            for i in xrange(self.datasets_number)
            ]

    def get(self, *args, **kwargs):
        return JsonResponse(
            {'data': self.get_datasets(*args, **kwargs)}
        )

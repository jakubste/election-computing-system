from django.http import JsonResponse
from django.views.generic import View


class ChartMixin(View):
    datasets_number = 0
    labels = None
    colors = None
    points_stroke_colors = None
    points_radii = None
    title = ""

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
        if not self.points_stroke_colors:
            return ['black' for i in xrange(self.datasets_number)]
        else:
            return self.points_stroke_colors

    def get_points_radii(self):
        if not self.points_radii:
            return [5 for i in xrange(self.datasets_number)]
        else:
            return self.points_radii

    def get_title(self):
        return self.title

    def get_datasets(self, *args, **kwargs):
        """
        Format data to Scatter dataset format
        """
        labels = self.get_labels()
        colors = self.get_colors()
        point_stroke_colors = self.get_points_stroke_colors()
        points_radii = self.get_points_radii()
        data = self.get_data()

        return {
            'datasets': [
                {
                    'label': labels[i],
                    'borderColor': colors[i],
                    'backgroundColor': point_stroke_colors[i],
                    'data': data[i],
                    'pointRadius': points_radii[i]
                }
                for i in xrange(self.datasets_number)
                ],
            'title': self.get_title()
        }

    def get(self, *args, **kwargs):
        return JsonResponse(
            {'data': self.get_datasets(*args, **kwargs)}
        )

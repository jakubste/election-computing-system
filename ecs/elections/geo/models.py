from math import sqrt

from django.db.models import Model
from django.db.models.fields import IntegerField


class Point(Model):
    x = IntegerField()
    y = IntegerField()

    def distance(self, other):
        sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

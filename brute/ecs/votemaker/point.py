from math import sqrt


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def compute_euclidean_norm(a, b):
        """
        :param a: Point
        :param b: Point
        :return: distance between two points
        """
        return sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)

class Candidate:

    def __init__(self, candidate_id, name, coordinates=None):
        """
        :param candidate_id: id
        :param name: name
        :param coordinates: Point
        """
        self.candidate_id = candidate_id
        self.name = name
        self.coordinates = coordinates

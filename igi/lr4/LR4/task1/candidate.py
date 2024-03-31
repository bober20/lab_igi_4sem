class Candidate:
    def __init__(self, name, votes=0):
        self.name = name
        self._votes = votes

    @property
    def votes(self):
        return self._votes

    @votes.setter
    def votes(self, value):
        self._votes = value

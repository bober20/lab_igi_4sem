class Candidate:
    region = "Belarus"
    def __init__(self, name, votes=0):
        self.name = name
        self.__votes = votes

    @property
    def votes(self):
        return self.__votes

    @votes.setter
    def votes(self, value):
        self.__votes = value

    # def set_votes(self, value):
    #     self.__votes = value
    #
    # def get_votes(self):
    #     return self.__votes
    #
    # votes = property(get_votes, set_votes)


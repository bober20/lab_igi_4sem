from random import randint

from task1.candidate import Candidate


class Election:
    def __init__(self):
        self.candidates = (Candidate("candidate1"),
                           Candidate("candidate2"), Candidate("candidate3"))
        self.candidates_dict = dict()

        self.perform_election()
        self.create_candidates_dictionary()

    def initialize_candidates_using_dict(self, candidates_dict):
        """This function initialises candidates using dict which contains candidate's
                name and number of votes."""

        self.candidates = list()

        for i in candidates_dict.keys():
            self.candidates.append(Candidate(i, candidates_dict[i]))

    def create_candidates_dictionary(self):
        """This function creates candidates dictionary which contains candidate's
                name and number of votes for serialization."""

        item_name = "Candidate"

        for i in range(len(self.candidates)):
            self.candidates_dict.update({item_name + str(i): self.candidates[i].votes})

    def perform_election(self):
        """This function imitates election."""

        n = 2000
        for i in self.candidates:
            votes = randint(0, n)
            i.votes = votes

            n -= votes

    def get_winners(self):
        """This function returns candidates which passed the first election."""

        allowed_num_of_votes = 2000/3
        winners = list()

        for i in self.candidates:
            if i.votes >= allowed_num_of_votes:
                winners.append(i)

        return winners

    def get_candidate_info(self, name_of_candidate):
        """This function returns candidate's info."""

        for i in self.candidates:
            if i.name == name_of_candidate:
                return i

        print("There is no candidate with such name")

import pickle
import csv


class FileService:
    def __init__(self, items_dict):
        self.items_dict = items_dict

    def serialize_using_pickle(self):
        with open('lr_files/data.pickle', 'wb') as f:
            pickle.dump(self.items_dict, f)

    def deserialize_using_pickle(self):
        with open('lr_files/data.pickle', 'rb') as f:
            retrieved_data = pickle.load(f)

        return retrieved_data

    def serialize_using_csv(self):
        with open('lr_files/data.csv', 'w', newline='') as f:
            writer = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

            for i in self.items_dict.keys():
                writer.writerow([i] + [self.items_dict[i]])

    def deserialize_using_csv(self):
        with open('lr_files/data.csv', 'r', newline='') as f:
            reader = csv.reader(f, delimiter=' ', quotechar='|')

            candidates = dict()
            for row in reader:
                candidates.update({row[0]: row[1]})

        return candidates

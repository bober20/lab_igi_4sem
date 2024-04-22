import pickle
import csv
from task1.binary_mixin import BinaryMixin


class FileService(BinaryMixin):
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
            columns = ["name", "votes"]
            writer = csv.DictWriter(f, fieldnames=columns)

            writer.writeheader()

            for name, votes in sorted(self.items_dict.items()):
                writer.writerow(dict(name=name, votes=votes))

            # writer = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            #
            # for i in self.items_dict.keys():
            #     writer.writerow([i] + [self.items_dict[i]])


    def deserialize_using_csv(self):
        with open('lr_files/data.csv', 'r', newline='') as f:
            reader = csv.DictReader(f)

            items_dict = dict()

            for row in reader:
                items_dict.update({row["name"]: row["votes"]})

            # reader = csv.reader(f, delimiter=',', quotechar='|')
            #
            # items_dict = dict()
            # for row in reader:
            #     items_dict.update({row[0]: row[1]})

        return items_dict


    # def serialize_using_binary(self):
    #     with shelve.open('lr_files/data.bin') as items_list:
    #         for i in self.items_dict.keys():
    #             items_list[i] = self.items_dict[i]
    #
    #
    # def deserialize_using_binary(self):
    #     with shelve.open('lr_files/data.bin') as items_list:
    #         items_dict = dict()
    #
    #         for i in sorted(items_list):
    #             items_dict.update({i: items_list[i]})
    #
    #     return items_dict



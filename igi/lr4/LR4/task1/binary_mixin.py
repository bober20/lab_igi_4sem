import shelve


class BinaryMixin:
    def serialize_using_binary(self):
        with shelve.open('lr_files/data.bin') as items_list:
            for i in self.items_dict.keys():
                items_list[i] = self.items_dict[i]


    def deserialize_using_binary(self):
        with shelve.open('lr_files/data.bin') as items_list:
            items_dict = dict()

            for i in sorted(items_list):
                items_dict.update({i: items_list[i]})

        return items_dict
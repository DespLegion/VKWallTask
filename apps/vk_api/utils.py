

class ADictMeta(type):
    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)


class Adict(metaclass=ADictMeta):
    pass


def fill_adict_from_dict(input_dict):
    val_flag = False
    if len(input_dict) != 0:
        keys = input_dict.keys()
        for key in keys:
            Adict[key] = input_dict[key]
            val_flag = True
    if val_flag:
        return Adict

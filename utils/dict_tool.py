from collections import defaultdict


class DictTool:

    @staticmethod
    def join_dicts(*args) -> defaultdict:
        dicts = []
        for _dict in args:
            if type(_dict) == dict:
                dicts.append(_dict)

        super_dict = defaultdict(set)
        for d in dicts:
            for k, v in d.items():  # use d.iteritems() in python 2
                super_dict[k].add(v)

        return super_dict

    @staticmethod
    def to_dict(super_dict: defaultdict) -> dict:
        return dict(super_dict)

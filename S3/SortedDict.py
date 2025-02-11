# -*- coding: utf-8 -*-

## Amazon S3 manager
## Author: Michal Ludvig <michal@logix.cz>
##         http://www.logix.cz/michal
## License: GPL Version 2
## Copyright: TGRMN Software and contributors

from __future__ import absolute_import, print_function

from .BidirMap import BidirMap

class SortedDictIterator(object):
    def __init__(self, sorted_dict, keys, reverse=False):
        self.sorted_dict = sorted_dict
        self.keys = keys
        if reverse:
            self.pop_index = -1
        else:
            self.pop_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.keys.pop(self.pop_index)
        except IndexError:
            raise StopIteration

    next = __next__

class SortedDict(dict):
    def __init__(self, mapping = {}, ignore_case = True, **kwargs):
        """
        WARNING: SortedDict() with ignore_case==True will
                 drop entries differing only in capitalisation!
                 Eg: SortedDict({'auckland':1, 'Auckland':2}).keys() => ['Auckland']
                 With ignore_case==False it's all right
        """
        dict.__init__(self, mapping, **kwargs)
        self.ignore_case = ignore_case

    def keys(self):
        # TODO fix
        # Probably not anymore memory efficient on python2
        # as now 2 copies of keys to sort them.
        keys = dict.keys(self)
        if self.ignore_case:
            # Translation map
            xlat_map = BidirMap()
            for key in keys:
                xlat_map[key.lower()] = key
            # Lowercase keys
            lc_keys = sorted(xlat_map.keys())
            return [xlat_map[k] for k in lc_keys]
        else:
            keys = sorted(keys)
            return keys

    def __iter__(self):
        return SortedDictIterator(self, self.keys())

    def __reversed__(self):
        return SortedDictIterator(self, self.keys(), reverse=True)

    def __getitem__(self, index):
        """Override to support the "get_slice" for python3 """
        if isinstance(index, slice):
            r = SortedDict(ignore_case = self.ignore_case)
            for k in self.keys()[index]:
                r[k] = self[k]
        else:
            r = super(SortedDict, self).__getitem__(index)
        return r


if __name__ == "__main__":
    d = { 'AWS' : 1, 'Action' : 2, 'america' : 3, 'Auckland' : 4, 'America' : 5 }
    sd = SortedDict(d)
    print("Wanted: Action, america, Auckland, AWS,    [ignore case]")
    print("Got:   ", end=' ')
    for key in sd:
        print("%s," % key, end=' ')
    print("   [used: __iter__()]")
    d = SortedDict(d, ignore_case = False)
    print("Wanted: AWS, Action, America, Auckland, america,    [case sensitive]")
    print("Got:   ", end=' ')
    for key in d.keys():
        print("%s," % key, end=' ')
    print("   [used: keys()]")

# vim:et:ts=4:sts=4:ai

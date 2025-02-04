from typing import List

import Values as v


class Person:
    name = ""
    preferences = set() # dictionary with "workshop -> prio of pref"
    friend = ""
    excluded_pref = ""
    assigned_workshops = {}

    def __init__(self, row: List[str]):
        self.name = row[1]
        self.friend = row[2]
        self.excluded_pref = row[3]
        for i in range(4):
            if i + 4 < len(row): # check if index exists
                self.preferences.add(v.HIGHEST_PREFERENCE_PRIO - i)
from typing import List
import Values as v


class Person:
    key = ""
    name = ""
    preferences = {} # dictionary with "workshop -> prio of pref"
    key_friend = ""
    excluded_pref = ""
    assigned_workshops = {}
    grouped = False

    def __init__(self, row: List[str]):
        self.key = row[0]
        self.name = row[1]
        self.key_friend = row[2]
        self.excluded_pref = row[3]
        self.grouped = False
        for i in range(v.NR_MAX_PREF):
            if i*v.SLOTS_PER_PREF + v.COLUMN_OF_FIRST_PREF < len(row): # check if index exists
                new_pref = {0: row[i * v.SLOTS_PER_PREF + v.COLUMN_OF_FIRST_PREF],
                            1: row[i * v.SLOTS_PER_PREF + v.COLUMN_OF_FIRST_PREF + 1]}
                self.preferences[i] = new_pref




from typing import List, Dict
import Values as v


class Person:
    def __init__(self, row: List[str]):
        self.key = row[v.COLUMN_OF_KEY]
        self.name = row[v.COLUMN_OF_NAME]
        self.key_friend = row[v.COLUMN_OF_KEY_FRIEND]
        self.excluded_pref = [v.COLUMN_OF_EXCLUDE_PRIO]
        # TODO: save other information about person
        self.other: str = ""
        self.grouped = False
        self.preferences = {} # dictionary with "workshop -> prio of pref"
        for i in range(v.NR_MAX_PREF):
            if i*v.SLOTS_PER_PREF + v.COLUMN_OF_FIRST_PREF < len(row): # check if index exists
                new_pref = {0: row[i * v.SLOTS_PER_PREF + v.COLUMN_OF_FIRST_PREF],
                            1: row[i * v.SLOTS_PER_PREF + v.COLUMN_OF_FIRST_PREF + 1]}
                self.preferences[i] = new_pref
        self.assigned_workshops: Dict[str, str] = {}

    def assign_to_workshop(self, slot: str, workshop_key: str):
        self.assigned_workshops[slot] = workshop_key

    def is_fully_assigned(self):
        if v.LAST_WORKSHOP_TIMESLOT in self.assigned_workshops:
            return True
        if len(self.assigned_workshops) == len(v.WORKSHOP_POSSIBLE_TIMESLOTS) - 1:
            return True
        return False

    def get_unassigned_slot(self) -> str:
        if len(self.assigned_workshops) == 0:
            return v.LAST_WORKSHOP_TIMESLOT
        for key in v.WORKSHOP_POSSIBLE_TIMESLOTS.keys():
            if not key in self.assigned_workshops:
                return key
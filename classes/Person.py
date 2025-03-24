from typing import List, Dict
import Values as v


class Person:
    def __init__(self, row: List[str]):
        self.key:str = row[v.COLUMN_OF_KEY]
        self.name = row[v.COLUMN_OF_NAME]
        self.key_friend: str = row[v.COLUMN_OF_KEY_FRIEND]
        self.information: str = row[v.COLUMN_OF_INFORMATION]
        self.excluded_pref = row[v.COLUMN_OF_EXCLUDE_PRIO]
        self.preferences: List[Dict] = [None] * v.NR_MAX_PREF # list with preferences[prio of pref] -> workshop["workshop_name(s)"]
        for i in range(v.NR_MAX_PREF):
            new_pref = {}
            for j in range(v.SLOTS_PER_PREF):
                #if not row[i * v.SLOTS_PER_PREF + v.COLUMN_OF_FIRST_PREF + j] is None:
                new_pref[v.WORKSHOP_TIMESLOT_NAMES[j]] = row[i * v.SLOTS_PER_PREF + v.COLUMN_OF_FIRST_PREF + j]
            if not new_pref["b"]:
                new_pref.clear()
                new_pref[v.LAST_WORKSHOP_TIMESLOT] = row[i * v.SLOTS_PER_PREF + v.COLUMN_OF_FIRST_PREF]
            self.preferences[i] = new_pref
        # relevant information for allocation process
        self.grouped = False
        self.assigned_workshops: Dict[str, str] = {}

    def assign_to_workshop(self, slot: str, workshop_key: str):
        self.assigned_workshops[slot] = workshop_key

    def is_fully_assigned(self):
        if v.LAST_WORKSHOP_TIMESLOT in self.assigned_workshops:
            return True
        if len(self.assigned_workshops) == len(v.WORKSHOP_POSSIBLE_TIMESLOTS) - 1:
            return True
        return False

    def get_unassigned_slot(self):
        if len(self.assigned_workshops) == 0:
            return v.LAST_WORKSHOP_TIMESLOT
        for key in v.WORKSHOP_POSSIBLE_TIMESLOTS.keys():
            if not key in self.assigned_workshops:
                return key

    def get_if_promotable(self):
        first_prio = {}
        for key in self.preferences[0].keys():
            first_prio[key] = self.preferences[0][key]
        if self.assigned_workshops == first_prio:
            return False
        return True

    def cut_unused_wishes(self):
        for key_assigned in self.assigned_workshops.keys():
            delete = False
            for i in range(len(self.assigned_workshops)):
                if key_assigned in self.preferences[i]:
                    if delete:
                        del self.preferences[i][key_assigned]
                    elif self.preferences[i][key_assigned] == self.assigned_workshops[key_assigned]:
                        delete = True
                        del self.preferences[i][key_assigned]
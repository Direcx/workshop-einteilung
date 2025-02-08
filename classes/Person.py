from typing import List, Dict
import Values as v


class Person:
    def __init__(self, row: List[str]):
        self.key = row[0]
        self.name = row[1]
        self.key_friend = row[2]
        self.excluded_pref = row[3]
        # TODO: save other information about person
        self.other: str = ""
        self.grouped = False
        self.preferences = {} # dictionary with "workshop -> prio of pref"
        for i in range(v.NR_MAX_PREF):
            if i*v.SLOTS_PER_PREF + v.COLUMN_OF_FIRST_PREF < len(row): # check if index exists
                # print(f"{i} * {v.SLOTS_PER_PREF} + {v.COLUMN_OF_FIRST_PREF} is in row {row[i * v.SLOTS_PER_PREF + v.COLUMN_OF_FIRST_PREF]}")
                new_pref = {0: row[i * v.SLOTS_PER_PREF + v.COLUMN_OF_FIRST_PREF],
                            1: row[i * v.SLOTS_PER_PREF + v.COLUMN_OF_FIRST_PREF + 1]}
                self.preferences[i] = new_pref
        self.assigned_workshops: Dict[str, str] = {}

    def assign_to_workshop(self, slot: str, workshop_key: str):
        self.assigned_workshops[slot] = workshop_key

    def is_fully_assigned(self):
        if v.WORKSHOP_POSSIBLE_TIMESLOTS[0] in self.assigned_workshops:
            if v.WORKSHOP_POSSIBLE_TIMESLOTS[1] in self.assigned_workshops:
                return True
        if v.WORKSHOP_POSSIBLE_TIMESLOTS[2] in self.assigned_workshops:
            return True
        return False

    def get_unassigned_slots(self):
        free_slots = []
        if not v.WORKSHOP_POSSIBLE_TIMESLOTS[0] in self.assigned_workshops:
            if not v.WORKSHOP_POSSIBLE_TIMESLOTS[1] in self.assigned_workshops:
                free_slots.append(v.WORKSHOP_POSSIBLE_TIMESLOTS[2])
                return free_slots
            else:
                free_slots.append(v.WORKSHOP_POSSIBLE_TIMESLOTS[0])
        if not v.WORKSHOP_POSSIBLE_TIMESLOTS[1] in self.assigned_workshops:
            free_slots.append(v.WORKSHOP_POSSIBLE_TIMESLOTS[1])
        return free_slots
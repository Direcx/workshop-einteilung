from typing import List, Dict, Tuple
import Values as v


class Workshop:
    def __init__(self, row:List[str]):
        self.key:str = row[v.COLUMN_WS_KEY]
        self.name = row[v.COLUMN_WS_NAME]
        self.information = int(v.COLUMN_WS_INFORMATION) # relevant for timeslot, decides how many timeslots this workshop uses
        self.slots = int(row[v.COLUMN_WS_SLOTS])
        self.timeslot = row[v.COLUMN_WS_TIMESLOT] # decides on which timeslot the workshop is held
        self.processed = False
        self.assigned_persons: List[str] = []
        self.number_pre_assigned = 0
        self.pre_assigned_groups: Dict[str, Tuple[int, int]]  = {} # [key_group] = [pref_rank, group_size]

    def pre_assign(self, group_key: str, group_size: int, pref_rank: int):
        pref_of_group = pref_rank, group_size
        self.pre_assigned_groups[group_key] = pref_of_group
        self.number_pre_assigned += group_size
        return self

    def assign(self, key_person: str):
        if not self.processed:
            self.assigned_persons.append(key_person)
            if len(self.assigned_persons) == self.slots:
                self.processed = True
        else:
            print("tried to assign but workshop is already full")

    def get_pre_assigned_groups(self):
        return self.pre_assigned_groups

    def process(self):
        self.processed = True
        return self

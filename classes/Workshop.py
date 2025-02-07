from typing import List, Dict, Tuple
import Values as v


class Workshop:
    def __init__(self, row:List[str]):
        self.key:str = row[0]
        self.name = row[1]
        self.weight = int(row[2]) # relevant for timeslot, decides how many timeslots this workshop uses
        self.slots = int(row[3])
        self.timeslot = row[4] # decides on which timeslot the workshop is held
        self.processed = False
        self.assigned_persons: List[str] = []
        self.number_pre_assigned = 0
        self.pre_assigned_groups: Dict[str, Tuple[int, int]]  = {} # [key_group] = [pref_rank, group_size]

    def pre_assign(self, group_key: str, group_size: int, pref_rank: int):
        pref_of_group = pref_rank, group_size
        self.pre_assigned_groups[group_key] = pref_of_group
        # print(f"assigned {group_key} with {pref_of_group} to {self.key} with pre_assigned: {self.pre_assigned_groups}")
        self.number_pre_assigned += group_size
        # print(f"added {group_size} to now {self.number_pre_assigned}")
        return self

    def assign(self, key_person: str):
        if len(self.assigned_persons) <= self.slots:
            self.assigned_persons.append(key_person)
            if len(self.assigned_persons) == self.slots:
                self.processed = True
        elif v.LOG:
            print(f"tried to assign Person to workshop {self.name} but {len(self.assigned_persons)} ==? {self.slots}")

    def get_pre_assigned_groups(self):
        return self.pre_assigned_groups

    def process(self):
        self.processed = True
        return self

from typing import List, Dict, Tuple


class Workshop:
    key = ""
    name = ""
    weight = 0 # relevant for timeslot
    slots = ""
    processed = False
    assigned_persons: List[str] = []
    pre_assigned_groups: List[Tuple[int, int, str]] = []
    number_pre_assigned = 0

    def __init__(self, row:List[str]):
        self.key = row[0]
        self.name = row[1]
        self.weight = int(row[2])
        self.slots = row[3]
        self.number_pre_assigned = 0

    def pre_assign(self, group_key: str, group_size, pref_rank):
        pref_of_group = len(self.pre_assigned_groups), pref_rank, group_key
        self.pre_assigned_groups.append(pref_of_group)
        print(f"assigned {pref_of_group} to {self.pre_assigned_groups}")
        self.number_pre_assigned += group_size
        print(f"added {group_size} to now {self.number_pre_assigned}")

    def assign(self, key_person: str):
        self.assigned_persons[len(self.assigned_persons)] = key_person

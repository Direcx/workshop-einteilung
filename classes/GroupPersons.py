from typing import Dict, List
from classes.Person import Person


class GroupPersons:
    def __init__(self, key):
        self.number_persons = 0
        self.persons: Dict[str, Person] = {}
        self.key = key

    def add_person(self, person: Person):
        self.persons[person.key] = person
        self.number_persons += 1

    def get_first_person(self):
        return list(self.persons)[0]

    def get_all_persons(self):
        return self.persons

    def get_all_persons_names(self):
        names_string = ""
        for key in self.persons.keys():
            names_string += self.persons[key].name
            names_string += " "
        return names_string

    def assign_persons(self, workshop_key: str, timeslot: int, persons: Dict[str, Person]):
        if timeslot == 1:
            for key in self.persons.keys():
                persons[key].assigned_workshops[timeslot - 1] = workshop_key
        elif timeslot == 2:
            for key in self.persons.keys():
                persons[key].assigned_workshops[timeslot - 3] = workshop_key
                persons[key].assigned_workshops[timeslot - 2] = workshop_key

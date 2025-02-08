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


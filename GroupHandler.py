from typing import Dict
from classes.Person import Person
import Values as v
from classes.GroupPersons import GroupPersons


# results of convert to groups:
# grouped_persons
# TODO: put persons, groups, workshops in global variables and put setter methode for those

def convert_persons_to_groups(persons: Dict[str, Person]) -> Dict[str, GroupPersons]:
    groups: dict[str, GroupPersons] = {}
    for key in persons.keys():
        if persons[key].grouped:
            continue
        group_size = check_group_size(persons, persons[key].key)
        if group_size > 1:
            groups, persons = add_group_multi_persons(groups, persons, key)
        else:
            new_group = GroupPersons(len(groups))
            new_group.add_person(persons[key])
            groups[str(len(groups))] = new_group
    return groups


def check_group_size(persons: Dict[str, Person], key_to_check: str):
    key_start = key_to_check
    key_current = persons[key_start].key_friend
    for i in range(0, v.MAX_GROUP_SIZE):
        if key_current == "0":
            return 1
        if key_current == key_start:
            return i + 1
        else:
            key_current = persons[key_current].key_friend
    return -1


def add_group_multi_persons(groups, persons: Dict[str, Person], person_key):
    new_group = GroupPersons(len(groups))
    start_key = person_key

    # adding first person of group
    new_group.add_person(persons[start_key])
    persons[start_key].grouped = True

    current_key = persons[start_key].key_friend
    while start_key != current_key:
        new_group.add_person(persons[current_key])
        persons[current_key].grouped = True
        current_key = persons[current_key].key_friend
    groups[len(groups)] = new_group
    return groups, persons


def get_group_preferences(group: GroupPersons, persons: Dict[str, Person]):
    preferences = persons[group.get_first_person()].preferences
    return preferences

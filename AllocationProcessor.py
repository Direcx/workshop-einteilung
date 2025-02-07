from classes.GroupPersons import GroupPersons
from classes.Person import Person
from classes.Workshop import Workshop
from typing import Dict, List
import random
import Values as v
import GroupHandler as gh


#done pre-assign groups to all workshops
#done get list of all unprocessed workshops
#done start with workshop with the fewest assigned groups:
    #done sort pre-assigned groups by preference for workshop
    #- for each preference
        #- check if enough slots for groups
        #- if yes assign, if not randomize the assigning
    #- cross off the assigned groups from the other pre-assigned workshops
# repeat process until all workshops with assigned people are processed
# if groups not assigned create new workshop "not assigned" and assign the groups
# return all workshops and groups


def pre_assign_groups(groups: Dict[str, GroupPersons], workshops: Dict[str, Workshop], persons: Dict[str, Person]):
    for key in groups.keys(): # iteration through all groups
        preferences_group = gh.get_group_preferences(groups[key], persons)
        for i in range(v.NR_MAX_PREF):
            # TODO: only assign if not already assigned to workshop
            workshops[preferences_group[i][0]] = workshops[preferences_group[i][0]].pre_assign(
                key, groups[key].number_persons, v.HIGHEST_PREFERENCE_PRIO - i)
            workshops[preferences_group[i][1]] = workshops[preferences_group[i][1]].pre_assign(
                key, groups[key].number_persons, v.HIGHEST_PREFERENCE_PRIO - i)
    return groups, workshops

def get_workshop_least_pre_assigned(workshops: Dict[str, Workshop], persons: Dict[str, Person]) -> str:
    lowest_subs = len(persons)
    for key in workshops.keys():
        if workshops[key].number_pre_assigned < lowest_subs:
            lowest_subs = workshops[key].number_pre_assigned
    for key in workshops.keys():
        if workshops[key].number_pre_assigned == lowest_subs:
            return key
    return ""

def get_unprocessed_workshops(workshops: Dict[str, Workshop]) -> Dict[str, Workshop]:
    unprocessed_workshops = {}
    for key in workshops.keys():
        if not workshops[key].processed:
            unprocessed_workshops[key] = workshops[key]
    return unprocessed_workshops

def get_sorted_pre_assigned_to_workshop(workshop: Workshop):
    sorted_groups: List[List[str]] = []
    for i in range(v.NR_MAX_PREF):
        sorted_groups.append([])
    for i in range(v.NR_MAX_PREF):
        for key in workshop.get_pre_assigned_groups():
            if workshop.get_pre_assigned_groups()[key][0] == v.HIGHEST_PREFERENCE_PRIO - i:
                sorted_groups[i].append(key)
    return sorted_groups

def check_space_for_pref_rank(sorted_groups: List[List[str]], prio_rank: int, workshops: Dict[str, Workshop], workshop_key):
    return len(sorted_groups[prio_rank]) <= workshops[workshop_key].slots - len(workshops[workshop_key].assigned_persons)

def assign_single_group(persons: Dict[str, Person], workshop: Workshop, group: GroupPersons):
    for person in group.persons.keys():
        workshop.assign(person)
        persons[person].assign_to_workshop(workshop.timeslot-1, workshop.key)
    return persons, group, workshop

def assign_random_groups(workshop: Workshop, ranked_groups: List[str]):
    # TODO: pick random groups and dont overshoot the limit of the workshop slots
    slots_available = workshop.slots - len(workshop.assigned_persons)
    assigned = random.sample(list(ranked_groups), slots_available)
    return assigned

def cross_off_assigned_group(group: str, workshops: Dict[str, Workshop]):
    # TODO: cross off from right part of workshops
    for workshop_key in workshops.keys():
        # print(f"{workshops[workshop_key].pre_assigned_groups}")
        if group in workshops[workshop_key].pre_assigned_groups:
            del workshops[workshop_key].pre_assigned_groups[group]

def get_unassigned_persons(persons: Dict[str, Person]):
    unassigned_persons = {}
    for person_key in persons.keys():
        if len(persons[person_key].assigned_workshops) == 0:
            unassigned_persons[person_key] = persons[person_key]
    return unassigned_persons

def assign_rest(unassigned_persons: Dict[str, Person]):
    no_workshop = Workshop(["null", "No Workshop", 1, 1, len(unassigned_persons)])
    for key in unassigned_persons.keys():
        unassigned_persons[key].assign_to_workshop(1, no_workshop.key)
        unassigned_persons[key].assign_to_workshop(2, no_workshop.key)
        no_workshop.assign(key)
    return no_workshop, unassigned_persons


def assign_main(groups: Dict[str, GroupPersons], workshops: Dict[str, Workshop], persons: Dict[str, Person]):
    empty_pre_assigned_groups: List[List[str]] = []
    for i in range(v.NR_MAX_PREF):
        empty_pre_assigned_groups.append([])
    while len(get_unprocessed_workshops(workshops)) > 0:
        #print(f"unprocessed Workshops: {get_unprocessed_workshops(workshops)}")
        least_pre_assigned_workshop = get_workshop_least_pre_assigned(get_unprocessed_workshops(workshops), persons)
        #print(f"least_pre_assigned_workshop: {workshops[least_pre_assigned_workshop].name}")
        sorted_pre_assigned_groups = get_sorted_pre_assigned_to_workshop(workshops[least_pre_assigned_workshop])
        #print(f"sorted groups: {sorted_pre_assigned_groups}")
        if sorted_pre_assigned_groups == empty_pre_assigned_groups:
            workshops[least_pre_assigned_workshop].process()
            continue
        for i in range(v.NR_MAX_PREF):
            if not sorted_pre_assigned_groups[i]:
                continue
            elif check_space_for_pref_rank(sorted_pre_assigned_groups, i, workshops, least_pre_assigned_workshop):
                for j in range(len(sorted_pre_assigned_groups[i])):
                    persons, group, workshop = assign_single_group(
                        persons, workshops[least_pre_assigned_workshop], groups[sorted_pre_assigned_groups[i][j]])
                    cross_off_assigned_group(sorted_pre_assigned_groups[i][j], workshops)
            else:
                random_assigned_persons = assign_random_groups(workshops[least_pre_assigned_workshop], sorted_pre_assigned_groups[i])
                for j in range(len(random_assigned_persons)):
                    cross_off_assigned_group(random_assigned_persons[j], workshops)

    unassigned_persons = get_unassigned_persons(persons)
    if len(unassigned_persons) > 0:
        workshops["null"], unassigned_persons = assign_rest(unassigned_persons)
    return groups, workshops, persons

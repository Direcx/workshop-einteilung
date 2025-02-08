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
groups: Dict[str, GroupPersons] = {}
workshops: Dict[str, Workshop] = {}
persons: Dict[str, Person] = {}


def set_variables(i_groups: Dict[str, GroupPersons], i_workshops: Dict[str, Workshop], i_persons: Dict[str, Person]):
    global groups  # access global variables
    global workshops
    global persons

    groups = i_groups  # make sure the global variables are set right
    workshops = i_workshops
    persons = i_persons


def pre_assign_groups():
    global groups  # access global variables
    global workshops
    global persons
    for key in groups.keys(): # iteration through all groups
        preferences_group = gh.get_group_preferences(groups[key], persons)
        for i in range(v.NR_MAX_PREF):
            # TODO: only assign if not already assigned to workshop
            workshops[preferences_group[i][0]] = workshops[preferences_group[i][0]].pre_assign(
                key, groups[key].number_persons, v.HIGHEST_PREFERENCE_PRIO - i)
            workshops[preferences_group[i][1]] = workshops[preferences_group[i][1]].pre_assign(
                key, groups[key].number_persons, v.HIGHEST_PREFERENCE_PRIO - i)
    return groups, workshops


def get_workshop_least_pre_assigned(unprocessed_workshops: List[str]) -> str:
    global persons
    global workshops
    lowest_subs = len(persons)
    for i in range(len(unprocessed_workshops)):
        if workshops[unprocessed_workshops[i]].number_pre_assigned < lowest_subs:
            lowest_subs = workshops[unprocessed_workshops[i]].number_pre_assigned
    for key in workshops.keys():
        if workshops[key].number_pre_assigned == lowest_subs and not workshops[key].processed:
            return key
    return ""

# TODO: make it depending on timeslots
def get_unprocessed_workshops() -> List[str]:
    global workshops
    unprocessed_workshops = []
    for key in workshops.keys():
        if not workshops[key].processed:
            #print(f"key added: {key}")
            unprocessed_workshops.append(key)
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


def check_space_for_pref_rank(sorted_groups: List[List[str]], prio_rank: int, workshop: Workshop):
    global groups
    persons_in_rank = 0
    for i in range(len(sorted_groups[prio_rank])):
        persons_in_rank += groups[sorted_groups[prio_rank][i]].number_persons
    if v.LOG:
        print(f"while checking for space in {workshop.name} there are {persons_in_rank} persons in rank and "
              f"{workshop.slots - len(workshop.assigned_persons)} available slots found")
    return persons_in_rank <= workshop.slots - len(workshop.assigned_persons)


def assign_single_group(workshop_key: str, group: GroupPersons):
    global persons
    global workshops
    for person in group.persons.keys():
        workshops[workshop_key].assign(person)
        persons[person].assign_to_workshop(workshops[workshop_key].timeslot, workshop_key)
    return persons, group, workshop_key

#TODO: take care of situation where last slots in workshop could be taken by group and filled to maximum
def assign_random_groups(workshop: Workshop, ranked_groups: List[str]):
    global groups
    global persons
    slots_available = workshop.slots - len(workshop.assigned_persons)
    groups_sample = ranked_groups
    assigned: List[str] = []
    if v.LOG:
        print(f"available slots: {slots_available} with length of list of groups: {len(ranked_groups)}")
    while len(groups_sample) > 0:
        random_group = random.choice(groups_sample)
        if groups[random_group].number_persons <= slots_available:
            assign_single_group(workshop.key, groups[random_group])
            assigned.append(random_group)
            slots_available -= groups[random_group].number_persons
            cross_off_assigned_group(random_group, workshop.timeslot)
        else:
            cross_off_from_specific_workshop(random_group, workshop.key)
        groups_sample.remove(random_group)
    return assigned


def cross_off_assigned_group(group: str, timeslot: str):
    global workshops
    for workshop_key in workshops.keys():
        if group in workshops[workshop_key].pre_assigned_groups and check_possible_timeslots(workshop_key, timeslot):
            del workshops[workshop_key].pre_assigned_groups[group]


def cross_off_from_specific_workshop(group:str, workshop:str):
    global workshops
    del workshops[workshop].pre_assigned_groups[group]


def check_possible_timeslots(key_workshop: str, timeslot: str):
    global workshops
    if timeslot == v.WORKSHOP_POSSIBLE_TIMESLOTS[2]:
        return True
    elif workshops[key_workshop].timeslot == timeslot:
       return True
    return False


def get_not_fully_assigned_persons():
    global persons
    not_fully_assigned_persons = []
    for person_key in persons.keys():
        if not persons[person_key].is_fully_assigned():
            not_fully_assigned_persons.append(person_key)
    return not_fully_assigned_persons


def assign_rest(unassigned_persons: List[str]):
    global persons
    global workshops
    for timeslot in v.WORKSHOP_POSSIBLE_TIMESLOTS:
        workshops[timeslot] = Workshop([f"{timeslot}", f"No Workshop at timeslot {timeslot}", 1,len(persons), timeslot])
    for i in range(len(unassigned_persons)):
        list_unassigned_slots = persons[unassigned_persons[i]].get_unassigned_slots()
        for slot in list_unassigned_slots:
            persons[unassigned_persons[i]].assign_to_workshop(slot, slot)
            workshops[slot].assign(unassigned_persons[i])


def assign_main():
    global groups
    global workshops
    global persons

    # get reference to decide if a workshop has no pre-assigned groups
    empty_pre_assigned_groups: List[List[str]] = []
    for i in range(v.NR_MAX_PREF):
        empty_pre_assigned_groups.append([])

    # assign groups/persons to workshops
    # TODO: make it depending on timeslots of workshops
    while len(get_unprocessed_workshops()) > 0:
        least_pre_assigned_workshop = get_workshop_least_pre_assigned(get_unprocessed_workshops())
        sorted_pre_assigned_groups = get_sorted_pre_assigned_to_workshop(workshops[least_pre_assigned_workshop])
        if sorted_pre_assigned_groups == empty_pre_assigned_groups:
            workshops[least_pre_assigned_workshop] = workshops[least_pre_assigned_workshop].process()
            continue
        for i in range(v.NR_MAX_PREF):
            if not sorted_pre_assigned_groups[i]:
                continue
            elif check_space_for_pref_rank(sorted_pre_assigned_groups, i, workshops[least_pre_assigned_workshop]):
                for j in range(len(sorted_pre_assigned_groups[i])):
                    assign_single_group(least_pre_assigned_workshop,
                                        groups[sorted_pre_assigned_groups[i][j]])
                    cross_off_assigned_group(sorted_pre_assigned_groups[i][j],
                                        workshops[least_pre_assigned_workshop].timeslot)
            else:
                assign_random_groups(workshops[least_pre_assigned_workshop], sorted_pre_assigned_groups[i])
    # assign the not fully/at all assigned persons to phantom workshops to be easily sorted out/taken care of afterward
    # TODO: assign the rest to similar workshops as the preferred ones
    not_fully_assigned_persons = get_not_fully_assigned_persons()
    if len(not_fully_assigned_persons) > 0:
        assign_rest(not_fully_assigned_persons)
    return groups, workshops, persons

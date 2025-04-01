from classes.GroupPersons import GroupPersons
from classes.Person import Person
from classes.Workshop import Workshop
from typing import Dict, List
import random
import Values as Val
import GroupHandler as gh


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
        for i in range(Val.NR_MAX_PREF):
            # TODO: only assign if not already assigned to workshop
            for pref in preferences_group[i]:
                if not preferences_group[i][pref] is None:
                    workshops[preferences_group[i][pref]].pre_assign(
                        key, groups[key].number_persons, Val.HIGHEST_PREFERENCE_PRIO - i)
    return groups, workshops

def set_assign_probability_factor():
    global persons
    global groups
    global workshops

    for group in groups.keys():
        factor_sum = 0.0
        first_person = groups[group].get_first_person()
        for i in range(Val.NR_MAX_PREF):
            if Val.LAST_WORKSHOP_TIMESLOT in persons[first_person].preferences[i].keys():
                workshop_pref = persons[first_person].preferences[i][Val.LAST_WORKSHOP_TIMESLOT]
                factor_sum += 2 * (workshops[workshop_pref].slots / workshops[workshop_pref].number_pre_assigned)
            else:
                for j in range(Val.SLOTS_PER_PREF):
                    workshop_pref = persons[first_person].preferences[i][Val.WORKSHOP_TIMESLOT_NAMES[j]]
                    factor_sum += workshops[workshop_pref].slots / workshops[workshop_pref].number_pre_assigned
        for key in groups[group].persons.keys():
            probability_factor = factor_sum/(Val.SLOTS_PER_PREF*Val.NR_MAX_PREF)
            persons[key].set_assign_probability(probability_factor)

def get_unprocessed_workshops() -> List[str]:
    global workshops
    unprocessed_workshops = []
    for key in workshops.keys():
        if not workshops[key].processed:
            unprocessed_workshops.append(key)
    return unprocessed_workshops

def get_workshops_with_highest_assign_prio(unprocessed_workshops: List[str]) -> List[str]:
    global workshops
    highest_prio_nr = 0
    highest_prio_timeslot = ""
    highest_assign_prio_workshops = []
    for i in range(len(unprocessed_workshops)):
        if Val.WORKSHOP_POSSIBLE_TIMESLOTS[workshops[unprocessed_workshops[i]].timeslot] > highest_prio_nr:
            highest_prio_nr = Val.WORKSHOP_POSSIBLE_TIMESLOTS[workshops[unprocessed_workshops[i]].timeslot]
            highest_prio_timeslot = workshops[unprocessed_workshops[i]].timeslot
    for i in range(len(unprocessed_workshops)):
        if workshops[unprocessed_workshops[i]].timeslot == highest_prio_timeslot:
            highest_assign_prio_workshops.append(unprocessed_workshops[i])
    return highest_assign_prio_workshops

def get_workshop_least_pre_assigned(unprocessed_workshops: List[str]) -> str:
    global persons
    global workshops
    lowest_subs = len(persons)
    for i in range(len(unprocessed_workshops)):
        wanted_factor = workshops[unprocessed_workshops[i]].number_pre_assigned/workshops[unprocessed_workshops[i]].slots
        if wanted_factor < lowest_subs:
            lowest_subs = wanted_factor
    for key in workshops.keys():
        wanted_factor = workshops[key].number_pre_assigned / workshops[key].slots
        if wanted_factor == lowest_subs and not workshops[key].processed:
            return key
    return ""

def get_sorted_pre_assigned_to_workshop(workshop: Workshop):
    sorted_groups: List[List[str]] = []
    for i in range(Val.NR_MAX_PREF):
        sorted_groups.append([])
    for i in range(Val.NR_MAX_PREF):
        for key in workshop.get_pre_assigned_groups():
            if workshop.get_pre_assigned_groups()[key][0] == Val.HIGHEST_PREFERENCE_PRIO - i:
                sorted_groups[i].append(key)
    return sorted_groups

def check_space_for_pref_rank(sorted_groups: List[List[str]], prio_rank: int, workshop: Workshop):
    global groups
    persons_in_rank = 0
    for i in range(len(sorted_groups[prio_rank])):
        persons_in_rank += groups[sorted_groups[prio_rank][i]].number_persons
    return persons_in_rank <= workshop.slots - len(workshop.assigned_persons)

def assign_single_group(workshop_key: str, group: GroupPersons):
    global persons
    global workshops
    for person in group.persons.keys():
        workshops[workshop_key].assign(person)
        persons[person].assign_to_workshop(workshops[workshop_key].timeslot, workshop_key)
    return persons, group, workshop_key

def assign_random_groups(workshop: Workshop, ranked_groups: List[str]):
    global groups
    global persons
    slots_available = workshop.slots - len(workshop.assigned_persons)
    groups_sample = ranked_groups

    assigned: List[str] = []
    while slots_available > Val.MAX_GROUP_SIZE * 2:
        diff_groups = search_most_difficult_assigning_groups(groups_sample)
        random_group = random.choice(diff_groups)
        assign_single_group(workshop.key, groups[random_group])
        assigned.append(random_group)
        slots_available -= groups[random_group].number_persons
        cross_off_global_assigned_group(random_group, workshop.timeslot)
        groups_sample.remove(random_group)
    while len(groups_sample) > 0:
        diff_groups = search_most_difficult_assigning_groups(groups_sample)
        largest_groups = get_largest_groups(diff_groups)
        random_group = random.choice(largest_groups)
        if groups[random_group].number_persons <= slots_available:
            assign_single_group(workshop.key, groups[random_group])
            assigned.append(random_group)
            slots_available -= groups[random_group].number_persons
            cross_off_global_assigned_group(random_group, workshop.timeslot)
        else:
            cross_off_specific_workshop(random_group, workshop.key)
        groups_sample.remove(random_group)
    return assigned

def get_largest_groups(sample_list: List[str]) -> List[str]:
    global groups
    groups_largest_size = []
    largest_group_size = 0
    for i in range(len(sample_list)):
        if groups[sample_list[i]].number_persons > largest_group_size:
            largest_group_size = groups[sample_list[i]].number_persons
    for i in range(len(sample_list)):
        if groups[sample_list[i]].number_persons == largest_group_size:
            groups_largest_size.append(sample_list[i])
    return groups_largest_size

def search_most_difficult_assigning_groups(group_sample:List[str]):
    global groups
    global persons
    most_difficult_assigning_groups:List[str] = []
    lowest_prob = persons[groups[group_sample[0]].get_first_person()].get_assign_probability()
    for i in range(len(group_sample)):
        prob = persons[groups[group_sample[0]].get_first_person()].get_assign_probability()
        if prob < lowest_prob:
            lowest_prob = prob
    for i in range(len(group_sample)):
        prob = persons[groups[group_sample[0]].get_first_person()].get_assign_probability()
        if prob == lowest_prob:
            most_difficult_assigning_groups.append(group_sample[i])
    return most_difficult_assigning_groups


def cross_off_global_assigned_group(group: str, timeslot: str):
    global workshops
    for workshop_key in workshops.keys():
        possible_timeslot = False
        if timeslot == Val.LAST_WORKSHOP_TIMESLOT:
            possible_timeslot = True
        elif workshops[workshop_key].timeslot == timeslot:
            possible_timeslot = True
        if group in workshops[workshop_key].pre_assigned_groups and possible_timeslot:
            del workshops[workshop_key].pre_assigned_groups[group]

def cross_off_specific_workshop(group:str, workshop:str):
    global workshops
    del workshops[workshop].pre_assigned_groups[group]

def assign_unassigned_persons():
    global persons
    global workshops
    not_fully_assigned_persons = []
    for person_key in persons.keys():
        if not persons[person_key].is_fully_assigned():
            not_fully_assigned_persons.append(person_key)
    if not not_fully_assigned_persons == [None]:
        for timeslot in Val.WORKSHOP_POSSIBLE_TIMESLOTS.keys():
            workshops[timeslot] = Workshop([f"{timeslot}", f"___________{timeslot} No Workshop", 1, len(persons), timeslot])
        for i in range(len(not_fully_assigned_persons)):
            unassigned_slot = persons[not_fully_assigned_persons[i]].get_unassigned_slot()
            persons[not_fully_assigned_persons[i]].assign_to_workshop(unassigned_slot, unassigned_slot)
            workshops[unassigned_slot].assign(not_fully_assigned_persons[i])

def get_promotable_groups():
    global groups
    global persons

    promotable_groups = {}
    for group in groups.keys():
        if persons[groups[group].get_first_person()].get_if_promotable():# check if theoretically promotable:
            promotable_groups[group] = groups[group]
    return promotable_groups

def set_for_promotion():
    global groups
    global persons
    global workshops

    promotable_groups = {}
    for group in groups.keys():
        if persons[groups[group].get_first_person()].get_if_promotable():  # check if theoretically promotable:
            promotable_groups[group] = groups[group]

    for key in promotable_groups.keys(): # deleting all unnecessary wishes
        persons[groups[key].get_first_person()].cut_unused_wishes()
    return promotable_groups

def remove_from_workshop(group: str,workshop: str):
    global groups
    global persons
    global workshops

    for person in groups[group].persons.keys():
        workshops[workshop].remove_person(person)

def evaluate_score():
    global persons
    score = 0

    for key in persons.keys():
        if not persons[key].is_fully_assigned():
            if persons[key].get_unassigned_slot() == Val.LAST_WORKSHOP_TIMESLOT:
                score += 2
            else:
                score += 1
    return score

def assign_main_with_pref_rank():
    global groups
    global workshops
    global persons

    # get reference to decide if a workshop has no pre-assigned groups
    empty_pre_assigned_groups: List[List[str]] = []
    for i in range(Val.NR_MAX_PREF):
        empty_pre_assigned_groups.append([])
    # set the factor for each person for the probability of a successful assignment
    set_assign_probability_factor()

    while len(get_unprocessed_workshops()) > 0:
        highest_assign_prio_workshops = get_workshops_with_highest_assign_prio(get_unprocessed_workshops())
        least_pre_assigned_workshop = get_workshop_least_pre_assigned(highest_assign_prio_workshops)
        sorted_pre_assigned_groups = get_sorted_pre_assigned_to_workshop(workshops[least_pre_assigned_workshop])
        if sorted_pre_assigned_groups == empty_pre_assigned_groups:
            workshops[least_pre_assigned_workshop] = workshops[least_pre_assigned_workshop].process()
            continue
        for i in range(Val.NR_MAX_PREF):
            if not sorted_pre_assigned_groups[i]:
                continue
            elif check_space_for_pref_rank(sorted_pre_assigned_groups, i, workshops[least_pre_assigned_workshop]):
                for j in range(len(sorted_pre_assigned_groups[i])):
                    assign_single_group(least_pre_assigned_workshop,
                                        groups[sorted_pre_assigned_groups[i][j]])
                    cross_off_global_assigned_group(sorted_pre_assigned_groups[i][j],
                                                    workshops[least_pre_assigned_workshop].timeslot)
            else:
                assign_random_groups(workshops[least_pre_assigned_workshop], sorted_pre_assigned_groups[i])
    # assign the not fully/at all assigned persons to phantom workshops to be easily sorted out/taken care of afterward
    # TODO: assign the rest to similar workshops as the preferred ones
    assign_unassigned_persons()
    return groups, workshops, persons


def assign_main_no_pref_rank():
    global groups
    global workshops
    global persons
    # get reference to decide if a workshop has no pre-assigned groups
    empty_pre_assigned_groups: List[List[str]] = []
    for i in range(Val.NR_MAX_PREF):
        empty_pre_assigned_groups.append([])

    # set the factor for each person for the probability of a successful assignment
    set_assign_probability_factor()

    while len(get_unprocessed_workshops()) > 0:
        prio_assigning_workshops = get_workshops_with_highest_assign_prio(get_unprocessed_workshops())
        least_pre_as_workshop = get_workshop_least_pre_assigned(prio_assigning_workshops)
        pre_assigned_groups = workshops[least_pre_as_workshop].get_pre_assigned_groups_list()
        if not pre_assigned_groups:
            workshops[least_pre_as_workshop] = workshops[least_pre_as_workshop].process()
            continue
        print(f"{workshops[least_pre_as_workshop].number_pre_assigned} =?=")
        if workshops[least_pre_as_workshop].get_free_slots() >= workshops[least_pre_as_workshop].number_pre_assigned:
            for i in range(len(pre_assigned_groups)):
                assign_single_group(least_pre_as_workshop, groups[pre_assigned_groups[i]])
                cross_off_global_assigned_group(pre_assigned_groups[i], workshops[least_pre_as_workshop].timeslot)
        else:
            assign_random_groups(workshops[least_pre_as_workshop], pre_assigned_groups)

    # assign the not fully/at all assigned persons to phantom workshops to be easily sorted out/taken care of afterward
    # TODO: assign the rest to similar workshops as the preferred ones
    assign_unassigned_persons()
    print(evaluate_score())
    return groups, workshops, persons

def promote_main():
    global groups
    global workshops
    global persons

    changed_smth = True

    while changed_smth:
        changed_smth = False
        prom_groups = set_for_promotion()
        if not prom_groups == {}:
            continue

    return groups, workshops, persons

from classes.GroupPersons import GroupPersons
from classes.Person import Person
from classes.Workshop import Workshop
from typing import Dict
import Values as v
import GroupHandler as gh


# pre-assign groups to all workshops
# start with workshop with the fewest assigned groups:
    # sort pre-assigned groups by preference for workshop
    # for each preference
        # check if enough slots for groups
        # if yes assign, if not randomize the assigning
    # cross off the assigned groups from the other pre-assigned workshops
# repeat process until all workshops with assigned people are processed
# if groups not assigned create new workshop "not assigned" and assign the groups
# return all workshops and groups


def pre_assign_groups(groups: Dict[str, GroupPersons], workshops: Dict[str, Workshop], persons: Dict[str, Person]):
    for key in groups.keys(): # iteration through all groups
        print(key)
        preferences_group = gh.get_group_preferences(groups[key], persons)
        for i in range(v.NR_MAX_PREF):
            # TODO: only assign if not already assigned to workshop
            workshops[preferences_group[i][0]].pre_assign(key, groups[key].number_persons, v.HIGHEST_PREFERENCE_PRIO - i)
            workshops[preferences_group[i][1]].pre_assign(key, groups[key].number_persons, v.HIGHEST_PREFERENCE_PRIO - i)
    return groups, workshops



# assign persons their group is assigned to
# return all assigned persons
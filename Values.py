# values to define the input and its format
DATA = "Data.xlsx"
SHEET1 = "Persons"
SHEET2 = "Workshops"
OUTPUT_FILE = "Data_processed.xlsx"


# person
E_COL_KEY = "ID"
COLUMN_OF_KEY = 0 # counts are info-style
COLUMN_OF_NAME = 1
COLUMN_OF_INFORMATION = 2
COLUMN_OF_KEY_FRIEND = 3
EMPTY_FRIEND_KEY = None
COLUMN_OF_EXCLUDE_PRIO = 4
COLUMN_OF_FIRST_PREF = 5
NR_MAX_PREF = 2
SLOTS_PER_PREF = 2 # slots or columns

# workshop
COLUMN_WS_KEY = 0 # counts are info-style
COLUMN_WS_NAME = 1
COLUMN_WS_INFORMATION = 2
COLUMN_WS_SLOTS = 3
COLUMN_WS_TIMESLOT = 4

LAST_WORKSHOP_TIMESLOT = "c"
WORKSHOP_POSSIBLE_TIMESLOTS = {"a" : 1, "b" : 1, LAST_WORKSHOP_TIMESLOT : 2}


# values for the algorithm
HIGHEST_PREFERENCE_PRIO = NR_MAX_PREF
MAX_GROUP_SIZE = 3
# values to define the input and its format
# person
COLUMN_OF_KEY = 0 # counts are info-style
COLUMN_OF_NAME = 1
COLUMN_OF_KEY_FRIEND = 2
COLUMN_OF_EXCLUDE_PRIO = 3
COLUMN_OF_FIRST_PREF = 4
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

excel_data = """
    header
1	Person1	2	X	A	A2	B	B2
2	Person2	1	X	A	A2	B	B2
3	Person3	4	X	A	A2	B	B2
4	Person4	5	X	A	A2	B	B2
5	Person5	3	X	A	A2	B	B2
6	Person6	0	X	A	A2	B	B2
"""

workshop_data = """
key name weight slots timeslot
A	A	1	3	a
B	B	1	3	a
C	C	1	3	c
A2	A2	1	5	b
B2	B2	1	0	b
"""
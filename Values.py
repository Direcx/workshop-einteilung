HIGHEST_PREFERENCE_PRIO = 10
PRIORITY_SCORES = [4, 3, 2, 1]
EXCLUDE = [1]
WORKSHOP_POSSIBLE_TIMESLOTS = ["a", "b", "c"]

STARTING_NR_FOR_KEYS = 1 #normal counted
COLUMN_OF_FIRST_PREF = 4 #info counted
NR_MAX_PREF = 2
SLOTS_PER_PREF = 2

LOG = False


GROUP_SIZE = 3

WORKSHOP_CAPACITIES = {
    "A" : 3,
    "B" : 3,
    "C" : 2,
    "D" : 3
}

excel_data = """
    header
1	Person1	2	X	A	A2	B	B2
2	Person2	1	X	A	A2	B	B2
3	Person3	4	X	A	A2	B	B2
4	Person4	5	X	A	A2	B	B2
5	Person5	3	X	A	A2	B	B2
6	Person6	0	X	B	A2	C	B2
"""

workshop_data = """
key name weight slots timeslot
A	A	1	3	a
B	B	1	3	a
C	C	1	0	a
A2	A2	1	10	b
B2	B2	1	10	b
"""
HIGHEST_PREFERENCE_PRIO = 10
PRIORITY_SCORES = [4, 3, 2, 1]
EXCLUDE = [1]
WORKSHOP_POSSIBLE_TIMESLOTS = ["a", "b", "c"]

STARTING_NR_FOR_KEYS = 1 #normal counted
COLUMN_OF_FIRST_PREF = 4 #info counted
NR_MAX_PREF = 2
SLOTS_PER_PREF = 2

LOG = True


GROUP_SIZE = 3

WORKSHOP_CAPACITIES = {
    "A" : 3,
    "B" : 3,
    "C" : 2,
    "D" : 3
}

excel_data = """
    header
1	Anna	2	A	B	C2	C	B2
2	Beate	1	A	B	C2	C	B2
3	Chris	4	B	C	A2	A	C2
4	Dieter	5	B	C	A2	A	C2
5	Emil	3	B	C	A2	A	C2
6	Fred	0	C	A	D2	B	D2
7	Giesela	0	D	A	C2	C	B2
"""

workshop_data = """
key name weight slots timeslot
A	A	1	2	a
B	B	1	3	a
C	C	1	3	a
D	D	1	3	a
A2	A2	1	2	b
B2	B2	1	3	b
C2	C2	1	3	b
D2	D2	1	3	b
"""
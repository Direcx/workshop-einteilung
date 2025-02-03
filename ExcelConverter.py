from typing import Dict, List, Set, Tuple
import logging

#TODO: read workshop capacities from excel file/sheet
WORKSHOP_CAPACITIES = {
    "A" : 3,
    "B" : 3,
    "C" : 2,
    "D" : 3
}

HIGHEST_PREFERENCE_PRIO = 10

class Person:
    name = ""
    preferences = set() # dictionary with "workshop -> prio of pref"
    friend = ""
    excluded_pref = ""
    assigned_workshops = {}

    def __init__(self, row: List[str]):
        self.name = row[1]
        self.friend = row[2]
        self.excluded_pref = row[3]
        for i in range(4):
            if i + 4 < len(row): # check if index exists
                self.preferences.add(HIGHEST_PREFERENCE_PRIO - i)

# results of reading form Excel sheet:
# grouped_persons,
# preferences of grouped_persons,
# excluded_prefs of grouped_persons,
# workshops with capacities and categories

PRIORITY_SCORES = [4, 3, 2, 1]
EXCLUDE = [1]


#TODO: read persons data from excel file/sheet
def parse_persons_data(data: str) -> Dict[str, Person]:
    """Parse the input data from Excel."""
    logging.info("Parsing input data")
    lines = data.strip().split('\n')
    lines_of_data = [line.split('\t') for line in lines[1:]] # Skip header

    # polish data from lines of strings to usable objects
    persons_data: dict[str, Person]= {}
    for row in lines_of_data:
        if len(row) < 8:
            continue
        person = Person(row)
        persons_data[person.name] = person

    return persons_data



excel_data = """
    Kopfzeile
01	Anna	Beate	A	B	C	C	B
02	Beate	Anna	A	B	C	C	B
03	Chris	Dieter	B	C	A	A	C
04	Dieter	Emil	B	C	A	A	C
05	Emil	Chris	B	C	A	A	C
06	Fred	 	C	A	D	B	D
07	Giesela	 	D	A	C	C	B
"""
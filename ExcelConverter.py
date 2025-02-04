from typing import Dict, List, Set, Tuple
from Person import Person

# results of reading form Excel sheet:
# list of persons, imported as Person, and number of persons
# workshops with capacities and categories


#TODO: read persons data from excel file/sheet
def parse_persons_data(data: str) -> Tuple[Dict[str, Person], int]:
    """Parse the input data from Excel."""
    lines = data.strip().split('\n')
    lines_of_data = [line.split('\t') for line in lines[1:]] # Skip header

    persons_count = 0
    # polish data from lines of strings to usable objects
    persons_data: dict[str, Person] = {}
    for row in lines_of_data:
        if len(row) < 8:
            continue
        person = Person(row)
        persons_data[person.name] = person
        persons_count += 1


    return persons_data, persons_count

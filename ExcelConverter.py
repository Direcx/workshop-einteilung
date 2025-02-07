from typing import Dict, Tuple
from classes.Person import Person
from classes.Workshop import Workshop

# results of reading form Excel sheet:
# list of persons, imported as Person, and number of persons
# workshops with capacities and categories

#TODO: check persons data for illegal preferences

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
        persons_data[person.key] = person
        persons_count += 1

    return persons_data, persons_count

def parse_workshop_data(data: str) -> Tuple[Dict[str, Workshop], int]:
    """Parse the input data from Excel."""
    lines = data.strip().split('\n')
    lines_of_data = [line.split('\t') for line in lines[1:]] # Skip header

    workshops_count = 0
    # polish data from lines of strings to usable objects
    workshops_data: dict[str, Workshop] = {}
    for row in lines_of_data:
        if len(row) < 4:
            continue
        workshop = Workshop(row)
        workshops_data[workshop.key] = workshop
        workshops_count += 1

    return workshops_data, workshops_count

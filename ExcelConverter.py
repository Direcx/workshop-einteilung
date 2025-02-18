from typing import Dict, Tuple
from classes.Person import Person
from classes.Workshop import Workshop
import pandas as pd
import Values as v


# results of reading form Excel sheet:
# list of persons, imported as Person, and number of persons
# workshops with capacities and categories

def import_person_data_form_excel(data: str) -> Dict[str, Person]:
    """import person data from Excel."""
    excel_data = pd.read_excel(data, v.SHEET1)

    # polish data from lines of strings to usable objects
    persons_data: dict[str, Person] = {}
    # range from 1 to len to skip the header row
    for i in range(excel_data.shape[0]):
        data_row = []
        for j in range(excel_data.shape[1]):
            if not pd.isna(excel_data.iat[i, j]):
                data_row.append(excel_data.iat[i, j])
            else:
                data_row.append(v.EMPTY_FRIEND_KEY)
        person = Person(data_row)
        persons_data[person.key] = person
    return persons_data

def import_workshop_data_form_excel(data: str) -> Dict[str, Workshop]:
    """import workshop data from Excel."""
    excel_data = pd.read_excel(data, v.SHEET2)

    # polish data from lines of strings to usable objects
    workshop_data: dict[str, Workshop] = {}
    # range from 1 to len to skip the header row
    for i in range(excel_data.shape[0]):
        data_row = []
        for j in range(excel_data.shape[1]):
            if not pd.isna(excel_data.iat[i, j]):
                data_row.append(excel_data.iat[i, j])
            else:
                data_row.append(v.EMPTY_FRIEND_KEY)
        workshop = Workshop(data_row)
        workshop_data[workshop.key] = workshop
    return workshop_data


#TODO: check persons data for illegal preferences


import logging
import Values as v
import ExcelConverter as ec
import GroupHandler as gh
import AllocationProcessor as ap
from classes.GroupPersons import GroupPersons
from classes.Workshop import Workshop

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_persons():
    # log function to log all persons etc.
    logging.info(f"it was {number_persons} persons found")
    logging.info("the persons are:")
    for key in persons.keys():
        logging.info(f"{key} {persons[key].name}")
        logging.info(f"with preferences: {persons[key].preferences}")

def log_groups():
    # log function to log all groups and which persons were grouped
    for key in groups.keys():
        logging.info(f"group {key} consists of {groups[key].get_all_persons_names()}")

def log_workshops():
    for key in workshops.keys():
        logging.info(f"workshop {key} {workshops[key].name} was found")

def log_pre_assigned_workshops():
    for key in workshops.keys():
        logging.info(f"workshop {workshops[key].name} got the following {workshops[key].number_pre_assigned} persons in groups pre-assigned")
        logging.info(f"number of groups: {len(workshops[key].pre_assigned_groups)}")
        for group_key in workshops[key].get_pre_assigned_groups():
            logging.info(f"group {groups[group_key].key} with prio {workshops[key].get_pre_assigned_groups()[group_key][0]}")

def log_assigned_workshops():
    for key in persons.keys():
        logging.info(f"person {persons[key].name} is assigned to {persons[key].assigned_workshops}")
    for key in workshops.keys():
        logging.info(f"workshop {workshops[key].name} has the following persons assigned")
        for i in range(len(workshops[key].assigned_persons)):
            logging.info(f"{workshops[key].name} {i+1} {persons[workshops[key].assigned_persons[i]].name}")

def test_pre_assign():
    group = GroupPersons("tg")
    workshop = Workshop(["hi", "test Workshop", 1, 3])
    logging.info(f"workshop {workshop.name} got {len(workshop.pre_assigned_groups)} groups assigned and"
                 f" {workshop.number_pre_assigned} persons.")
    logging.info(f"{workshop.pre_assigned_groups}")
    workshop = workshop.pre_assign(group.key, 1, 10)
    logging.info(f"workshop {workshop.name} got {len(workshop.pre_assigned_groups)} groups assigned and"
                 f" {workshop.number_pre_assigned} persons.")
    logging.info(f"{workshop.pre_assigned_groups}")
    workshop2 = Workshop(["nope", "newest Workshop", 1, 3])
    logging.info(f"{workshop2.pre_assigned_groups}")


if __name__ == "__main__":
    logging.info("reading person data from excel")
    persons, number_persons = ec.parse_persons_data(v.excel_data)
    #log_persons()

    logging.info("converting persons to groups")
    groups = {}
    groups = gh.convert_persons_to_groups(persons, groups)
    #log_groups()

    logging.info("reading workshop data from excel")
    workshops, number_workshops = ec.parse_workshop_data(v.workshop_data)
    #log_workshops()

    logging.info("pre-assigning groups to workshops")
    ap.set_variables(groups, workshops, persons)
    ap.pre_assign_groups()
    #log_pre_assigned_workshops()

    logging.info("assigning groups to workshops")
    groups, workshops, persons = ap.assign_main()
    log_assigned_workshops()



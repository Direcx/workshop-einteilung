import logging
import Values as v
import ExcelConverter as ec
import GroupHandler as gh
import AllocationProcessor as ap


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
        logging.info(f"workshop {workshops[key].name} got the following {workshops[key].number_pre_assigned} pre-assigned")
        for i in range(workshops[key].number_pre_assigned):
            logging.info(f"group {groups[workshops[key].pre_assigned_groups[i][2]]}")

if __name__ == "__main__":
    logging.info("reading person data from excel")
    persons, number_persons = ec.parse_persons_data(v.excel_data)
    #log_persons()
    logging.info("converting persons to groups")
    groups = gh.convert_persons_to_groups(persons)
    #log_groups()
    logging.info("reading workshop data from excel")
    workshops, number_workshops = ec.parse_workshop_data(v.workshop_data)
    #log_workshops()
    logging.info("pre-assigning groups to workshops")
    groups, workshops = ap.pre_assign_groups(groups, workshops, persons)
    log_pre_assigned_workshops()
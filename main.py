import logging
import Values as Val
import ExcelConverter as Ec
import GroupHandler as Gh
import AllocationProcessor as Ap
from classes.GroupPersons import GroupPersons
from classes.Workshop import Workshop

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_persons():
    # log function to log all persons etc.
    logging.info(f"it was {len(persons)} persons found")
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
        logging.info(f"it has {workshops[key].slots} slots free")

def log_pre_assigned_workshops():
    for key in workshops.keys():
        logging.info(f"workshop {workshops[key].name} got the following {workshops[key].number_pre_assigned} persons in groups pre-assigned")
        logging.info(f"number of groups: {len(workshops[key].pre_assigned_groups)}")
        for group_key in workshops[key].get_pre_assigned_groups():
            logging.info(f"group {groups[group_key].key} with prio {workshops[key].get_pre_assigned_groups()[group_key][0]}")

def log_assigned_workshops():
    for key in workshops.keys():
        logging.info(f"{workshops[key].name} has {len(workshops[key].assigned_persons)} persons assigned:")
        for i in range(len(workshops[key].assigned_persons)):
            logging.info(f"{workshops[key].name} {i+1} {persons[workshops[key].assigned_persons[i]].name}\t with factor {persons[workshops[key].assigned_persons[i]].get_assign_probability()}")

def log_assigned_persons():
    for key in persons.keys():
        logging.info(f"person {persons[key].name} is assigned to {persons[key].assigned_workshops}")


if __name__ == "__main__":
    logging.info("reading person data from excel")
    persons = Ec.import_person_data_form_excel(Val.DATA)
    #log_persons()

    logging.info("converting persons to groups")
    groups = Gh.convert_persons_to_groups(persons)
    #log_groups()

    logging.info("reading workshop data from excel")
    workshops = Ec.import_workshop_data_form_excel(Val.DATA)
    #log_workshops()

    logging.info("pre-assigning groups to workshops")
    Ap.set_variables(groups, workshops, persons)
    Ap.pre_assign_groups()
    #log_pre_assigned_workshops()

    logging.info("assigning groups to workshops")
    #groups, workshops, persons = Ap.assign_main_with_pref_rank()
    groups, workshops, persons = Ap.assign_main_no_pref_rank()

    logging.info("promoting groups to workshops with higher prio")
    Ap.set_variables(groups, workshops, persons)
    groups, workshops, persons = Ap.promote_main()
    #log_assigned_persons()
    log_assigned_workshops()


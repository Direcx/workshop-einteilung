from typing import Dict, List, Set, Tuple
import logging

WORKSHOP_CAPACITIES = {
    "A" : 3,
    "B" : 3,
    "C" : 2,
    "D" : 3
}

PRIORITY_SCORES = [3, 2, 1]

def parse_input_data(data: str) -> List[List[str]]:
    """Parse the input data from Excel."""
    logging.info("Parsing input data")
    lines = data.strip().split('\n')
    return [line.split('\t') for line in lines[1:]]  # Skip header


def process_survey_data(data: List[List[str]]) -> Tuple[Dict[str, List[str]], List[str], Set[str]]:
    """Process survey data to get preferences, friend pairs, and selected shifts."""
    logging.info("Processing survey data")
    preferences = {}
    friend_pairs = {}
    selected_workshops = set()

    for row in data:
        if len(row) < 3:  # Skip rows with insufficient data
            continue
        name = row[1]
        friends_string = row[2]
        preferences[name] = []

        # Store preferences and track selected shifts
        for i in range(3):
            if i + 3 < len(row):  # Check if the index exists
                shift = row[i + 3]
                if shift and shift in WORKSHOP_CAPACITIES:
                    preferences[name].append(shift)
                    selected_workshops.add(shift)
    return preferences, friends_string, selected_workshops

excel_data = """
    Zeitstempel	Dein Name	Personen, mit denen du am liebsten eine Schicht zusammen machen würdest. Hier kannst du so viele Personen auswählen, wie du möchtest.	Priorität 1	Priorität 2	Priorität 3	Priorität 4	Priorität 5
    08.09.2024 23:52:47	Mark	Anna, Johanna, Liv, Melwin, Niki, Sarah K, Sarah R, Tobi J, Tobi L	Bar 23:00-00:30	Bar 00:30-02:00	Kasse 23:00-00:30	Einlass 23:00-00:30	
    08.09.2024 23:53:57	Julian	Anna, Finn, Flori, Magda, Mark, Niki, Sarah K, Sarah R, Tobi J, Tobi L	Bar 21:30-23:00	Bar 23:00-00:30	Kasse 19:45-21:30	Kasse 21:30-23:00	Bar 00:30-02:00
    08.09.2024 23:57:04	Luca	Lisa, Sarah D, Toto	Kasse 19:45-21:30	Bar 19:45-21:30	Kasse 21:30-23:00	Einlass 19:45-21:30	Bar 21:30-23:00
    08.09.2024 23:57:07	Lisa	Luca, Sarah D, Toto	Kasse 19:45-21:30	Bar 19:45-21:30	Kasse 21:30-23:00	Einlass 19:45-21:30	Bar 21:30-23:00
    08.09.2024 23:57:22	Johanna	Liv, Magda, Mark, Melwin, Sarah K, Sarah R, Tobi J, Tobi L	Bar 19:45-21:30	Einlass 19:45-21:30	Kasse 19:45-21:30	Bar 21:30-23:00	Einlass 21:30-23:00
    09.09.2024 00:01:26	Melwin	Liv	Bar 21:30-23:00	Bar 23:00-00:30	Kasse 21:30-23:00		
    09.09.2024 00:01:44	Liv	Melwin	Bar 21:30-23:00	Bar 23:00-00:30	Kasse 21:30-23:00		
    09.09.2024 00:03:39	Anna	Flori, Mark, Sarah K, Sarah R, Tobi J	Bar 21:30-23:00	Bar 23:00-00:30	Kasse 21:30-23:00	Kasse 23:00-00:30	Bar 19:45-21:30
    09.09.2024 00:04:59	Finn	Alex, Anna, Elias, Flori, Isabell, Johanna, Julian, Lenny, Linda, Lisa, Liv, Luca, Magda, Mark, Melwin, Niki, Paula, Sarah D, Sarah K, Sarah R, Sophia, Tobi J, Tobi L, Toto	Bar 23:00-00:30	Bar 00:30-02:00	Bar 21:30-23:00	Bar 19:45-21:30	
    09.09.2024 08:01:09	Sarah D	Lisa, Luca, Toto	Kasse 19:45-21:30	Einlass 19:45-21:30	Bar 19:45-21:30		
    09.09.2024 10:08:16	Toto	Sarah D	Kasse 19:45-21:30	Einlass 19:45-21:30	Bar 19:45-21:30	Kasse 19:45-21:30	Einlass 19:45-21:30
    09.09.2024 10:40:30	Magda	Julian, Tobi L	Bar 21:30-23:00	Bar 19:45-21:30	Kasse 19:45-21:30		
    09.09.2024 10:53:14	Alex	Anna, Finn, Flori, Julian, Magda, Mark, Niki, Sarah K, Sarah R, Tobi J, Tobi L	Bar 21:30-23:00	Bar 19:45-21:30	Bar 23:00-00:30		
    09.09.2024 12:37:22	Niki	Julian, Liv, Mark, Sarah K, Sarah R, Tobi L	Bar 21:30-23:00	Einlass 21:30-23:00	Einlass 23:00-00:30	Bar 19:45-21:30	Bar 23:00-00:30
    09.09.2024 12:44:28	Isabell	Paula	Einlass 19:45-21:30	Einlass 21:30-23:00	Einlass 23:00-00:30		
    09.09.2024 12:44:47	Paula	Isabell	Einlass 19:45-21:30	Einlass 21:30-23:00	Einlass 23:00-00:30		
    09.09.2024 12:49:51	Linda	Lenny, Lisa, Liv, Melwin, Toto	Bar 19:45-21:30	Kasse 19:45-21:30	Einlass 19:45-21:30		
    09.09.2024 13:35:32	Elias	Alex, Anna, Finn, Flori, Isabell, Johanna, Julian, Lenny, Linda, Lisa, Liv, Luca, Magda, Mark, Melwin, Niki, Paula, Sarah D, Sarah K, Sarah R, Sophia, Tobi J, Tobi L, Toto	Bar 19:45-21:30	Bar 21:30-23:00	Einlass 19:45-21:30	Einlass 21:30-23:00	Kasse 19:45-21:30
    09.09.2024 16:16:27	Sophia	Lenny, Linda, Liv, Melwin	Einlass 19:45-21:30	Bar 19:45-21:30	Kasse 19:45-21:30	Einlass 21:30-23:00	Kasse 21:30-23:00
    09.09.2024 17:37:57	Sarah K	Anna, Flori, Johanna, Julian, Mark, Melwin, Niki, Sophia, Tobi J, Tobi L	Bar 21:30-23:00	Einlass 19:45-21:30	Kasse 19:45-21:30	Einlass 21:30-23:00	Kasse 21:30-23:00
    09.09.2024 20:42:56	Tobi L	Julian, Magda	Bar 21:30-23:00	Bar 19:45-21:30	Kasse 19:45-21:30		
    09.09.2024 21:17:18	Tobi J	Anna, Finn, Flori, Johanna, Julian, Magda, Mark, Melwin, Niki, Sarah K, Sarah R, Tobi L	Bar 21:30-23:00	Bar 23:00-00:30	Kasse 21:30-23:00		
    """
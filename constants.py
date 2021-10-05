from enum import Enum

class CSV_COLUMNS(Enum):
    AGE = 0
    GENDER = 1
    COUNTRY = 2
    OFFICIAL_TIME = 3
    OVERALL_PLACE = 4
    GENDER_PLACE = 5
    DIVISION_PLACE = 6
    MILE_PACE = 7

class SCRAPE_PI_CATEGORY(Enum):
    AGE = 2
    GENDER = 3
    COUNTRY = 6
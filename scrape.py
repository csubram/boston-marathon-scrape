import sys
import requests
import bs4 as bs
from time import sleep
from datetime import datetime
from constants import SCRAPE_PI_CATEGORY
from itertools import count


def init_results_file(year):
    with open(f'results/marathon_results_{year}.csv', 'w') as file:

        # Participant information categories
        file.write("AGE,GENDER,COUNTRY,")

        # Official results and placement
        file.write("OFFICIAL_TIME,OVERALL_PLACE,GENDER_PLACE,DIVISION_PLACE,")

        # Pacing and splits
        file.write("MILE_PACE,5K,10K,15K,20K,25K,30K,35K,40K")

        file.write('\n')

def get_participant_info(category, pi_list):
    if (category.value > len(pi_list) or not pi_list[category.value]):
        return ''
    
    return pi_list[category.value].string.strip()

def write_entry_to_results_file(participant_info, official_results, splits):
    age = get_participant_info(SCRAPE_PI_CATEGORY.AGE, participant_info)
    gender = get_participant_info(SCRAPE_PI_CATEGORY.GENDER, participant_info)
    country = get_participant_info(SCRAPE_PI_CATEGORY.COUNTRY, participant_info)

    file = open(f'results/marathon_results_{year}.csv', 'a')
    file.write(f'{age},{gender},{country},')

    # Overall time and scores
    file.write(f'{official_results[2]},{official_results[3]},{official_results[4]},{official_results[5]},')

    # Pace per mile
    file.write(f'{official_results[0]},')

    # 5k - 40k splits each 5k
    splits.pop(4)
    file.write(','.join(splits))

    file.write('\n')
    file.close()

def scrape_results_by_year(year):

    results_url = f'http://registration.baa.org/{year}/cf/Public/iframe_ResultsSearch.cfm'

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'http://registration.baa.org',
        'Referer': f'http://registration.baa.org/{year}/cf/Public/iframe_ResultsSearch.cfm?mode=results',
    }

    # According to the BAA website the max field size of any year
    # was ~39k participants, so this should do to get all the results 
    max_num_participants = 40000

    params = {
        'mode': 'results',
        'criteria': '',
        'StoredProcParamsOn': 'yes',
        'VarGenderID': 0,
        'VarBibNumber': '',
        'VarLastName': '',
        'VarFirstName': '',
        'VarStateID': 0,
        'VarCountryOfResID': 0,
        'VarCountryOfCtzID': 0,
        'VarReportingSegID': 1,
        'VarAwardsDivID': 0,
        'VarQualClassID': 0,
        'VarCity': '',
        'VarTargetCount': max_num_participants,
        'records': 25,
        'headerexists': 'Yes'
    }

    for page, record_number in enumerate(count(1, 25)):

        print(f'Reading page number {page} of up to {int(max_num_participants/25)} pages')

        response = requests.post(
            results_url,
            params=params,
            headers=headers,
            data={'start': record_number, 'next': 'Next 25 Records'}
        )

        soup = bs.BeautifulSoup(response.text, 'html.parser')

        record_headers = soup.find_all('tr', 'tr_header')
        record_body = soup.find_all('table', 'table_infogrid')

        for header, body in zip(record_headers, record_body):

            participant_info = header.find_all('td')

            results_categories = body.find_all('tr')
            
            official_results_raw = results_categories[3].find_all('td')
            official_results = list(map(lambda x: x.string.strip(), official_results_raw))

            splits_raw = results_categories[1].find_all('td')
            splits = list(map(lambda x: x.string.strip(), splits_raw))

            write_entry_to_results_file(participant_info, official_results, splits)


        if 'Next 25 Records' not in response.text:
            print(f'Finished parsing all results.\nTotal of {record_number - 25 + len(record_headers)} records')
            break

        # Don't annoy the server
        sleep(1)


if __name__ == '__main__':
    year = int(sys.argv[1])
    if (year < 2009 or year > datetime.now().year):
        print('Invalid year input. Results are not available prior to 2009 or for the future :)')
        sys.exit(1)

    init_results_file(year)
    scrape_results_by_year(year)
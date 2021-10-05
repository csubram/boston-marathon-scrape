import os.path
from argparse import ArgumentParser
import csv
from constants import CSV_COLUMNS
from filter import GenderFilter, AgeGroupFilter, CountryFilter, MultiFilter
from datetime import datetime, timedelta

def find_average_time(year, filter):
    
    with open(f'results/marathon_results_{year}.csv', 'r') as csv_file:
        result_reader = csv.reader(csv_file, delimiter=',')

        # Skip column headers
        next(result_reader)
        
        sum_time = timedelta(0)
        results_count = 0

        for row in result_reader:
            if filter.filter(row):
                results_count += 1

                t = datetime.strptime(row[CSV_COLUMNS.OFFICIAL_TIME.value], '%H:%M:%S')
                sum_time += timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)

        return sum_time, results_count      


if __name__ == '__main__':
    parser = ArgumentParser(description="""
        This script will find the average finish times in the Boston marathon\n
        with options to view averages by gender, gender and age group, or gender and country.""")
        
    parser.add_argument('year', help='Results year')
    parser.add_argument('gender', choices=['M', 'F'], help='Gender (M/F)')
    parser.add_argument('--country', help='Country code, eg. USA, CAN, KEN')
    parser.add_argument('--age_group', help='Inclusive age range separated by a dash, eg. 19-25')
    
    args = parser.parse_args()

    year = args.year
    if not os.path.exists(f'results/marathon_results_{year}.csv'):
        print(f'Results have not been collected for this year yet.\nTry running "scrape.py {year}"')
    
    category_filters = list()
    gender_filter = GenderFilter(args.gender)

    if (args.age_group):
        age_filter = AgeGroupFilter(args.age_group)
        category_filters.append(age_filter)
    
    if (args.country):
        country_filter = CountryFilter(args.country)
        category_filters.append(country_filter)

    category_filters.append(gender_filter)
    multi_filter = MultiFilter(category_filters)

    sum_time, results_count = find_average_time(year, multi_filter)

    if (results_count == 0):
        print('No results found for the filters specified.')

    else:
        print(f'''Average time for {'Women' if args.gender == 'F' else 'Men'} in 
            {args.country if args.country else 'any country'},
            {f'between ages {args.age_group}' if args.age_group else 'all ages'}
            based on {results_count} results,
            is {sum_time/results_count}''')
    
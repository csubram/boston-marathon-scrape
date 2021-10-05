from constants import CSV_COLUMNS
from abc import ABCMeta, abstractmethod
from typing import List

class Filter:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, bucket):
        self.filter_category = None
        self.filter_bucket = bucket

    def filter(self, row) -> bool:
        match = row[self.filter_category.value] == self.filter_bucket
        return match

class AgeGroupFilter(Filter):
    def __init__(self, bucket):
        self.filter_category = CSV_COLUMNS.AGE
        
        self.min_age = int(bucket.split('-')[0])
        self.max_age = int(bucket.split('-')[1])

    def filter(self, row) -> bool:
        age = int(row[self.filter_category.value])
        return (age >= self.min_age) and (age <= self.max_age)

class GenderFilter(Filter):
    def __init__(self, bucket):
        self.filter_category = CSV_COLUMNS.GENDER
        self.filter_bucket = bucket

class CountryFilter(Filter):
    def __init__(self, bucket):
        self.filter_category = CSV_COLUMNS.COUNTRY
        self.filter_bucket = bucket

class MultiFilter():
    def __init__(self, filters: List[Filter]):
        self.filters = filters

    def filter(self, row):
        for sieve in self.filters:
            if sieve.filter(row) == False:
                return False
        return True
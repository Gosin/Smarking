"""Generate data for analyze.

Generate number of parking cars each hour based on input CSV file.
"""

import csv
import datetime
import cProfile
from collections import OrderedDict


def count_by_hour(entry, exit, counter):
    """Count cars in parking lot."""
    start = entry
    while (start <= exit):
        if start not in counter:
            counter[start] = 1
        else:
            counter[start] += 1
        start += datetime.timedelta(hours=1)


def csv_preprocess(file_name):
    """Preprocess csv file."""
    daily_counter = OrderedDict()
    with open(file_name, 'r') as original_file:
        # skip the header
        next(original_file)
        reader = csv.reader(original_file)
        for row in reader:
            entry = (datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                     .replace(minute=0, second=0)
                     )
            exit = (datetime.datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
                    .replace(minute=0, second=0)
                    )
            count_by_hour(entry, exit, daily_counter)
    OrderedDict(sorted(daily_counter.items(), key=lambda t: t[0]))
    with open('output.csv', 'w', newline='') as output_file:
        output_writer = csv.writer(output_file)
        for key, value in daily_counter.items():
            output_writer.writerow([key, value])

if __name__ == "__main__":
    cProfile.run('csv_preprocess("trans.csv")')

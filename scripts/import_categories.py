#! /usr/bin/env python
"""
Import from a CSV file containing a two-level categorisation for G-Cloud, create
or overwrite a YAML structure as required for our framework question definition.

We expect to see three columns, labelled as follows:

 "Top level (lot)" - used to filter the rows - provide the lot as the second argument
 "Primary category" - more broad categorisation
 "Secondary category" - more specific categorisation (if any)

Usage:
    scripts/import-categories.py <input-csv-file> <lot> [<output-yaml-file>]

"""

from docopt import docopt
import yaml
from collections import defaultdict
import csv
import sys


if __name__ == '__main__':
    arguments = docopt(__doc__)
    primary_by_label = defaultdict(dict)
    lot_filter = arguments['<lot>']

    csv_path = arguments['<input-csv-file>']
    with open(csv_path, 'r') as h_csv:
        reader = csv.DictReader(h_csv)
        for row in reader:
            lot = row['Top level (lot)'].strip()
            if lot == lot_filter:
                primary_label = row['Primary category'].strip()
                secondary_label = row['Secondary category'].strip()
                primary = primary_by_label[primary_label]
                if not primary:
                    primary['label'] = primary_label
                    if secondary_label:
                        primary['options'] = list()

                if secondary_label:
                    secondary = dict()
                    secondary['label'] = secondary_label
                    primary['options'].append(secondary)

    if not primary_by_label:
        print "No data found in that lot"
        sys.exit(1)

    output_file = arguments.get('<output-yaml-file>')
    if output_file:
        with open(output_file, 'r') as yaml_file:
            original_question_data = yaml.safe_load(yaml_file)
    else:
        original_question_data = {}

    original_question_data['options'] = sorted(primary_by_label.values())

    if output_file:
        with open(output_file, 'w') as h_yaml:
            yaml.safe_dump(original_question_data, h_yaml)
    else:
        yaml.safe_dump(original_question_data, sys.stdout)
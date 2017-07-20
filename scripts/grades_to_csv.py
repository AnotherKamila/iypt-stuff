#!/usr/bin/env python3

import glob
import os
import os.path
import sys

import yaml

def sum_grades(grades):
    return sum(grades) - max(grades)/2 - min(grades)/2

def convert(file, save_as):
    countries = {}
    columns   = set()
    with open(file) as raw:
        yml = yaml.safe_load(raw)

        for fightnum, fight in enumerate(yml):
            for room in fight:
                for stage in room['stages']:
                    for teampos in stage['teams']:
                        team = stage['teams'][teampos]
                        row = countries.setdefault(team['team'], {})
                        column = '{}: fight {}'.format(teampos, fightnum+1)
                        columns.add(column)
                        grades = list(map((lambda j: j[-1]), team['grades']))
                        row[column] = sum_grades(grades)

    with open(save_as, 'w') as outfile:
        column_names = sorted(columns)
        print(','.join(['Country']+column_names), file=outfile)
        for country in sorted(countries):
            row = [country]+[countries[country].get(col, '') for col in column_names]
            print(','.join(str(x) for x in row), file=outfile)

if __name__ == '__main__':
    for file in sys.argv[1:] or glob.glob("grades*.yml"):
        save_as = os.path.splitext(file)[0]+'.csv'
        print('{}\t->\t{}\t'.format(file, save_as), file=sys.stderr, end='')
        try:
            convert(file, save_as)
            print('✓', file=sys.stderr)
        except yaml.YAMLError as err:
            print('\nError parsing yaml: {} at {}:{}'.format(err.problem, err.problem_mark.line+1, err.problem_mark.column+1),
                  file=sys.stderr)

#!/usr/bin/python

import zipfile
from os.path import basename, splitext
import csv
import argparse
from itertools import izip_longest
from pprint import pprint


def inspect(path):
    print basename(path)
    with open_indexfile(path) as f:
        reader = csv.reader(f, delimiter='\t')
        print '-', '\n- '.join(next(reader))
        print 'Record count:', sum(1 for _ in reader)


def compare(paths):
    readers = [
        csv.DictReader(open_indexfile(path), delimiter='\t') for path in paths
    ]
    first = readers[0]
    rest = readers[1:]
    fieldnames = first.fieldnames

    for reader in rest:
        if reader.fieldnames != fieldnames:
            print "Fieldnames don't match: %s != %s" % (
                reader.fieldnames, fieldnames
            )
            print "Common fields are", ", ".join(
                set(reader.fieldnames) & set(fieldnames)
            )
            return

    for i, rows in enumerate(izip_longest(*readers)):
        first_row = rows[0]
        for row in rows[1:]:
            for fieldname in fieldnames:
                if not row:
                    continue
                if first_row.get(fieldname) != row.get(fieldname):
                    print "Difference detected in field %s for record %d: %s != %s" % (
                        fieldname, i, first_row.get(fieldname), row.get(fieldname)
                    )


def diff(paths, id_field="filename"):
    readers = [
        csv.DictReader(open_indexfile(path), delimiter='\t') for path in paths
    ]

    records = list({} for _ in paths)

    for reader, path, record in zip(readers, paths, records):
        for row in reader:
            record[row[id_field]] = row

    ids = [
        set(r.keys())
        for r in records
    ]

    all_ids = set()
    for idset in ids:
        all_ids |= idset

    print all_ids

    for idset, path in zip(ids, paths):
        missing = all_ids - idset
        if missing:
            print path, "is missing", ', '.join(missing)
        else:
            print path, "has no missing records"


def print_indexfiles(paths):
    readers = [
        csv.DictReader(open_indexfile(path), delimiter='\t') for path in paths
    ]
    for path, reader in zip(paths, readers):
        print path
        for row in reader:
            pprint(row)
        print


def open_indexfile(path):
    name, ext = splitext(basename(path))

    if ext == '.zip':
        zp = zipfile.ZipFile(path)
        return zp.open(zp.namelist()[0])
    else:
        return open(path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Inspect index files.')
    parser.add_argument(
        '-i', '--inspect', action='store_const', const='inspect', dest='mode',
        default='inspect'
    )
    parser.add_argument(
        '-c', '--compare', action='store_const', const='compare', dest='mode'
    )
    parser.add_argument(
        '-d', '--diff', action='store_const', const='diff', dest='mode'
    )
    parser.add_argument(
        '-p', '--print', action='store_const', const='print', dest='mode'
    )
    parser.add_argument('indexfiles', nargs='+')

    args = parser.parse_args()

    if args.mode == 'inspect':
        print 'Inspecting', ', '.join(args.indexfiles)
        for path in args.indexfiles:
            inspect(path)
    elif args.mode == 'compare':
        print 'Comparing', ', '.join(args.indexfiles)
        compare(args.indexfiles)
    elif args.mode == 'diff':
        print 'Diffing', ', '.join(args.indexfiles)
        diff(args.indexfiles)

    elif args.mode == 'print':
        print_indexfiles(args.indexfiles)

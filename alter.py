#!/usr/bin/python

import os
import zipfile
from os.path import basename, splitext
import csv
import argparse
import tempfile
import shutil
from datetime import timedelta

from django.utils.dateparse import parse_datetime


def unique_id(base, field, fp, out_fp):
    reader = csv.DictReader(fp, delimiter='\t')
    writer = csv.DictWriter(out_fp, reader.fieldnames, delimiter='\t')
    writer.writeheader()

    for i, row in enumerate(reader):
        row[field] = "%s_%d" % (base, i)
        writer.writerow(row)


def adjust(paths, field, field_type):
    for path in paths:
        with tempfile.NamedTemporaryFile() as of:
            reader = csv.DictReader(open_indexfile(path), delimiter='\t')
            writer = csv.DictWriter(of, reader.fieldnames, delimiter='\t')
            writer.writeheader()

            # adjust the value here
            for row in reader:
                value = row[field]
                if field_type == "string":
                    value = value + "_altered"
                elif field_type == "int":
                    value = str(int(value) + 1)
                elif field_type == "float":
                    value = str(float(value) + 0.1)
                elif field_type == "date":
                    value = parse_datetime(
                        value
                    ).replace(tzinfo=None)
                    value = value + timedelta(days=1)
                    value = value.isoformat("T") + "Z"

                row[field] = value

                try:
                    row['checksum'] = str(int(row['checksum']) * 2)
                except:
                    row['checksum'] = row['checksum'] + 'x'

                writer.writerow(row)

            of.flush()
            del reader

            os.unlink(path)

            if splitext(path)[1] == ".zip":
                with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zp:
                    zp.write(of.name, splitext(basename(path))[0])

            else:
                shutil.copyfile(of.name, path)


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
        '-u', '--unique', action='store_const', const='unique', dest='mode'
    )
    parser.add_argument(
        '-a', '--adjust', action='store_const', const='adjust', dest='mode'
    )
    parser.add_argument(
        '-f', '--field', dest='field'
    )
    parser.add_argument(
        '-t', '--type', dest='field_type',
        choices=["int", "float", "string", "date"], default="string"
    )
    parser.add_argument('indexfiles', nargs='+')

    args = parser.parse_args()

    if args.mode == 'unique':
        print 'Uniquising IDs', ', '.join(args.indexfiles)
        for path in args.indexfiles:
            unique_id(path)
    elif args.mode == 'adjust':
        print 'Altering', ', '.join(args.indexfiles)
        adjust(args.indexfiles, args.field, args.field_type)

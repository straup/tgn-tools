#!/usr/bin/env python

import tgn
import logging

if __name__ == '__main__':

    import sys
    import pprint
    import csv

    import optparse

    parser = optparse.OptionParser()

    parser.add_option('--input', dest='input',
                        help='',
                        action='store')

    parser.add_option('--output', dest='output',
                      help='',
                      default=None,
                      action='store')

    parser.add_option('--fieldnames', dest='fieldnames',
                      help='',
                      default=None,
                      action='store')

    parser.add_option("-v", "--verbose", dest="verbose",
                      help="enable chatty logging; default is false", 
                      action="store_true", default=False)

    options, args = parser.parse_args()
    
    if options.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if options.output:

        out = open(options.output, 'w')
    else:
        out = sys.stdout

    writer = None
    fieldnames = None

    if options.fieldnames:

        fieldnames = options.fieldnames.split(",")

        if not 'uri' in fieldnames:
            fieldnames.append('uri')

    # to do: read from STDIN

    path = options.input
    nt = tgn.nt(path)

    if not fieldnames:
        predicates = nt.predicates()
        fieldnames = predicates.keys()

    uri = None
    details = {}

    for key in fieldnames:
        details[key] = ''

    for s,p,o in nt.parse():

        if uri and uri != s:

            details['uri'] = uri

            if not writer:

                logging.debug("setup writer with columns %s" % ",".join(fieldnames))

                writer = csv.DictWriter(out, fieldnames=fieldnames)
                writer.writeheader()

            logging.debug("write row for %s" % uri)

            writer.writerow(details)

            uri = None

            for k, v in details.items():
                details[k] = ''

        uri = s

        details[p] = o

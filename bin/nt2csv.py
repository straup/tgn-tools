#!/usr/bin/env python

import tgn
import logginging

def prepare_details(predicates):

    details = {}

    for key, ignore in predicates.items():
        details[key] = ''

    return details

if __name__ == '__main__':

    import sys
    import pprint
    import csv

    uri = None
    details = None

    out = sys.stdout
    writer = None

    path = sys.argv[1]
    nt = tgn.nt(path)

    predicates = nt.predicates()

    for s,p,o in tgn.parse():

        if uri and uri != s:

            details['uri'] = uri

            if not writer:

                fieldnames = details.keys()
                logging.debug("setup writer with columns %s" % ",".join(fieldnames))

                writer = csv.DictWriter(out, fieldnames=fieldnames)
                writer.writeheader()

            logging.debug("write row for %s" % uri)

            writer.writerow(details)

            uri = None
            details = None

            sys.exit()

        if not uri:
            details = prepare_details(predicates)
            
        uri = s
        details[p] = o

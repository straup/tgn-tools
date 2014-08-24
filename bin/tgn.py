import rdflib
import os.path
import logging
import requests
import StringIO

class nt:

    def __init__ (self, **kwargs):

        if kwargs.get('file', False):

            self.fh = open(kwargs['file'], 'r')

        elif kwargs.get('url', False):

            io = StringIO.StringIO()

            rsp = requests.get(kwargs['url'])
            io.write(rsp.text)
            io.seek(0)

            self.fh = io

        else:

            raise Exception, "Nothing to parse!"

        self.simplify_predicates = kwargs.get('simplify_predicates', True)

    def parse(self):

        self.fh.seek(0)

        for ln in self.fh:

            ln = ln.strip()

            graph = rdflib.Graph()
            graph.parse(data=ln, format='n3')

            for stmt in graph:
                yield self.prepare_statement(stmt)

    def predicates(self):

        predicates = {}
        line = 0

        for s,p,o in self._parse():

            if predicates.get(p, False):
                predicates[p] += 1
            else:
                predicates[p] = 1

            line += 1
            logging.debug("%s %s predicates" % (line, len(predicates.keys())))
            
        return predicates

    def prepare_statement(self, stmt):

        s, p, o = map(unicode, stmt)

        if self.simplify_predicates:

            p = os.path.basename(p)
            
            if "#" in p:
                ignore, p = p.split("#")

        return (s, p, o)

if __name__ == '__main__':

    import sys

    logging.basicConfig(level=logging.DEBUG)

    # path = sys.argv[1]
    # tgn = nt(file='1000095.nt', simplify_predicates=True)

    tgn = nt(url='http://vocab.getty.edu/tgn/1000095.nt', simplify_predicates=False)

    for s,p,o in tgn.parse():
        logging.info("s '%s' p '%s' o '%s'" % (s, p, o))

    sys.exit()

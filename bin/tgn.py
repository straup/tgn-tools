import rdflib
import os.path
import logging

class nt:

    def __init__ (self, path, **kwargs):

        self.fh = open(path, 'r')

        self.simplify_predicates = kwargs.get('simplify_predicates', True)

    def parse(self):

        self.fh.seek(0)

        for ln in self.fh.xreadlines():

            ln = ln.strip()

            graph = rdflib.Graph()
            graph.parse(data=ln, format='n3')

            for stmt in graph:
                yield self.prepare_statement(stmt)

    def predicates(self):

        predicates = {}
        line = 0

        for s,p,o in self.parse():

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

    path = sys.argv[1]
    tgn = nt(path, simplify_predicates=True)

    for s,p,o in tgn.parse():
        logging.info("s '%s' p '%s' o '%s'" % (s, p, o))

    sys.exit()

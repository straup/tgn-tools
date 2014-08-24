# tgn-tools

Various tools to make working with the [Getty TGN linked open data dumps](http://blogs.getty.edu/iris/getty-thesaurus-of-geographic-names-released-as-linked-open-data/) less painful.

Because nothing says _"This is why we can't have nice things"_ like a single file containing 17GB worth of RDF triples...

Basically the goal is to create a set of tools for parsing the data in streams or for generating derivative representations which mean never having to deal with the hassle of loading this stuff in to a triple store or trying to wrap your head around SPARQL queries.

If nothing else it might useful for generating simple CSV files which can be combined in to more useful [GeoJSON files](https://github.com/straup/tgn-geojson). We'll see.

## Example - local file

	import tgn
   
	path = "TGNOut_Coordinates.nt"
	nt = tgn.nt(file=path)

	for s,p,o in nt.parse():

		# do something with each statement

# Example - remote URL

  	url = "http://vocab.getty.edu/tgn/1000095.nt"
	nt = tgn.nt(url=url)

	for s,p,o in nt.parse():

		# do something with each statement

The `parse` methods parses and then [yields](https://docs.python.org/2/reference/simple_stmts.html#the-yield-statement) each line in your *.nt file. It returns still returns a triple (containing a subject, predicate and object in that order) but each part has been explicitly cast as a string. Predicates are simplified by default, according to the following rules:

* The predicate is replaced with the basename of its URI
* If the resultant predicate contains an anchor (for example `#type`) then the predicate is replaced with the value following the hash mark

It is assumed that at some point this will yield unexpected results or hilarity so you can disable simplified predicates in the constructor. Like this:

    path = "TGNOut_Coordinates.nt"
    nt = tgn.nt(path, simplify_predicates=False)

What you do afterwards is up to you but at least now you're just dealing with line-based streams containing strings.

## To do

* A lot, probably.

## See also:

* http://blogs.getty.edu/iris/getty-thesaurus-of-geographic-names-released-as-linked-open-data/
* http://vocab.getty.edu
* https://github.com/straup/tgn-geojson

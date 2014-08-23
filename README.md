# tgn-tools

Various tools to make working with the TGN linked open data dumps less painful. Because nothing says "this is why we can't have nice things like 17GB of triples".

Basically the goal is to create a set of tools for parsing the data in streams or for generating derivative representations which mean never having to deal with the hassle of loading this stuff in to a triple store or trying to wrap your head around SPARQL queries.

If nothing else it might useful for generating simple CSV files which can be combined in to more useful GeoJSON files. We'll see.

## Example

    path = "TGNOut_Coordinates.nt"
    nt = tgn.nt(path)

    for s,p,o in tgn.parse():

    	# do something with each statement

The `parse` methods parses and then [yields]() each line in your *.nt file. We are still returning a triple but each part has been explicitly cast as a string. Predicates are explicitly simplified by default, according to the following rules:

* The predicate is replaced with the basename of its URI
* If the resultant predicate contains an anchor (for example `#type`) then the predicate is replaced with the value following the hash mark

It is assumed that at some point this will yield unexpected results or hilarity so you can disable simplified predicates in the constructor. Like this:

    path = "TGNOut_Coordinates.nt"
    nt = tgn.nt(path, simplify_predicates=False)

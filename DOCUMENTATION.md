# Documentation
===

## `Graph(filename)`
Arguments:
- String `filename`
  - Path for initialization

Initializes a Graph at the path `filename`.  
Returns:
- Graph object
### Sample Usage
```python
db = Graph('graph.db')
```

## `Graph.create_node(labels,properties)`
Arguments:
- Array `labels`
  - Contains short Strings of labels
- Dict `properties`
  - Contains key:value pairs of the node properties.

Adds a node to the graph with the labels defined with `labels` and the properties defined with `properties`.  
Returns:
- Node ID
### Sample Usage
```python
one = db.create_node([":Person"],{'name_first':'John','name_last':'Doe'})
```

## `Graph.create_edge(start,end,label,[directed=True])`
Arguments:
- Integer `start`
  - ID of the starting node
- Integer `end`
  - ID of the ending node
- String `label`
  - Label of the edge
- Optional Boolean argument `directed`
  - If the edge should work in only from start to end.

Adds an edge to the graph with the starting and ending nodes (defined with `start` and `end`), labeled with `label`.
Directed edges allow you to restrict movement along the edge to a single direction.  
Returns:
- Edge ID
### Sample Usage
```python
one = db.create_node([":Person"],{'name_first':'John','name_last':'Doe'})
two = db.create_node([":Person"],{'name_first':'Jane','name_last':'Doe'})

edge = db.create_edge(one,two,':Married')
```
## `Graph.cypher(query)`
**Note: Cypher is not fully implemented. What is described here in the example is the extent of the query functionality.**
Arguments:
- String `query`
  - Multi-line query string.

Allows the user to execute a simple [Cypher](https://neo4j.com/docs/developer-manual/current/cypher/) query.  
Returns:
- Array of resulting nodes or edges in Dict form.
### Sample Usage
```python
db.cypher('''
	MATCH (a:Person)--[:Married]--(b:Person)
	RETURN a,b
''')
```
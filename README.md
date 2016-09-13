### Fusion Center
===

## What this is
Graph Database Engine built with Python on top of Sqlite3

## How to use

This sample code will initialize the database and create four nodes and five edges.

```python
	db = Graph('graph.db')

	one = db.create_node([":Person"],{'name_first':"Jane",'name_last':"Doe"})
	two = db.create_node([":Person"],{'name_first':"Jack",'name_last':"Doe"})
	three = db.create_node([":Person"],{'name_first':"John",'name_last':"Doe"})
	four = db.create_node([":Person"],{'name_first':"Jill",'name_last':"Doe"})
	db.create_edge(one,two,":Mother",directed=True)
	db.create_edge(three,four,":Father",directed=True)
	db.create_edge(one,three,":Married")
	db.create_edge(one,four,":Mother",directed=True)
	db.create_edge(three,two,":Father",directed=True)

```
This code will execute a simple Cypher query to look up the two nodes labeled `:Person`, which are connected by an edge labeled `:Married`
```python
	db.cypher('''
		MATCH (a:Person)--[:Married]--(b:Person)
		RETURN a,b
	''')
````

from graph import Graph

a = Graph('graph.db')
#one = a.create_node([":Person"],{'name_first':"Jane",'name_last':"Doe"})
#two = a.create_node([":Person"],{'name_first':"Jack",'name_last':"Doe"})
#three = a.create_node([":Person"],{'name_first':"John",'name_last':"Doe"})
#four = a.create_node([":Person"],{'name_first':"Jill",'name_last':"Doe"})
#a.create_edge(one,two,":Mother",directed=True)
#a.create_edge(three,four,":Father",directed=True)
#a.create_edge(one,three,":Married")
#a.create_edge(one,four,":Mother",directed=True)
#a.create_edge(three,two,":Father",directed=True)
#print a.get_nodes_by_label(':Person')
#print a.handle_match('(a:Person)<-[:Mother]--(b:Person)','')
print a.cypher('''
	MATCH (a:Person)--[:Married]->(b:Person)
	RETURN a,b
''')

import sqlite3,re,string

def rem_dupes_dict(d):
	out = []
	for item in d:
		if not item in out:
			out.append(item)
	return out
class Graph():
	def __init__(self,file):
		"""
		schema: 
			Edge|1|0|1|;key:value;key:value;|
			Node|1|;key:value;key:value;|	
	
		"""
		self.file = file
		con = sqlite3.connect(self.file)
		c = con.cursor()
		c.execute('''
			CREATE TABLE IF NOT EXISTS nodes
				(id INTEGER PRIMARY KEY, labels TEXT, properties TEXT)
		''')
		c.execute('''
			CREATE TABLE IF NOT EXISTS edges
			(id INTEGER PRIMARY KEY, start INTEGER, end INTEGER, label TEXT, properties TEXT, directed INTEGER)
		''')
		con.commit()
		con.close()

	def create_node(self,labels,prop):
		con = sqlite3.connect(self.file)
		c = con.cursor()
		c.execute('''
			INSERT INTO nodes (labels,properties) VALUES (?,?)
		''',(';'.join(labels),str(prop)))
		last = c.lastrowid
		try:
			con.commit()
			con.close()
			return last
		except Exception as e:
			raise e

	def create_edge(self,to,_from,label,prop={},directed=False):
		con = sqlite3.connect(self.file)
		c = con.cursor()
		c.execute('''
			INSERT INTO edges (start,end,label,properties,directed) VALUES (?,?,?,?,?)
		''',(to,_from,label,str(prop),(1 if directed else 0)))
		last = c.lastrowid
		try:
			con.commit()	
			con.close()
			return last
		except Exception as e:
			raise e

	def get_edges(self,node_id):
		con = sqlite3.connect(self.file)
		c = con.cursor()
		c.execute('''
			SELECT * FROM edges WHERE start=? OR end=?
		''',(node_id,node_id))
		con.commit()
		result = c.fetchall()
		con.close()
		return [{'id':item[0],'start':item[1],'end':item[2],'label':item[3],'properties':item[4]} for item in result]

	def get_node_by_id(self,node_id):
		con = sqlite3.connect(self.file)
		c = con.cursor()
		c.execute('''
			SELECT * FROM nodes WHERE id=?
		''',(node_id,))
		con.commit()
		result = c.fetchone()
		con.close()
		return {'id':result[0],'labels':result[1],'properties':result[2]}

	def get_nodes_by_label(self,label):
		con = sqlite3.connect(self.file)
		c = con.cursor()
		c.execute('''
			SELECT * FROM nodes WHERE labels LIKE ?
		''',("%{}%".format(label),))
		con.commit()
		result = c.fetchall()
		con.close()
		return [{'id':item[0],'labels':item[1],'properties':item[2]} for item in result]

	def get_edges_by_label_start(self,node_id,label):
		con = sqlite3.connect(self.file)
		c = con.cursor()
		c.execute('''
			SELECT * FROM edges WHERE start=? AND label=?
		''',(node_id,label))
		con.commit()
		result = c.fetchall()
		con.close()
		return [{'id':item[0],'start':item[1],'end':item[2],'label':item[3],'properties':item[4],'directed':item[5]} for item in result]

	def get_edges_by_label_end(self,node_id,label):
		con = sqlite3.connect(self.file)
		c = con.cursor()
		c.execute('''
			SELECT * FROM edges WHERE end=? AND label=?
		''',(node_id,label))
		con.commit()
		result = c.fetchall()
		con.close()
		return [{'id':item[0],'start':item[1],'end':item[2],'label':item[3],'properties':item[4],'directed':item[5]} for item in result]

	def check_edges_of_nodes(self,nodelist,nodelist_2,edge_label):
		edges = []
		out_nodes = []
		out_edges = []
		for node in nodelist:
			edges += self.get_edges_by_label_start(node['id'],":"+edge_label)
		for node in nodelist_2:
			for edge in edges:
				if node['id'] == edge['end']:
					out_nodes.append(node)
					out_edges.append(edge)
		for node in nodelist:
			for edge in edges:
				if node['id'] == edge['start']:
					out_nodes.append(node)
					out_edges.append(edge)
		#print out_nodes,out_edges
		return [rem_dupes_dict(out_nodes),rem_dupes_dict(out_edges)]

	def check_directionality_of_edges(edges,dir):
		out = []
		for edge in edges:
			if edge['directed'] == 1:
				out.append(edge)

	def variable_parse(self,nodes,edge,inp):
		a = [[],[],[]]
		o = {'node_1_var': '', 'edge_var': '', 'node_2_var': ''}
		for ed in inp[1]:
			for node in inp[0]:
				if node['id'] == ed['start']:
					a[0].append(node)
					if not ed in a[1]:
						a[1].append(ed)
				elif node['id'] == ed['end']:
					a[2].append(node)
					if not ed in a[1]:
						a[1].append(ed)

		for i in range(len(nodes)):
			if not (len(nodes[i]['var']) == 1 and nodes[i]['var'] in string.punctuation):
				o['node_'+str(i+1)+'_var'] = nodes[i]['var']
			else:
				o['node_'+str(i+1)+'_var'] = '___IGNORE'
		if not (len(edge['var']) == 1 and edge['var'] in string.punctuation):
			o['edge_var'] = edge['var']
		else:
			o['edge_var'] = '___IGNORE'
		out = {}
		out[o['node_1_var']] = a[0] 
		out[o['edge_var']] = a[1]
		out[o['node_2_var']] = a[2]

		return out

	def match_db(self,data):
		out = {}
		nodes = data[0]
		edge = data[1]
		direction = data[2]
		node_1_out = self.get_nodes_by_label(nodes[0]['label'])
		node_2_out = self.get_nodes_by_label(nodes[1]['label'])
		check = self.check_edges_of_nodes(node_1_out,node_2_out,edge['label'])
		out = self.variable_parse(nodes,edge,check)
		#out = self.check_directionality_of_edges(check[1],direction)
		return out


	def handle_match(self,query,more):
		m = re.match(r'\((?P<variable_name>[A-z]+):(?P<labels>[A-z]+)\)(?P<directed_one>.)\-\[?(?P<edge_variable_name>[A-z]+):(?P<edge_label>[A-z]+)\]\-(?P<directed_two>.)\((?P<var_2>[A-z]+):(?P<lab_2>[A-z]+)\)',query)
		node_1 = {'var': m.group('variable_name'), 'label': m.group('labels')}
		edge = {'var': m.group('edge_variable_name'), 'label': m.group('edge_label')}
		node_2 = {'var': m.group('var_2'), 'label': m.group('lab_2')}
		directed_one = 1 if m.group('directed_one') == "<" else 0
		directed_two = 1 if m.group('directed_two') == ">" else 0
		return [[node_1,node_2],edge,[directed_one,directed_two]]

	def handle_where(self,query,more):
		pass

	def pretty_print(self,out,columns):
		rows = []
		for i in range(len(out[0])):
			line = "| "
			for j in range(len(out)):
				x = out[i]
				y = x[j]
				line += '{} |'.format(y['properties'])
			rows.append(line)
		rows = rows[::-1]
		rows.append("="*len(rows[0]))
		#rows.append("|"+"".zfill(len(rows[0])-1))
		rows = rows[::-1]
		return '\n'.join(rows)

	def handle_return(self,query,more):
		q = query.split(',')
		out = []
		for key,value in more.iteritems():
			if key in q:
				out.append(value)
		return out

	def cypher(self,query):
		"""
			query format:
				MATCH (node)--[edge]--(node2)
				WHERE attribute (booleans etc)
				RETURN output
			directionality:
				start -> end
				end <- start

		"""
		q = query.split('\n')
		cache = []
		final_result = None
		pp = ""
		for line in q:
			line = line.strip()
			if line != '':
				if not line.split(' ')[0] in ['MATCH','WHERE','RETURN']:
					raise Exception('There is an error in your Cypher query at line '+str(q.index(line)))
				else:
					l = line.split(' ')
					if l[0] == "MATCH":
						print line
						fin = self.handle_match(l[1:][0],cache)
						data = self.match_db(fin)
						cache = data
					elif l[0] == "WHERE":
						self.handle_where(l[1:],cache)
					elif l[0] == "RETURN":
						final_result = self.handle_return(l[1:][0],cache)
						#pp = self.pretty_print(final_result,cache.keys())
		return final_result
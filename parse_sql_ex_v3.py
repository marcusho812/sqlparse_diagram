import sys
import io

from sqlglot import parse_one, exp
from sqlglot.optimizer.scope import build_scope, traverse_scope, walk_in_scope, ScopeType

from graphviz import Digraph

from TestData import *
from TestFiles import *



sql_code = load_sql_data(TestFiles.temp)
# sql_code = TestQuery.fail_data


expression = sqlglot.parse_one(sql_code, read=sqlglot.Dialects.BIGQUERY)
    
# for e in expression.iter_expressions():
#     print("============================= Printing Node: =============================")
#     print(e)
def printDependencies(dependencies):
    for k, node_link in dependencies.items():
        print(k, node_link)
        


class NodeLink():
    name = None
    event = None
    
    def __init__(self, name, event=None):
        self.name = name
        if event:
            self.event = event
            
    def __repr__(self):
        return str(self.name)

def get_name_or_alias(expression, name_first=True):
    if name_first:
        if not expression.name:
            return cte.alias
        else:
            return cte.name
    else:
        return expression.alias_or_name
    
def get_full_table_name(table):
    return ".".join([p.name for p in table.parts])

def remove_expression(source, exp_type, same_level_only=True):
    first = source.find(exp_type)
    if first is None:
        return
    
    depth_start = first.depth
    for e in source.find_all(exp_type):
        if same_level_only:
            if e.depth > depth_start:
                continue     # maybe should break out of loop because it should never be slower if using BFS
        e.pop()


node_columns = {}

dependencies = {}
for cte in parse_one(sql_code, read=sqlglot.Dialects.BIGQUERY).find_all(exp.CTE):
    cte_name = get_name_or_alias(cte)
       
    cte_cols = [c.alias_or_name for c in cte.find(exp.Select).expressions]
    node_columns[cte_name] = cte_cols
    print(cte_name)
    print(cte_cols) 
    
    
    # columns = [(col.alias_or_name) for col in cte_cols.find_all(exp.Alias)]
    # cte_cols.find(exp.From).pop()
    # cte_cols.find(exp.Join).pop()
    
    # print(cte_name, columns)
    # print(repr(cte))
    # print(repr(cte_cols))
    
    
    
    
    dependencies[cte_name] = []

    for table in cte.find_all(exp.Table):
        table_name = get_full_table_name(table)
        dependencies[cte_name].append(NodeLink(table_name))    

root_name = "root_query"
dependencies[root_name] = []

root_exp = expression.copy()

# Remove CTEs
with_exp = root_exp.find(exp.With)
if with_exp:
    with_exp.pop()
# Check if first expression is Select
root_exp_name = next(root_exp.walk())[0].key
is_raw_select = (root_exp_name == "select")
print("is_raw_select", is_raw_select)
print(repr(root_exp))
    
if not is_raw_select:
    root_cols = [c.alias_or_name for c in root_exp.find(exp.Select).expressions]
    node_columns[root_name] = root_cols
    
    # Store all tables in SELECT and remove SELECT from tree
    select_exp = root_exp.find(exp.Select)  # Choose first SELECT expression
    select_exp.pop()
    for table in select_exp.find_all(exp.Table):
        table_name = get_full_table_name(table)
        dependencies[root_name].append(NodeLink(table_name))
    
    print("After pop")
    printDependencies(dependencies)
    # Remaining table (Should only be one) would be the target table of (INSERT, CREATE TABLE, etc)
    for table in root_exp.find_all(exp.Table):
        table_name = get_full_table_name(table)
        dependencies[table_name] = []
        dependencies[table_name].append(NodeLink(root_name, root_exp_name))
else:
    for table in root_exp.find_all(exp.Table):
        table_name = get_full_table_name(table)
        dependencies[root_name].append(NodeLink(table_name))
        
    root_cols = [c.alias_or_name for c in root_exp.find(exp.Select).expressions]
    node_columns[root_name] = root_cols


# for col in expression.find_all(exp.Column):
#     print(col)
#     for table in  col.parent_select.find_all(exp.Table):
#         print(table.name)
        
    
# insert_exp = root_exp.copy()

# for insert_remove in root_exp.find_all(exp.Insert):
#     print("===============Remove insert===============")
#     print(insert_remove)
#     insert_remove.pop()
    

# print("===============Insert===============")
# for select_exp in insert_exp.find_all(exp.Select):
#     select_exp.pop()
# for table in insert_exp.find_all(exp.Table):
#     print(table)
#     print(table.name)
#     print(table.sql())

# print("===============Root exp===============")
# print(repr(root_exp))
# for table in root_exp.find_all(exp.Table):
#     print("===============Iteration===============")
#     print(table)
#     print(table.name)
#     print(table.sql())
    
#     table_name = get_full_table_name(table)
#     dependencies[root_name].append(table_name) 


# for scopes in traverse_scope(expression):
#     if scopes.scope_type == ScopeType.ROOT:
#         for source in scopes.find_all(exp.Table):
#             source_name = get_full_table_name(source)
#             dependencies[root_name].append(source_name)


print(dependencies)

# sys.exit()

def format_node(table, cols):
    result = ""
    result += table + "\n"
    result += "==================" + "\n"
    for c in cols:
        result += c + "\n"
    return result


dag = Digraph()


for table, cols in node_columns.items():
    dag.node(table, format_node(table, cols))

for node in dependencies:
    for node_link in dependencies[node]:
        dep = node_link.name
        label = node_link.event
        dag.edge(dep, node, label=label)

print(dag.source)
dag.render(view=True)       
        
        



    # select = scopes.find_all(exp.Select)
    # for projection in select:
    #     print(projection.alias_or_name)
    

# for scopes in traverse_scope(expression), list(build_scope(expression).traverse()):
#     print(len(scopes))
#     print(scopes)
#     print(scopes[0].expression.sql())
#     print(scopes[1].expression.sql())
#     print(scopes[0].scope_type)
#     print(scopes[1].scope_type)
    
#     print(scopes[1].source_columns)


# root_scope = build_scope(sql_code)
# print(root_scope)


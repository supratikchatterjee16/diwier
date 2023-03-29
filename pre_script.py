# Query for getting parent dependencies for a table

# Required libraries for connection
import sys
import pandas as pd
import sqlalchemy as sa
from sqlalchemy.engine import create_engine

# DB connection
DIALECT = 'oracle'
SQL_DRIVER = 'cx_oracle'
USERNAME = None
PASSWORD = None
HOST = None
PORT = None
SERVICE = None
ENGINE_PATH_WIN_AUTH = DIALECT + '+' + SQL_DRIVER + '://' + USERNAME + ':' + PASSWORD +'@' + HOST + ':' + str(PORT) + '/?service_name=' + SERVICE

engine = create_engine(ENGINE_PATH_WIN_AUTH)

# Settings

pd.set_option("display.max_rows", None)

def execute_query(query : str) -> pd.DataFrame:
    '''Execution program for running a query and parsing it into a DataFrame
    for visualizations and analytical needs.
    '''
    global engine
    sql_text = sa.text(query)

    with engine.connect() as conn:
        result = conn.execute(sql_text)
        return pd.DataFrame(result)

# Extract Parents
parents_extract_query = '''
select b.table_name, b.column_name, b.r_constraint_name, a.table_name r_table, a.column_name r_col from all_cons_columns a
JOIN
(select a.table_name, b.column_name, a.r_constraint_name, b.position from all_constraints a 
JOIN all_cons_columns b on a.owner = b.owner and a.constraint_name = b.constraint_name
where a.constraint_type = 'R'
and a.table_name IN ({tables})) b 
on b.r_constraint_name = a.CONSTRAINT_NAME and b.position = a.position
order by table_name, column_name
'''

def get_relations(tables : list) -> pd.DataFrame : 
    global parents_extract_query
    table_str ='\'' + '\', \''.join(table for table in tables) + '\''
    return execute_query(parents_extract_query.format(tables=table_str))

# Extract children
children_extract_query = '''
select b.parent, a.table_name child, b.constraint_name
from all_constraints a
JOIN
(select constraint_name, table_name parent from all_cons_columns where table_name in ({tables})) b
on a.r_constraint_name = b.constraint_name
where b.parent != a.table_name
'''

def get_children(tables : list) -> pd.DataFrame : 
    global children_extract_query
    table_str ='\'' + '\', \''.join(table for table in tables) + '\''
    return execute_query(children_extract_query.format(tables=table_str))

# Formulation of the tree structure that is to be later used for rule-mining
class DependencyNode:
    def __init__(self, name):
        self.name = name
        self.relations = {}
        self.parents = set()
        self.children = set()
    
    def update_parents(self, element, relation = None):
        element.update_children(self, relation=relation)
        self.parents.add(element)
        if not relation is None:
            self.relations[element] = relation
    
    def update_children(self, element, relation = None):
        self.children.add(element)
        if not relation is None:
            self.relations[element] = relation
    
    def is_independent(self):
        return (len(self.parents) == 0)
    def has_children(self):
        return (len(self.children) != 0)
    
    def __contains__(self, table_name : str) -> bool:
        flag = False
        for child in self.children :
            if flag == True:
                break
            if child.name == table_name : 
                flag = True
            else:
                if table_name in child : 
                    flag = True
        return flag
    def __eq__(self, other) -> bool:
        if isinstance(other, Table):
            return (other.name == self.name)
        elif isinstance(other, str) :
            return (other == self.name)
        return False
    
    def __str__(self):
        return 'Node({0}, {1})'.format(self.name, self.is_independent(), self.children)
    def __repr__(self):
        return 'Node({0}, {1})'.format(self.name, self.is_independent(), self.children)
    def __hash__(self):
        return hash(self.name)

class Table(DependencyNode):
    '''Class for representing each node of the tree.
    This contains every piece of static information that may be required for analysis.
    
    '''
    def __init__(self, name, cols=None):
        super(Table, self).__init__(name)
        self.cols=cols
        self.visited = False
        self.col_relations = None
    
    def add_cols(self, df : pd.DataFrame):
        self.cols = df
    def add_relations(self, df : pd.DataFrame):
        self.col_relations = df
    def generate_search_criteria(self, module=None):
        selection = ''
        if self.is_independent():
            print('Ignoring rules for independent table :\n', self.col_relations.to_string())
            selection = '''TRUNC({tablename}.{datecol}) BETWEEN (SELECT PRG_PERIOD_START FROM PURGE_MODULE_INPUT WHERE REQUEST_ID = PRG_BTCH_ID AND MODULE = '{module}' AND STATUS = 'INITIATED') AND (SELECT PRG_PERIOD_END FROM PURGE_MODULE_INPUT WHERE REQUEST_ID = PRG_BTCH_ID AND MODULE = '{module}' AND STATUS = 'INITIATED')'''.format(tablename=self.name,datecol=self.get_date_col(), module=module)
        else :
            for parent in self.parents:
                criterias = ''
                for _, row in self.col_relations[self.col_relations['r_table'] == parent.name].iterrows():
                    if len(criterias) > 0:
                        criterias += ' AND '
                    criterias += '{0}.{1} = {2}.{3} '.format(row['table_name'], row['column_name'], row['r_table'], row['r_col'])
                criterias += ' AND ' + parent.generate_search_criteria(module=module)
                selection += 'INNER JOIN {parent_name} ON {criterias}'.format(parent_name = parent.name, criterias = criterias)
        return selection
    def get_cols(self) -> pd.DataFrame:
        return self.cols
    def is_visited(self) -> bool :
        return self.visited
    def set_visited(self) :
        self.visited = True
    def get_date_col(self):
        try:
            return self.cols[(self.cols['data_type'] == 'DATE') & (self.cols['nullable'] == 'N')].iloc[-1]['column_name']
        except Exception as e:
            # print(e)
            return None
    def __str__(self):
        return 'Table({0}, {1})'.format(self.name, self.is_independent(), self.children)
    def __repr__(self):
        return 'Table({0}, {1})'.format(self.name, self.is_independent(), self.children)
    
class DependencyGraph:
    def __init__(self, o_type):
        self.elements : list[o_type]= []
        self._element_type = o_type
    
    def add(self, child, parent = None, relation=None):
        parent_instance = None
        child_instance = None
        # print("Child : {0}, Parent : {1}".format(child, parent))
        if not parent is None:
            if parent in self :
                parent_instance = self[parent]
                # print('Parent found : {0}'.format(parent_instance))
            else:
                parent_instance = self._element_type(parent)
                self.elements.append(parent_instance)
                # print('Parent created')
        # print(self.elements)
        if child in self:
            self[child].update_parents(parent_instance, relation=relation)
            # print('Child updated {0}'.format(self[child]))
        else:
            child_instance = self._element_type(child)
            if not parent_instance is None :
                child_instance.update_parents(parent_instance, relation=relation)
            self.elements.append(child_instance)
            # print('Child created')

    def get_ids(self):
        return [element.name for element in self.elements]
    
    def get_elements(self):
        return self.elements
    def get_originals(self):
        return [element for element in self.elements if element.is_independent()]
    def __str__(self):
        return "DependencyGraph({0})".format(self.get_ids())
    def __iter__(self):
        for element in self.elements:
            yield element
    def __repr__(self):
        return "DependencyGraph({0})".format(self.get_ids())
    def __getitem__(self, name : str):
        name = name.upper()
        for x in self.elements :
            if x == name : 
                return x
    def __contains__(self, name):
        return (name in self.elements)

def generate_dependencies(roots, execution_limit : int = 10) -> list:
    temp = pd.Series(roots)
    graph = DependencyGraph(Table)
    while True:
        df = get_children(temp)
        if df is None or df.shape == (0, 0) :
            break
        for val in df.itertuples():
            graph.add(val[2], parent=val[1], relation = val[3])
        temp = df.iloc[:, 1]
        execution_limit -= 1
        if execution_limit <= 0 :
            break
    cols = get_columns(graph.get_ids())
    relations = get_relations(graph.get_ids())
    for item in graph.get_elements():
        item.add_cols(cols[cols['table_name'] == item.name])
        item.add_relations(relations[relations['table_name'] == item.name])
    return graph

# Generation of the function based on rules-mined from the generated tree
bckp_prg_sql = None
with open('template_function.sql','r') as func_file:
    bckp_prg_sql = func_file.read()

subprog = '''
        IF NOT {0}(purg_req_id, o_error_message)
        THEN
            prog := 'MH_REIM_BATCH_PURGE.{0}';
            RAISE raised_exception;
        END IF;
'''
def generate_function(module, table, backup_prefix='', backup_suffix = 'PRG_BCKP', prefix='MH', func_suffix='BCKP_DEL', subprograms : list = []):
    global bckp_prg_sql, subprog
    table_name = table.name.upper()
    module = module.upper()
    bckp_table = table_name + '_' + backup_suffix
    if not backup_prefix is None and len(backup_prefix) > 0 : 
        bckp_table = (backup_prefix + '_' + bckp_table).upper()
    func_name = '{prefix}_{table}_{func_suffix}'.format(prefix=prefix, table=table_name, func_suffix=func_suffix)
    # insert and delete conditions building
    search_criteria = table.generate_search_criteria(module=module)
    insert_stmt = 'SELECT * INTO {bckp_table} FROM {table_name} '.format(bckp_table=bckp_table, table_name = table_name) + search_criteria
    delete_stmt = 'DELETE FROM (SELECT {table_name}.* FROM {table_name} {search_criteria})'.format(table_name=table_name, search_criteria=search_criteria)
    return func_name, bckp_prg_sql.format(func_name=func_name, table=table_name, bckp_table=bckp_table, module=module, prefix=prefix, insert_stmt=insert_stmt, delete_stmt=delete_stmt, child_backup_purge_program='\n'.join([subprog.format(elem) for elem in subprograms]))

# requisite tables received from Padmashree(RMS Admin, TCS - Spar)

tables =['TSFHEAD', 'TSFDETAIL', 'TSFHEAD_AU', 'TSFDETAIL_AU', 'ORDHEAD', 'ORDLOC', 'ORDHEAD_AU', 'ORDLOC_AU', 'ORDHEAD_REV', 'ORDSKU', 'SHIPMENT', 'SHIPSKU']

# Generation of the purge package for execution, from package template
bckp_prg_pkg_sql = None
with open('template_package.sql', 'r') as pkg_file:
    bckp_prg_pkg_sql = pkg_file.read()
func_head = '''
    FUNCTION {func_name} (
      prg_btch_id       IN       NUMBER,
      o_error_message   IN OUT   VARCHAR2
   )
      RETURN BOOLEAN;
'''
run_head = '''
    FUNCTION RUN_PURGE (o_error_message IN OUT VARCHAR2)
      RETURN BOOLEAN;
'''
run_body = '''
    FUNCTION RUN_PURGE (o_error_message IN OUT VARCHAR2)
      RETURN BOOLEAN
   IS
      program    VARCHAR2 (60) := '{module}.RUN';
      purg_req_id   NUMBER (10) := 0;
   BEGIN
      -- TRUNCATE THE TEMP PRG_REIM_DOC FOR INSERTING FRESH DOC_ID FOR PURGE
      EXECUTE IMMEDIATE 'truncate table PRG_REIM_DOC';

      -- CALLS THE FUNCTION fetch_btch_req_id TO GET REQUEST_ID
      purg_req_id := mh_reim_batch_purge.fetch_btch_req_id (o_error_message);

      --CHECKS REQUEST_ID IS NOT ZERO
      IF purg_req_id <> '0'
      THEN
         BEGIN
             {subprogs}
        END;
        RETURN TRUE;
       ELSE
         o_error_message := 'REQ ID not able to fetch';
         RAISE mh_raise_exception;
       END IF;
    EXCEPTION
      WHEN raised_exception
      THEN
         o_error_message :=
            sql_lib.create_msg ('PACKAGE_ERROR',
                                SQLERRM,
                                program,
                                TO_CHAR (SQLCODE)
                               );
         ROLLBACK;
         RETURN FALSE;
   END RUN_PURGE;
'''

def generate_package(module : str, package_name : str = 'BTCH_PRG', tables : list = [], log=sys.stdout, *args, **kwargs):
    '''Perform the generation of full script as per the flow prepared'''
    orig_out = sys.stdout
    print('Working...', end = '')
    sys.stdout = log
    global bckp_prg_pkg_sql, func_head, subprog, run_head, run_body
    try:
        # print('Generating dependencies...', end='')
        dependency_graph = generate_dependencies(tables)
        print('\n## Tables in graph\n\n```')
        print(dependency_graph, '\n```\n')
        print('\n### Independent tables\n\n```\n', dependency_graph.get_originals(),'\n```')
        print('\n### Dependent tables and their parents\n\n```\n')
        for table in dependency_graph.elements:
            if not table.is_independent() : 
                print(table.name, '\t', [parent.name for parent in table.parents], '  ')
        print('```\n')
        def generate_dependent_functions(module, table, *args, **kwargs):
            funcs = {}
            internal_calls = []
            print('Generating for {0}'.format(table.name))
            if not table.is_independent():
                for parent in table.parents :
                    if not parent.is_visited() :
                        print('Parent {0} is not resolved, ignoring for later'.format(parent.name))
                        return {}
            table.set_visited()
            if table.has_children():
                print('Resolving children : ', ', '.join([child.name for child in table.children]))
                for child in table.children :
                    funcs.update(generate_dependent_functions(module, child, *args, **kwargs))
                for child in table.children :
                    for key in funcs.keys():
                        if child.name in key :
                            internal_calls.append(key)
                print('Finished generating child functions for {0}'.format(table.name))
            k,v = generate_function(module, table, subprograms=internal_calls)
            print('Finished {0}\n'.format(table.name))
            funcs[k] = v
            return funcs
        print('Generating program, listing tables and their children...    ')
        funcs = {}
        originals = dependency_graph.get_originals()
        for table in originals :
            funcs.update(generate_dependent_functions(module, table, *args, **kwargs))

        head = ''
        body = ''
        run_subprogs = ''
        for k,v in funcs.items():
            for table in originals:
                if table.name + '_BCKP_DEL' in k :
                    run_subprogs += subprog.format(k)
            head += func_head.format(func_name=k)
            body += '\n' + v
        head += run_head
        body += '\n' + run_body.format(module=module, subprogs=run_subprogs)
    except Exception as e:
        print('An error occured while generating package : ', e.message)
    finally:
        sys.stdout = orig_out
        print('\rDone        ')
    return bckp_prg_pkg_sql.format(module=module, package=package_name, func_defns=head, func_bodies=body)

with open('RMS_PRG_2.sql', 'w') as generated_file :
    with open('outcome.md', 'w+') as logfile:
        generated_file.write(generate_package(module='RMS', package_name='MH_RMS_BTCH_PRG_2', tables=tables, log =logfile))

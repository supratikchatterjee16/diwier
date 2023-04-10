import pandas as pd
import sqlalchemy as sa
import importlib

from types import ModuleType
from deg import DependencyGraph, DependencyNode

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

def execute_query(engine : sa.engine.Engine, query : str) -> pd.DataFrame:
    '''Execution program for running a query and parsing it into a DataFrame
    for visualizations and analytical needs.
    '''
    sql_text = sa.text(query)

    with engine.connect() as conn:
        result = conn.execute(sql_text)
        return pd.DataFrame(result)

def get_relations(engine : sa.engine.Engine, locale : ModuleType, tables : list) -> pd.DataFrame :
    parents_extract_query = locale.parents_extract
    table_str ='\'' + '\', \''.join(table for table in tables) + '\''
    return execute_query(engine, parents_extract_query.format(tables=table_str))

def get_children(engine : sa.engine.Engine, locale : ModuleType, tables : list) -> pd.DataFrame : 
    children_extract_query = locale.children_extract
    table_str ='\'' + '\', \''.join(table for table in tables) + '\''
    return execute_query(engine, children_extract_query.format(tables=table_str))

def get_columns(engine : sa.engine.Engine, locale : ModuleType, tables : list) -> pd.DataFrame : 
    columns_extract_query = locale.col_extract
    table_str ='\'' + '\', \''.join(table for table in tables) + '\''
    return execute_query(engine, columns_extract_query.format(tables=table_str))

def generate_dependencies(engine : sa.engine.Engine, roots, execution_limit : int = 10) -> list:
    locale = importlib.import_module('diwier.query_store.' + engine.name)
    temp = pd.Series(roots)
    graph = DependencyGraph(Table)
    while True:
        df = get_children(engine, locale, temp)
        if df is None or df.shape == (0, 0) :
            break
        for val in df.itertuples():
            graph.add(val[2], parent=val[1], relation = val[3])
        temp = df.iloc[:, 1]
        execution_limit -= 1
        if execution_limit <= 0 :
            break
    cols = get_columns(engine, locale, graph.get_ids())
    relations = get_relations(engine, locale, graph.get_ids())
    for item in graph.get_elements():
        item.add_cols(cols[cols['table_name'] == item.name])
        item.add_relations(relations[relations['table_name'] == item.name])
    return graph

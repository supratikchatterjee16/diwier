import sys
import sqlalchemy as sa
import importlib

from deg import DependencyGraph
from sqlalchemy.engine import Engine
from diweir.mapper import generate_dependencies
from diweir.config import PurgeConfiguration

def generate_function(locale, module, table, backup_prefix='', backup_suffix = 'PRG_BCKP', prefix='MH', func_suffix='BCKP_DEL', subprograms : list = []):
    bckp_prg_sql = locale.template_function
    subprog = locale.subprog
    table_name = table.name.upper()
    module = module.upper()
    bckp_table = table_name + '_' + backup_suffix
    if backup_prefix is not None and len(backup_prefix) > 0 : 
        bckp_table = (backup_prefix + '_' + bckp_table).upper()
    func_name = '{prefix}_{table}_{func_suffix}'.format(prefix=prefix, table=table_name, func_suffix=func_suffix)
    # insert and delete conditions building
    search_criteria = table.generate_search_criteria(module=module)
    insert_stmt = 'SELECT * INTO {bckp_table} FROM {table_name} '.format(bckp_table=bckp_table, table_name = table_name) + search_criteria
    delete_stmt = 'DELETE FROM (SELECT {table_name}.* FROM {table_name} {search_criteria})'.format(table_name=table_name, search_criteria=search_criteria)
    return func_name, bckp_prg_sql.format(func_name=func_name, table=table_name, bckp_table=bckp_table, module=module, prefix=prefix, insert_stmt=insert_stmt, delete_stmt=delete_stmt, child_backup_purge_program='\n'.join([subprog.format(elem) for elem in subprograms]))


def prepare_purge(engine : Engine, module : str, package_name : str = 'BTCH_PRG', tables : list = [], backup=True, log=sys.stdout, *args, **kwargs):
    orig_out = sys.stdout
    print('Working...', end = '')
    sys.stdout = log
    
    locale = importlib.import_module('diwier.query_store.' + engine.name)
    bckp_prg_pkg_sql = locale.template_package
    func_head = locale.func_head
    subprog = locale.subprog
    run_head = locale.run_head
    run_body = locale.run_body

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
            k,v = generate_function(locale, module, table, subprograms=internal_calls)
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

def purge(configs : PurgeConfiguration):
    pass
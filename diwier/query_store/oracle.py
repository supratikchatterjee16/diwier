parents_extract     = None
children_extract    = None
col_extract         = None
func_head           = None
run_head            = None
run_body            = None
subprog             = None
template_function   = None
template_package    = None

parents_extract = '''
select b.table_name, b.column_name, b.r_constraint_name, a.table_name r_table, a.column_name r_col from all_cons_columns a
JOIN
(select a.table_name, b.column_name, a.r_constraint_name, b.position from all_constraints a 
JOIN all_cons_columns b on a.owner = b.owner and a.constraint_name = b.constraint_name
where a.constraint_type = 'R'
and a.table_name IN ({tables})) b 
on b.r_constraint_name = a.CONSTRAINT_NAME and b.position = a.position
order by table_name, column_name
'''

children_extract = '''
select b.parent, a.table_name child, b.constraint_name
from all_constraints a
JOIN
(select constraint_name, table_name parent from all_cons_columns where table_name in ({tables})) b
on a.r_constraint_name = b.constraint_name
where b.parent != a.table_name
'''

col_extract = '''SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE, NULLABLE FROM ALL_TAB_COLUMNS WHERE TABLE_NAME IN ({tables})'''

subprog = '''
        IF NOT {0}(purg_req_id, o_error_message)
        THEN
            prog := 'MH_REIM_BATCH_PURGE.{0}';
            RAISE raised_exception;
        END IF;
'''

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

template_function = ''''''
template_package = ''''''
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

template_function = '''    FUNCTION {func_name}(
        prg_btch_id       IN       NUMBER,
        o_error_message   IN OUT   VARCHAR2
    )
        RETURN BOOLEAN
    IS
        prog     VARCHAR2 (60) := '{module}.{table}';
        rec_exists     VARCHAR2 (1)  := 'N';
        rec_inserted   NUMBER (20)   := 0;
        rec_deleted    NUMBER (20)   := 1;
    BEGIN
        IF prg_btch_id <> '0'
          THEN
             ---  PURGE TABLE DETIALS ARE INSERTED INTO PURGE_REQUEST_DETAILS
             INSERT INTO purge_request_details VALUES (prg_btch_id, {table}, {bckp_table}, '0', '0', 'INPROGRESS', NULL);

             BEGIN
                -- INSERT STATEMENT FOR {table}
                {insert_stmt}
                -- CAPTURING THE INSERTED RECORDS COUNT
                rec_inserted := SQL%ROWCOUNT;

                BEGIN
                   -- CHECKS WHETHER RECORDS PURGE TABLE RECORDS EXISTS IN PURGE_REQUEST_DETAILS OR NOT
                       -- WHICH IS INSERTED AT EARLIER
                       -- THIS IS KEPT FOR CROSS VERIFICATION PURPOSE IF RECORD EXISTS SET TO Y
                   SELECT 'Y'
                     INTO rec_exists
                     FROM purge_request_details
                    WHERE request_id = prg_btch_id
                      AND prod_tbl_name = '{table}';
                EXCEPTION
                   WHEN NO_DATA_FOUND
                   THEN rec_exists := 'N';
                END;
                {child_backup_purge_program}
                BEGIN
                   -- IF REC EXISTS THEN ONLY IT WILL ALLOWS TO DELETE
                   IF rec_exists = 'Y'
                   THEN
                      -- DELETE STATEMENT FOR {table}
                      {delete_stmt}

                      -- CAPTURING DELETED RECORDS COUNT
                      rec_deleted := SQL%ROWCOUNT;

                      -- CHECKING RECORDS INSERTED AND DELETED ARE MATCHING OR NOT
                      IF rec_inserted >= rec_deleted
                      THEN
                         -- IF RECORDS ARE MATCHED THEN PURGE PROCESS FOR THIS TABLE IS COMPLETE
                         -- SAME IS UPDATED IN PURGE TABLES WITH RECORDS COUNT
                         UPDATE purge_request_details
                            SET status = 'COMPLETED',
                                row_cnt_inserted = row_cnt_inserted + rec_inserted,
                                row_cnt_deleted = row_cnt_deleted + rec_deleted
                          WHERE request_id = prg_btch_id
                            AND prod_tbl_name = {table}
                            AND status = 'INPROGRESS';
                      ELSE
                         -- IF RECORDS COUNT IS NOT MATCHED THEN RAISE EXCEPTION
                         -- AND ABORT PROCESS. ROLLBACK ACTIONS DONE TILL NOW.
                         o_error_message := ' DELETED RECORDS ARE MORE THAN INSERTED FOR {table}';
                         RAISE raised_exception;
                      END IF;
                   ELSE
                      o_error_message := 'NO RECORDS INSERTED INTO purge_request_details FOR {table}';
                      RAISE raised_exception;
                   END IF;
                END;
             END;

             RETURN TRUE;
          ELSE
             o_error_message := 'REQ ID not able to fetch';
             RAISE raised_exception;
          END IF;
       EXCEPTION
          WHEN raised_exception
          THEN
             o_error_message := sql_lib.create_msg ('PACKAGE_ERROR', SQLERRM, prog, TO_CHAR (SQLCODE));
             ROLLBACK;
             RETURN FALSE;
    END {func_name};'''
template_package = '''
CREATE OR REPLACE PACKAGE {module}.{package}
AS
    FUNCTION CREATE_MODULE_REQS();
    FUNCTION DELETE_MODULE_REQS();
    FUNCTION FETCH_BTCH_ID(o_error_message IN OUT VARCHAR2)
      RETURN NUMBER;
    {func_defns}
    
END {package};

CREATE OR REPLACE PACKAGE BODY {module}.{package}
AS
   custom_exception   EXCEPTION;
   raised_exception   EXCEPTION;
   
   FUNCTION CREATE_MODULE_REQS()
   BEGIN
       -- CREATE STATEMENTS FOR PURGING
        CREATE TABLE RMS.PURGE_REQUEST
        (
          REQUEST_ID      NUMBER(10) PRIMARY KEY,
          PURGE_MODULE    VARCHAR2(15 BYTE)             NOT NULL,
          PRG_START_TIME  DATE                          NOT NULL,
          PRG_END_TIME    DATE,
          STATUS          VARCHAR2(10 BYTE)             NOT NULL,
          COMMENTS        VARCHAR2(2500 BYTE),
          CONSTRAINT CHECK_STATUS CHECK (status IN('INITIATED','INPROGRESS','COMPLETED','FAILED')),
          PRIMARY KEY (REQUEST_ID)
        );

        COMMENT ON TABLE PURGE_REQUEST IS 'TABLE FOR INITIATING PURGE AND RECORDING STATUS.';

        CREATE TABLE RMS.PURGE_REQUEST_DETAILS
        (
          REQUEST_ID        NUMBER(10)                  NOT NULL,
          PROD_TBL_NAME     VARCHAR2(100 BYTE)          NOT NULL,
          BKP_TBL_NAME      VARCHAR2(100 BYTE)          NOT NULL,
          ROW_CNT_INSERTED  NUMBER(11)                  NOT NULL,
          ROW_CNT_DELETED   NUMBER(11)                  NOT NULL,
          STATUS            VARCHAR2(10 BYTE)           NOT NULL,
          COMMENTS          VARCHAR2(3000 BYTE),
          CONSTRAINT CHCK_STATUS CHECK (status IN('INITIATED','INPROGRESS','COMPLETED','FAILED')),
          CONSTRAINT CHCK_REQ_ID FOREIGN KEY (REQUEST_ID) REFERENCES RMS.PURGE_REQUEST (REQUEST_ID)
        );

        COMMENT ON TABLE PURGE_REQUEST_DETAILS IS 'TABLE FOR MAINTAINING DETAILS FOR A PURGE REQUEST.';

        CREATE TABLE RMS.PURGE_MODULE_INPUT
        (
          PURGE_DATE           DATE                     NOT NULL,
          MODULE               VARCHAR2(10 BYTE)        NOT NULL,
          PURGE_COMPLETE_DATE  DATE,
          PRG_PERIOD_START     DATE                     NOT NULL,
          PRG_PERIOD_END       DATE                     NOT NULL,
          REQUEST_ID           NUMBER(10),
          STATUS               VARCHAR2(10 BYTE)        NOT NULL,
          COMMENTS             VARCHAR2(3000 BYTE),
          COMMENTS1            VARCHAR2(3000 BYTE),
          CONSTRAINT CHK_STATUS CHECK (status IN('INITIATED','INPROGRESS','COMPLETED','FAILED')),
          CONSTRAINT CHECK_REQ_ID FOREIGN KEY (REQUEST_ID) REFERENCES RMS.PURGE_REQUEST (REQUEST_ID)
        );

        COMMENT ON TABLE PURGE_MODULE_INPUT IS 'TABLE FOR CONTROL PARAMS FOR PURGING.';

        CREATE SEQUENCE RMS.PURGE_REQ_ID START WITH 0 MAXVALUE 999999999 MINVALUE 10 NOCYCLE CACHE 15 ORDER;

   END CREATE_MODULE_TABLES;
   
   FUNCTION DELETE_MODULE_REQS()
   BEGIN
       -- PURGING TABLE DELETION SCRIPT
        DROP TABLE RMS.PURGE_MODULE_INPUT CASCADE CONSTRAINTS;
        DROP TABLE RMS.PURGE_REQUEST_DETAILS CASCADE CONSTRAINTS;
        DROP TABLE RMS.PURGE_REQUEST CASCADE CONSTRAINTS;
        DROP SEQUENCE RMS.PURGE_REQ_ID;
   END DELETE_MODULE_TABLES;
   FUNCTION FETCH_BTCH_ID (o_error_message IN OUT VARCHAR2)
      RETURN NUMBER
   IS
      prog    VARCHAR2 (60) := '{package}.FETCH_BTCH_ID';
      prg_btch_id   NUMBER (10);
   BEGIN
      prg_btch_id := 0;

      -- GETS THE REQUEST ID FOR THE PURGING
      SELECT purge_req_id.NEXTVAL
        INTO prg_btch_id
        FROM DUAL;

      IF prg_btch_id <> '0'
      THEN
         -- WHEN THE PURGE ID IS NOT 0 THEN ONLY IT WILL START THE PROCESS AND INSERT REQUEST_ID DETAILS
         INSERT INTO purge_request
              VALUES (prg_btch_id, 'REIM_BATCH', SYSDATE, NULL, 'INITIATED',
                      NULL);

         -- SAME REQUEST ID ID UPDATE IN PRG MODULE INPUT FOR CHECKING AND FETCHING DETAILS FOR FURTHER REFERNCE
         UPDATE purge_module_input
            SET request_id = prg_btch_id
          WHERE module = '{module}'
            AND status = 'INITIATED'
            AND purge_date = TRUNC (SYSDATE);

         --DBMS_OUTPUT.put_line (prg_btch_id);
         RETURN prg_btch_id;
      ELSE
         -- IF REQ_ID IS NOT ABLE TO GENERATE THEN  IT WILL RAISE EXCEPTION
         o_error_message := 'REQ ID not able to fetch';
         RAISE raised_exception;
      END IF;
   EXCEPTION
      WHEN raised_exception
      THEN
         o_error_message := sql_lib.create_msg ('PACKAGE_ERROR', SQLERRM, prog, TO_CHAR (SQLCODE));
         ROLLBACK;
         RETURN '0';
   END FETCH_BTCH_ID;
   {func_bodies}
END {package};
'''

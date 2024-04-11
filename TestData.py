import sys
import os.path as osp
import io


def load_sql_data(file_path):
    textbuffer = io.StringIO()
    with open(file_path, 'r') as file:
        for i, line in enumerate(file, start=1):
            if line.lower().startswith("declare"):
                continue
            textbuffer.write(line)
            # text = file.read()

    sql_code = textbuffer.getvalue()
    return sql_code




class TestQuery():
    
    a = '''
        with

        A as (
            SELECT 
            id as id_a,
            (SELECT 1 FROM table_k) as content_a
            FROM table_a aa
            LEFT JOIN table_e on table_a.id = table_e.id
            LEFT JOIN table_g on table_a.id = table_g.id
        ),

        C as (
            SELECT 
            id, name
            FROM table_c
        ),

        D as (
            SELECT * FROM C
        )

        SELECT *, D.name
        FROM (
            SELECT * FROM db.B    
        )
        LEFT JOIN D ON A.id = D.id
        '''
    b = '''
        with

        A as (
            SELECT table_a.id 
            FROM (
                SELECT 
                id, name
                FROM table_a
            )
            LEFT JOIN table_a_extra e on table_a.id = e.id
        ),

        C as (
            SELECT 
            id, name
            FROM table_c
        ),

        D as (
            SELECT * FROM C
        )

        SELECT *, D.name
        FROM (
            SELECT * FROM db.B    
        )
        LEFT JOIN D ON A.id = D.id
        '''
    fail_data = '''

                INSERT INTO 'database.export' (a, b)


                With 
                A as (
                    SELECT 
                    *
                    FROM table_a
                ),

                B as (
                    SELECT * FROM A
                )

                SELECT * FROM B


                '''
    c = '''
        
    
        with

        A as (
            SELECT table_a.id 
            FROM (
                SELECT 
                id, name
                FROM table_a
            )
            LEFT JOIN table_a_extra e on table_a.id = e.id
        ),

        C as (
            SELECT 
            id, name
            FROM table_c
        ),

        D as (
            SELECT * FROM C
        )

        SELECT *, D.name
        FROM (
            SELECT id, item FROM db.B    
        ) alias_B
        LEFT JOIN D ON alias_B.id = D.id
        WHERE (SELECT 1 FROM max_check) > alias_B.id
        '''
# 
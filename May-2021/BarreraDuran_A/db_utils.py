from sqlalchemy.orm import Session, mapper
import sqlalchemy as sa
import pandas as pd
from typing import Dict, List


def get_engine():
    """Generates a 'connection string' of sorts that will be used for querying the DB
    the db later on

    Returns
    -------
    engine : `db object`
        the 'connection string'.
    """
    SERVER = '127.0.0.1'
    DATABASE = "AdventureWorks2019"
    UID = "sa"
    PWD = "CorrectHorseBatteryStaple4_For"
    DRIVER = "{ODBC Driver 17 for SQL Server}"

    parms = 'DRIVER='+DRIVER+';SERVER=' + \
        SERVER + ';DATABASE=' + DATABASE + ';UID=' + UID + ';PWD=' + PWD

    engine = sa.create_engine(
        "mssql+pyodbc:///?odbc_connect={}".format(parms))

    return engine


def read_sql(query):
    """ 
    Returns a DataFrame representation of the output of a SQL Query.

    Parameters
    ----------
    query: `string`
        a string that contains structured query language (SQL) executable my MSSQL

    Returns
    -------
    sql_df : `DataFrame`
        a DataFrame representation of the SQL Query
    """
    sql_df = pd.read_sql(query, get_engine())
    return sql_df


def insert_sql(db_model, values: List[Dict]):
    """ 
    Runs insert statements on the SQL Database in bulk using SQL Alchemy's
    ORM.

    Parameters
    ----------
    db_model: `sqlalchemy.schema.Table`
        a objected oriented represention of a SQL Table that lives inside of the DB
    values: `List[Dict]`
        a list of dictionaries which represent the column names (keys) that will be inserted
        into as well as the values
    """
    session = Session(bind=get_engine())
    session.bulk_insert_mappings(db_model, values)
    session.commit()
    session.close()
    return


def update_sql(query):
    """ 
    Executes an update statement inside of SQL given a pure SQL query

    Parameters
    ----------
    query: `string`
        a string that contains structured query language (SQL) executable my MSSQL
    """
    session = Session(bind=get_engine())
    session.execute(query)
    session.commit()
    session.close()
    return
